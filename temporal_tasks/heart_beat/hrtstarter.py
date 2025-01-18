import asyncio
from temporalio.client import Client
from hrtworkflow import FetchNamesWorkflow

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Start the workflow to fetch 10 names starting from ID 100
    start_id = 10
    count = 1000
    handle = await client.start_workflow(
        FetchNamesWorkflow.run,
        args=(start_id, count),
        id="fetch-names-workflow",
        task_queue="names-task-queue",
    )

    print(f"Workflow started with ID: {handle.id}")

    # Get the result of the workflow
    result = await handle.result()
    print(f"Fetched Names: {result}")

if __name__ == "__main__":
    asyncio.run(main())
