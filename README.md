# 📊 LangSmith REST API Experiments

This repo shows how to record experiments using LangSmith's REST API directly.

It does not require any special test harness or setup - you can run your LLM app however you'd like, then just send the inputs and outputs for each run. This allows you to use [LangSmith](https://docs.langchain.com/langsmith/home) as a system of record to track experiments over time, as well as use features like [annotation queues](https://docs.langchain.com/langsmith/annotation-queues) to help align your app with human preferences and automatically triggered [LLM-as-judge evaluators](https://docs.langchain.com/langsmith/llm-as-judge) to autonomously score performance.

[![](/static/img/tweet.png)](https://x.com/mitsuhiko/status/1978207600706519370)

![](/static/img/rest-experiment.gif)

It is implemented in Python, but the actual language-specific components are lightweight - only a `for` loop in [`recorder.py`](/recorder.py) and a few HTTP calls in [`rest.py`](/rest.py). This minimizes the amount of surface area needed when porting to other languages.

> [!NOTE] 
> If your app is written in Python or TypeScript and you do not already have a evals harness, we suggest using LangSmith's SDKs for the best possible experience. See our [main documentation on evals](https://docs.langchain.com/langsmith/evaluation) to get started.

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy the `.env.example` file to a new file named `.env` with your LangSmith API key. If you don't have one already, you can [sign up here](https://smith.langchain.com/).
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

### LLM-as-judge evaluators

For simplicity and portability, this repo does not run evaluators in code. Instead, we'll cover how to set up LLM-as-judge evaluators that automatically run in LangSmith as your experiment runs finish.

> [!NOTE] 
> If you would like to run evaluators in code, you can [check out this guide](https://docs.langchain.com/langsmith/run-evals-api-only) for examples of how to create feedback via [LangSmith's REST API](https://api.smith.langchain.com/redoc?#tag/feedback/operation/create_feedback_api_v1_feedback_post).

While you can run your evaluators over your experiment locally, you can also configure LangSmith to automatically run LLM-as-judge evaluators over each run.

To do so, navigate back to your dataset in LangSmith, then switch to the `Evaluators` pane:

![](/static/img/create-evaluator.png)

Press the `+ Evaluator` button and select `Create from Scratch`:

![](/static/img/create-from-scratch.png)

The default evaluator measures `correctness`, but you can tweak the prompt, model and feedback criteria as desired. You can also map different parts of your experiment run's inputs and outputs into the prompt.

When you're ready, give it a name, then press `Create` in the top right corner of the pane.

![](/static/img/save-changes.png)

Now, the next time you run an experiment over this dataset, this evaluator will run and leave feedback!

![](/static/img/experiment-with-feedback.png)

LangSmith runs these jobs in a queue, so feedback may be delayed a few minutes.

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

To run the method over real experiment results, you can import and call the `record_langsmith_experiment` method in `recorder.py`, passing in your own inputs, expected reference outputs (if known), and actual outputs as appropriate.

## Project Structure

- `main.py` - Entry point with fixture data
- `recorder.py` - Experiment orchestration logic
- `rest.py` - LangSmith REST API client functions
- `.env` - Environment variables (not committed)

## How It Works

This minimal runner takes the following steps to record experiments:

1. Creates or retrieves a dataset by name
2. Generates deterministic example IDs using UUID5
3. Creates or updates examples in the dataset
4. Creates an experiment session
5. Logs runs for each fixture with metadata and timing
6. Outputs a link to view results in LangSmith UI
