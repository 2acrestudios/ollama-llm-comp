import requests
import json
from tqdm import tqdm  # For the progress bar (even though it's one prompt)
from termcolor import colored
from pyfiglet import Figlet
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama2:13b-chat-q8_0"


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

    prompts = [
        "Tell me a joke about using AI to do marketing.",
        "Write a limerick about a programmer who loves Python.",
        "Compose a haiku about the beauty of a starry night sky.",
    ]

    model = MODEL
    context = None

    # Progress bar for multiple prompts
    with tqdm(total=len(prompts), desc=colored("Processing Prompts", "green"), bar_format="{l_bar}{bar}|", position=0, leave=True) as pbar:
        for prompt in prompts:
            print(f"\n{colored('Prompt:', 'blue')} {prompt}")
            result, context = call_ollama(model, prompt, temperature=0.9, context=context)
            print(f"{colored('Result:', 'yellow')} {result}\n")
            pbar.update(1)
            time.sleep(0.1)  

    print(colored("\nTest completed.", "magenta"))


if __name__ == "__main__":
    main()
