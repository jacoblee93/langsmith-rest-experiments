import uuid
import aiohttp
from rest import (
    get_or_create_dataset,
    get_or_create_example,
    create_experiment_session,
    create_run,
)


async def record_langsmith_experiment(dataset_name: str, fixture_results: list):
    print(f"Creating experiment with {len(fixture_results)} runs...")
    print()
    async with aiohttp.ClientSession() as session:
        dataset = await get_or_create_dataset(dataset_name, session)
        experiment_session = await create_experiment_session(
            dataset["id"],
            "Custom fixture experiment " + str(uuid.uuid4())[0:8],
            session,
        )
        for fixture in fixture_results:
            example = await get_or_create_example(
                dataset["id"], fixture["inputs"], fixture["reference_outputs"], session
            )
            await create_run(
                inputs=fixture["inputs"],
                outputs=fixture["outputs"],
                start_time=fixture["start_time"],
                end_time=fixture["end_time"],
                example_id=example["id"],
                session_id=experiment_session["id"],
                metadata=fixture["metadata"],
                session=session,
            )
    print(
        f"Experiment created successfully! See it at https://smith.langchain.com/o/{experiment_session['tenant_id']}/datasets/{dataset['id']}/compare?selectedSessions={experiment_session['id']}"
    )
    print()
    print(
        "If you have set up any evaluators for your dataset, they will run asynchronously in the next few minutes."
    )
