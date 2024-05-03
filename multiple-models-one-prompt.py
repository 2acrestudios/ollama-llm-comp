import requests
import json
from tqdm import tqdm

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_available_models():
    """Retrieves the list of available models from the Ollama server."""
    response = requests.get("http://localhost:11434/api/tags")
    response.raise_for_status()
    return [model["name"] for model in response.json()["models"]]

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
    for model in tqdm(models, desc="Testing Models"):
        print(f"Testing with model: {model} at temperature {temperature}")
        result, _ = call_ollama(model, prompt, temperature, context)
        results[model] = result
    return results

def main():
    """Main function to run the performance test."""
    available_models = get_available_models()
    print("Available Models:")
    for i, model in enumerate(available_models):
        print(f"{i+1}. {model}")

    selected_indices = input(
        "Enter the indices of the models you want to test (comma-separated): "
    )
    selected_indices = [int(x.strip()) - 1 for x in selected_indices.split(",")]
    models_to_test = [available_models[i] for i in selected_indices]

    prompt = """
    # Instructions:
    # Your influences are:
    # Examples:
    """
    print("Starting performance test between Ollama LLM models...")
    results = performance_test(models_to_test, prompt, temperature=0.9)

    for model, result in results.items():
        print(f"\nResults for {model}:")
        print(result)
    print("\nPerformance test completed.")


if __name__ == "__main__":
    main()
