# LangSmith REST API experiments

This repo shows how to record experiments for your LLM apps using LangSmith's REST API directly. It is agnostic of your eval runner, and only requires raw inputs and outputs.

It is implemented in Python, but the actual language-specific components are quite lightweight - only a `for` loop in [`runner.py`](/runner.py) and a few methods in [`rest.py`](/rest.py). This minimizes the amount of surface area needed when porting to other languages.

For simplicity, this base setup does not include leaving feedback on individual runs in your experiment, but we cover how to set up LLM-as-judge evaluators that automatically run in LangSmith over each experiment result [in this section of this README](#setting-up-llm-as-judge-evaluators-in-langsmith).

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Create a `.env` file with your LangSmith API key:
```bash
LANGSMITH_API_KEY=your_api_key_here
```

## Usage

The main script runs an experiment with hard-coded data:

```bash
uv run main.py
```

This will create a dataset named `langsmith-rest-experiments` (if it doesn't exist already), then will populate it with examples from the hard-coded experiment results and create the experiment in LangSmith.

Follow the link logged to the console to see the results in the LangSmith UI!

### Setting up LLM-as-judge evaluators in LangSmith

While you can run your evaluators over your experiment locally, you can also configure LangSmith to automatically run LLM-as-judge evaluators over each run.

<!-- To do so, navigate back to your dataset, and  -->

### Using your own data

`main.py` contains results from three mock experiment runs:

```python
experiment_results = [
    {
        "inputs": {"messages": [{"role": "user", "content": "Your question"}]},
        "reference_outputs": {
            "messages": [{"role": "assistant", "content": "Expected answer (optional)"}]
        },
        "outputs": {"messages": [{"role": "assistant", "content": "Actual answer"}]},
        "start_time": ...,
        "end_time": ...,
        "metadata": {
            "ls_provider": "openai",
            "ls_model_name": "gpt-5-nano",
            "usage_metadata": {
                "input_tokens": 10,
                "output_tokens": 20,
                "total_tokens": 30,
            },
        },
    },
]
```

To run the method over real experiment results, you can import and call the `run_langsmith_experiment` method in `runner.py`, passing in your own inputs, expected reference outputs (if known), and actual outputs as appropriate.

## Project Structure

- `main.py` - Entry point with fixture data
- `runner.py` - Experiment orchestration logic
- `rest.py` - LangSmith REST API client functions
- `.env` - Environment variables (not committed)

## How It Works

1. Creates or retrieves a dataset by name
2. Generates deterministic example IDs using UUID5
3. Creates or updates examples in the dataset
4. Creates an experiment session
5. Logs runs for each fixture with metadata and timing
6. Outputs a link to view results in LangSmith UI
