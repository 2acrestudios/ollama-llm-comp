Below is a comprehensive final draft for the README.md documentation to accompany your Python script, designed to be published directly on your GitHub repository. This documentation is formatted in Markdown to ensure it displays properly on GitHub.

---

# Multiple LLM One Prompt

## Overview

This Python script is a command-line interface (CLI) tool designed to interact with a locally hosted machine learning model API to perform comparative performance tests across different models based on user-provided prompts. It showcases handling API requests, parsing JSON responses, streaming data, and enhancing the command-line user experience with progress bars and colored text.

## Features

- **Model Retrieval**: Fetch available machine learning models from a local API.
- **Interactive Testing**: Perform tests using selected models against a specified prompt.
- **Visual Enhancements**: Use ASCII art and colored text to improve the readability and user experience of CLI outputs.
- **Progress Tracking**: Utilize a progress bar to show ongoing test status.

## Installation

Before running the script, ensure you have the required dependencies installed. You can install them using pip:

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

