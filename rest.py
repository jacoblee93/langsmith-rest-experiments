import os
import aiohttp
import datetime
import json
import uuid

from dotenv import load_dotenv

load_dotenv()

LANGSMITH_API_URL = "https://api.smith.langchain.com"

HEADERS = {
    "x-api-key": os.getenv("LANGSMITH_API_KEY"),
}


async def get_or_create_dataset(dataset_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{LANGSMITH_API_URL}/datasets?name={dataset_name}&limit=1",
            headers=HEADERS,
        ) as existing_dataset_response:
            response = await existing_dataset_response.json()
            if existing_dataset_response.status == 200 and len(response) == 1:
                return response[0]
            elif existing_dataset_response.status == 404 or len(response) == 0:
                params = {
                    "name": dataset_name,
                    "data_type": "kv",
                }
                async with session.post(
                    f"{LANGSMITH_API_URL}/datasets",
                    headers={
                        **HEADERS,
                        "content-type": "application/json",
                    },
                    json=params,
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(
                            f"Failed to create dataset: {response.status} {await response.text()}"
                        )
            else:
                raise Exception(
                    f"Failed to get dataset: {existing_dataset_response.status} {await existing_dataset_response.text()}"
                )


async def create_example(
    dataset_id: str, example_id: str, inputs: dict, reference_outputs: dict
):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{LANGSMITH_API_URL}/examples",
            headers=HEADERS,
            json={
                "id": example_id,
                "inputs": inputs,
                "outputs": reference_outputs,
                "dataset_id": dataset_id,
            },
        ) as example_response:
            if example_response.status == 200:
                return await example_response.json()
            else:
                raise Exception(
                    f"Failed to create example: {example_response.status} {await example_response.text()}"
                )


async def get_or_create_example(dataset_id: str, inputs: dict, reference_outputs: dict):
    example_id = generate_example_id(dataset_id, inputs, reference_outputs)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{LANGSMITH_API_URL}/examples/{example_id}",
            headers=HEADERS,
        ) as example_response:
            if example_response.status == 200:
                return await example_response.json()
            elif example_response.status == 404:
                return await create_example(
                    dataset_id, example_id, inputs, reference_outputs
                )
            else:
                raise Exception(
                    f"Failed to get example: {example_response.status} {await example_response.text()}"
                )


# Generate a unique example ID for input/reference output example pair
# Using UUID5 (name-based using SHA-1) for deterministic IDs
def generate_example_id(dataset_id: str, inputs: dict, reference_outputs: dict):
    namespace = uuid.NAMESPACE_DNS
    name = f"{dataset_id}-{json.dumps(inputs, sort_keys=True)}-{json.dumps(reference_outputs or {}, sort_keys=True)}"
    return str(uuid.uuid5(namespace, name))


async def create_experiment_session(dataset_id: str, name: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{LANGSMITH_API_URL}/sessions",
            headers=HEADERS,
            json={
                "start_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "reference_dataset_id": dataset_id,
                "name": name,
                "description": "Experiment run via REST API",
            },
        ) as experiment_response:
            if experiment_response.status == 200:
                return await experiment_response.json()
            else:
                raise Exception(
                    f"Failed to create experiment: {experiment_response.status} {await experiment_response.text()}"
                )


async def create_run(
    *,
    inputs: dict,
    outputs: dict,
    start_time: str,
    end_time: str,
    example_id: str,
    session_id: str,
    metadata: dict,
):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{LANGSMITH_API_URL}/runs",
            headers=HEADERS,
            json={
                "name": "Custom fixture run",
                "inputs": inputs,
                "outputs": outputs,
                "reference_example_id": example_id,
                "start_time": start_time,
                "end_time": end_time,
                # Chain may be better here if you are tracing more than a single LLM call
                "run_type": "llm",
                "session_id": session_id,
                "extra": {
                    "metadata": metadata,
                },
            },
        ) as run_response:
            if run_response.status == 202:
                return await run_response.json()
            else:
                raise Exception(
                    f"Failed to create run: {run_response.status} {await run_response.text()}"
                )
