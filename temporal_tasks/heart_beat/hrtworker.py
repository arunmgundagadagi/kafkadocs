import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from hrtworkflow import FetchNamesWorkflow
from hrtactvity import enumerating_bigdata

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Start the worker
    worker = Worker(
        client,
        task_queue="names-task-queue",
        workflows=[FetchNamesWorkflow],
        activities=[enumerating_bigdata],
    )

    print("Worker started...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())