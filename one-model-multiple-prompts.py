
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = 'llama2:13b-chat-q8_0'

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

def main():
    prompts = [
        "Tell me a joke about using AI to do marketing.",
        "Write a limerick about a programmer who loves Python.",
        "Compose a haiku about the beauty of a starry night sky."
    ]

    model = MODEL
    context = None

    for prompt in prompts:
        print(f"Prompt: {prompt}")
        result, context = call_ollama(model, prompt, temperature=0.9, context=context)
        print(f"Result: {result}\n")

    print("Test completed.")

if __name__ == "__main__":
    main()
