from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from flow import GreetingWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="greeting-task-queue",
        workflows=[GreetingWorkflow],
    )
    print("Worker started. Listening for tasks...")
    await worker.run()

asyncio.run(main())
