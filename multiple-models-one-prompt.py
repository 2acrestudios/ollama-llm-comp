import requests
import json
from tqdm import tqdm

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELS = [
    'llama3:8b', 
    'dolphin-llama3:8b-v2.9-fp16',
    'deepseek-coder:6.7b-instruct-fp16',
    'gemma:2b-instruct',
    'gemma:2b-instruct-fp16',
    'llama2:13b-chat-q8_0',
    'llama3:8b-instruct-fp16',
    'llama3:latest',
    'llama3-gradient:8b-instruct-1048k-fp16',
    'mistral:7b-instruct-v0.2-fp16',
    'mistral:7b-instruct-v0.2-q8_0',
    'nous-hermes2:10.7b-solar-fp16',
    'open-orca-platypus2:13b-q8_0',
    'phi3:3.8b-mini-instruct-4k-fp16',
    'samantha-mistral:7b-instruct-fp16'
]

def call_ollama(model, prompt, temperature=0.5, context=None):
    payload = {
        'model': model,
        'prompt': prompt,
        'temperature': temperature,
        'context': context if context is not None else []
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}", None

    response_parts = []
    for line in response.iter_lines():
        part = json.loads(line)
        response_parts.append(part.get('response', ''))
        if part.get('done', False):
            break

    return ''.join(response_parts), part.get('context', None)

def performance_test(prompt, temperature=0.5, context=None):
    results = {}
    for model in MODELS:
        print(f"Testing with model: {model} at temperature {temperature}")
        result, _ = call_ollama(model, prompt, temperature, context)
        results[model] = result
    return results

def main():
    prompt = """
    # Instructions:
    # Your influences are: 
    # Examples: 
    """

    print("Starting performance test between Ollama LLM models...")
    results = performance_test(prompt, temperature=0.9)

    for model, result in results.items():
        print(f"\nResults for {model}:")
        print(result)

    print("\nPerformance test completed.")

if __name__ == "__main__":
    main()
