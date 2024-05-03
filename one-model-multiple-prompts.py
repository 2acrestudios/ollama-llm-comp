import requests
import json
from termcolor import colored
from pyfiglet import Figlet
import time
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_available_models():
    response = requests.get("http://localhost:11434/api/tags")
    response.raise_for_status()
    models = [
        model["name"]
        for model in response.json()["models"]
        if "embed" not in model["name"]
    ]
    return models

def call_ollama(model, prompt, temperature=0.5, context=None):
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

def print_spinner(step):
    spinner = ['|', '/', '-', '\\']
    idx = step % len(spinner)
    sys.stdout.write('\r' + colored(spinner[idx] + " Thinking...", "magenta"))
    sys.stdout.flush()

def main():
    f = Figlet(font="big")
    print(colored(f.renderText("One LLM Multiple Prompts"), "blue"))
    available_models = get_available_models()
    print(colored("------------------------------------------------------------", "magenta"))
    print(colored("Choose the model you want to test against your test prompts.", "white"))
    print(colored("------------------------------------------------------------", "magenta"))
    print(colored("Available Models:", "white"))
    print(colored("------------------------------------------------------------", "magenta"))
    for i, model in enumerate(available_models):
        if "llama" in model:
            color = "cyan"
        elif "mistral" in model:
            color = "green"
        else:
            color = "yellow"
        print(f"{colored(i + 1, color)}.{colored(model, color)}")

    selected_index_str = input("Enter the number of the model you want to test: ").strip()
    if not selected_index_str:
        selected_index = 0
    else:
        selected_index = int(selected_index_str) - 1
    model = available_models[selected_index]

    temperature_str = input("Enter the desired temperature (or press Enter for default 0.5): ")
    if not temperature_str:
        temperature = 0.5
    else:
        temperature = float(temperature_str)

    prompts = [
        "Tell me a joke about using AI to do marketing.",
        "Write a limerick about a programmer who loves Python.",
        "Compose a haiku about the beauty of a starry night sky.",
    ]
    results = []
    step = 0
    for prompt in prompts:
        print_spinner(step)
        result, _ = call_ollama(model, prompt, temperature=temperature)
        results.append(result)
        step += 1
    print(colored("\n\n--- Test Report ---", "green"))
    print(f"Model: {colored(model, 'cyan')}")
    print(f"Temperature: {colored(temperature, 'red')}")
    print(colored("------------------------------------------------------------", "magenta"))
    print(colored("\nPrompts and Results:", "yellow"))
    print(colored("------------------------------------------------------------", "magenta"))
    for i, (prompt, result) in enumerate(zip(prompts, results)):
        print(f"{colored(i+1, 'yellow')}. {prompt}")
        print(f"   {colored('Result:', 'yellow')} {result}\n")
        print(colored("------------------------------------------------------------", "magenta"))

if __name__ == "__main__":
    main()
