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
    ] 
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


def main():
    # Print ASCII art header
    f = Figlet(font="standard")
    print(colored(f.renderText("Ollama LLM Test"), "cyan"))

    # Get available models and display them with colors
    available_models = get_available_models()
    print(colored("Available Models:", "magenta"))
    for i, model in enumerate(available_models):
        if "llama" in model:
            color = "cyan"
        elif "mistral" in model:
            color = "green"
        else:
            color = "yellow"  # Default color
        print(f"{colored(i+1, color)}.{colored(model, color)}")

    # Get user's model choice
    selected_index = input(
        "Enter the index of the model you want to use: "
    )
    selected_index = int(selected_index.strip()) - 1
    model = available_models[selected_index]

    prompts = [
        "Tell me a joke about using AI to do marketing.",
        "Write a limerick about a programmer who loves Python.",
        "Compose a haiku about the beauty of a starry night sky.",
    ]

    context = None

    # Progress bar for multiple prompts
    with tqdm(
        total=len(prompts),
        desc=colored("Processing Prompts", "green"),
        bar_format="{l_bar}{bar}|",
        position=0,
        leave=True,
    ) as pbar:
        for prompt in prompts:
            print(f"\n{colored('Prompt:', 'blue')} {prompt}")
            result, context = call_ollama(model, prompt, temperature=0.9, context=context)
            print(f"{colored('Result:', 'yellow')} {result}\n")
            pbar.update(1)
            time.sleep(0.1)

    print(colored("\nTest completed.", "magenta"))


if __name__ == "__main__":
    main()
