import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflowretry import MyWorkflow
from activityretry import correct_id

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="retry-task-queue",
        workflows=[MyWorkflow],
        activities=[correct_id],
    )
    print("Worker started. Waiting for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())