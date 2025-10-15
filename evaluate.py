import uuid
from rest import (
    get_or_create_dataset,
    get_or_create_example,
    create_experiment_session,
    create_run,
)

from dotenv import load_dotenv

load_dotenv()

DATASET_NAME = "langchain-api-evals"


async def create_experiment(fixture_results: list):
    print(f"Creating experiment with {len(fixture_results)} runs...")
    print()
    dataset = await get_or_create_dataset(DATASET_NAME)
    experiment_session = await create_experiment_session(
        dataset["id"], "Custom fixture experiment " + str(uuid.uuid4())[0:8]
    )
    for fixture in fixture_results:
        example = await get_or_create_example(
            dataset["id"], fixture["inputs"], fixture["reference_outputs"]
        )
        await create_run(
            inputs=fixture["inputs"],
            outputs=fixture["outputs"],
            start_time=fixture["start_time"],
            end_time=fixture["end_time"],
            example_id=example["id"],
            session_id=experiment_session["id"],
            metadata=fixture["metadata"],
        )
    print(
        f"Experiment created successfully! See it at https://smith.langchain.com/o/{experiment_session['tenant_id']}/datasets/{dataset['id']}/compare?selectedSessions={experiment_session['id']}"
    )
    print()
    print("If you have set up any evaluators for your dataset, they will run asynchronously in the next few minutes.")
