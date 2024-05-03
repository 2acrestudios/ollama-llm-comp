# Multiple LLM One Prompt

## Overview

This Python script is a command-line interface (CLI) tool designed to interact with a locally hosted machine learning model API to perform comparative performance tests across different models based on user-provided prompts. It allows you to easily compare results from multiple local LLMs, generating a response from the same prompt. It will automatically discover which Ollama models you have installed on your system and give you a list to choose from. We filter out embedding models and color code model families. You also get to set the temperature for each run. Your results will be presented in a formatted report in CLI.

## Features

- **Model Retrieval**: Fetch available machine learning models from a local API.
- **Interactive Testing**: Perform tests using selected models against a specified prompt.

## Installation

Before running the script, ensure you have installed the required dependencies. You can install them using pip:

```bash
pip install requests tqdm termcolor pyfiglet
```

## Usage

Run the script directly from the command line:

```bash
python script_name.py
```

Follow the interactive prompts to select models and set parameters for the test. The script will guide you through the process of choosing models from a displayed list, inputting the desired temperature for the test, and entering the prompt.

## Functions

### `get_available_models()`

Retrieves a list of available non-embedding models from the local API.

**Returns**:
- `list`: Model names available for testing.

**Raises**:
- `requests.exceptions.HTTPError`: If the API request fails.

### `call_ollama(model, prompt, temperature=0.5, context=None)`

Performs a POST request to the API to get responses from a specific model based on the provided prompt and parameters.

**Parameters**:
- `model` (str): Model name to test.
- `prompt` (str): Prompt to send to the model.
- `temperature` (float): Temperature setting for the model's response.
- `context` (list, optional): Additional context for the model.

**Returns**:
- `tuple`: A tuple containing the model's response and the context.

### `performance_test(models, prompt, temperature=0.5, context=None)`

Tests a list of models against a prompt at a specified temperature, displaying results with a progress bar.

**Parameters**:
- `models` (list): List of model names to test.
- `prompt` (str): Prompt for the models.
- `temperature` (float): Temperature setting for the responses.
- `context` (list, optional): Additional context for the models.

**Returns**:
- `dict`: Dictionary with models as keys and their responses as values.

### `main()`

Main function to run the CLI application.

