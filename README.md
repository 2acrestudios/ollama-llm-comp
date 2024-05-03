# Ollama Local LLM Competition Testing Scripts
-----------------------------

# Multiple LLM One Prompt

<img src="https://2acrestudios.com/wp-content/uploads/2024/05/3346000889_output.png" style="width:300px;" align="right" />

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
<img src="https://2acrestudios.com/wp-content/uploads/2024/05/376213993_output.png" style="width:300px;" align="right" />
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

-----------------------------------

# One LLM Multiple Prompts

### Script Overview

<img src="https://2acrestudios.com/wp-content/uploads/2024/05/359596278_output.png" style="width:300px;" align="right" />

The script acts as a CLI tool to interact with a local API that serves machine learning models. It is designed to test a single model against multiple creative prompts to evaluate its output in different contexts. It features a user-friendly interface with real-time status updates through a custom spinner. With this script, you can run a single LLM through a 'prompt gauntlet' allowing you to have it generate unique responses for several different prompts in a single run. It automatically discovers which Ollama models you have installed and gives you an easy-to-use interface to choose your model, the temperature, and away it goes! You are presented with a nicely format report in CLI when the run is complete. The script offers a simple but effective way of measuring the performance of local LLM models using your own prompts that fit your use case.

### Key Features

- **Model Selection**: Users can choose from available models fetched from the API.
- **Custom Test Prompts**: Supports testing with a list of predefined creative prompts.
- **Configurable Parameters**: Allows setting the model response temperature dynamically.

### Installation

To run this script, ensure that the following Python packages are installed. You can install them using pip:

```bash
pip install requests termcolor pyfiglet
```

### How to Use

Execute the script from the command line:

```bash
python your_script_name.py
```

Follow the on-screen prompts to select the model and set parameters. The script will then proceed to test the selected model with each prompt and display the results.

### Detailed Function Descriptions

#### `get_available_models()`

Fetches and lists models available from the API that are suitable for generating text (excluding embedding models).

**Returns**:
- `list`: Names of suitable models.

**Exceptions**:
- `requests.exceptions.HTTPError`: Handles API call failures.

#### `call_ollama(model, prompt, temperature=0.5, context=None)`

Sends a request to the API to generate responses based on the model, prompt, and temperature settings.

**Parameters**:
- `model` (str): The selected model's name.
- `prompt` (str): The creative prompt for the model.
- `temperature` (float): Influences the randomness of the response.
- `context` (optional, list): Context data for the model, if any.

**Returns**:
- `tuple`: The complete response text and the context used, if any.

#### `print_spinner(step)`

Displays a spinner in the CLI to indicate ongoing processing.

**Parameters**:
- `step` (int): The current step of the process, used to determine the spinner's state.

#### `main()`

Coordinates the flow of the script:
- Displays the header and model choices.
- Accepts user inputs for model selection and temperature.
- Initiates the processing of multiple prompts.
- Displays the results formatted with colored text.

### Example Usage

Here is an example of the script output during usage, showing the selection process and results display:

```
$ python your_script_name.py
[ASCII art title "One LLM Multiple Prompts"]
Choose the model you want to test against your test prompts:
1. model_name_1
2. model_name_2
Enter the number of the model you want to test: 1
Enter the desired temperature (or press Enter for default 0.5): 0.7
[Spinner indicating processing]
--- Test Report ---
Model: model_name_1
Temperature: 0.7
Prompts and Results:
1. Tell me a joke about using AI to do marketing.
Result: "Why did the marketer break up with the AI? It kept predicting 'It's not you, it's me!'"
------------------------------------------------------------
[Test complete! ASCII art]
```

### Edit the Test Prompts

To edit the prompts, find line #77. You can add as many prompts as you want, and the script will automatically iterate through your entire list. Just know you might over-run your display buffer in your terminal and lose some of your report if you have a very long list of prompts.

```
    prompts = [
        "Tell me a joke about using AI to do marketing.",
        "Write a limerick about a programmer who loves Python.",
        "Compose a haiku about the beauty of a starry night sky.",
    ]
```
