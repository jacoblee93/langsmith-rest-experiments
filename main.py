import asyncio
import datetime
import random
import runner

from dotenv import load_dotenv

load_dotenv()

DATASET_NAME = "langsmith-rest-experiments"

experiment_results = [
    {
        "inputs": {"messages": [{"role": "user", "content": "Hello, how are you?"}]},
        # May be omitted if you don't have a reference output
        "reference_outputs": {
            "messages": [{"role": "assistant", "content": "I'm doing well, thank you!"}]
        },
        "outputs": {
            "messages": [{"role": "assistant", "content": "I'm doing well, thank you!"}]
        },
        "metadata": {
            "ls_provider": "openai",
            "ls_model_name": "gpt-5-nano",
            "usage_metadata": {
                "input_tokens": 10,
                "output_tokens": 10,
                "total_tokens": 20,
            },
        },
        "start_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "end_time": (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=5 + random.uniform(0, 5))
        ).isoformat(),
    },
    {
        "inputs": {
            "messages": [{"role": "user", "content": "What is the capital of France?"}]
        },
        # May be omitted if you don't have a reference output
        "reference_outputs": {"messages": [{"role": "assistant", "content": "Paris"}]},
        "outputs": {"messages": [{"role": "assistant", "content": "Marseille"}]},
        "start_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "end_time": (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=5 + random.uniform(0, 5))
        ).isoformat(),
        "metadata": {
            "ls_provider": "openai",
            "ls_model_name": "gpt-5-nano",
            "usage_metadata": {
                "input_tokens": 10,
                "output_tokens": 10,
                "total_tokens": 20,
            },
        },
    },
    {
        "inputs": {
            "messages": [{"role": "user", "content": "What is photosynthesis?"}]
        },
        # May be omitted if you don't have a reference output
        "reference_outputs": {},
        "outputs": {"messages": [{"role": "assistant", "content": "I'm not sure!"}]},
        "start_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "end_time": (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=5 + random.uniform(0, 5))
        ).isoformat(),
        "metadata": {
            "ls_provider": "openai",
            "ls_model_name": "gpt-5-nano",
            "usage_metadata": {
                "input_tokens": 10,
                "output_tokens": 10,
                "total_tokens": 20,
            },
        },
    },
]

if __name__ == "__main__":
    asyncio.run(runner.run_langsmith_experiment(DATASET_NAME, experiment_results))
