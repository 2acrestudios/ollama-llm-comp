import requests
import json
from tqdm import tqdm
from termcolor import colored
from pyfiglet import Figlet
import time

OLLAMA_URL = "http://localhost:11434/api/generate"


def get_available_models():
    """Retrieves the list of available models from the Ollama server, excluding embed models."""
    response = requests.get("http://localhost:11434/api/tags")
    response.raise_for_status()
    models = [
        model["name"]
        for model in response.json()["models"]
        if "embed" not in model["name"]
    ]  # Filter out models containing 'embed'
    return models

def call_ollama(model, prompt, temperature=0.5, context=None):
    """Sends a generation request to the Ollama server and returns the response."""
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "context": context if context is not None else [],
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}", None
    response_parts = []
    for line in response.iter_lines():
        part = json.loads(line)
        response_parts.append(part.get("response", ""))
        if part.get("done", False):
            break
    return "".join(response_parts), part.get("context", None)


def performance_test(models, prompt, temperature=0.5, context=None):
    """Conducts performance tests on the specified models using the given prompt."""
    results = {}
    with tqdm(
        total=len(models),
        desc=colored("Testing Models", "green"),
        bar_format="{l_bar}{bar}|",
        position=0,
        leave=True,
    ) as pbar:
        for model in models:
            # Print model information on a new line
            print(
                f"\n{colored('Testing with model:', 'blue')} {colored(model, 'yellow')} {colored('at temperature', 'red')} {colored(temperature, 'red')}"
            ) 
            result, _ = call_ollama(model, prompt, temperature, context)
            results[model] = result
            pbar.update(1)
            time.sleep(0.1)
    return results


def main():
    # Print ASCII art header
    f = Figlet(font="standard")
    print(colored(f.renderText("Ollama LLM Test"), "magenta"))

    """Main function to run the performance test."""
    available_models = get_available_models()
    print(colored("Available Models:", "magenta"))
    for i, model in enumerate(available_models):
        if "llama" in model:
            color = "cyan"
        elif "mistral" in model:
            color = "green"
        elif "gemma" in model:
            color = "blue"
        else:
            color = "yellow"  # Default color
        print(f"{colored(i+1, color)}.{colored(model, color)}")

    selected_indices = input(
        "Enter the indices of the models you want to test (comma-separated): "
    )
    selected_indices = [int(x.strip()) - 1 for x in selected_indices.split(",")]
    models_to_test = [available_models[i] for i in selected_indices]

    prompt = """
    # Instructions: write a poem
    # Your influences are: Your favorite author
    # Examples: Your favorite work by your favorite author
    """
    print("Starting performance test between Ollama LLM models...")
    results = performance_test(models_to_test, prompt, temperature=0.9)

    for model, result in results.items():
        print(f"\n{colored('Results for', 'yellow')} {colored(model, 'yellow')}:")
        print(result)
    print(colored("\nPerformance test completed.", "magenta"))


if __name__ == "__main__":
    main()
