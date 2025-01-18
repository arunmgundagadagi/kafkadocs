from temporalio.client import Client
from temporalio.worker import Worker
from fstflow import ParallelWorkflow
from activity111 import activity_one, activity_two
import asyncio
 
async def main():
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233", namespace="default")

    # Create a worker
    worker = Worker(
        client,
        task_queue="parallel-task-queue",
        workflows=[ParallelWorkflow],
        activities=[activity_one, activity_two],
    )

    # Start the worker
    print("Worker started.")
    await worker.run()


asyncio.run(main())