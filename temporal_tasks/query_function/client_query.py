import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from another_workflow import GreetingWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    
    worker = Worker(
        client,
        task_queue="greeting-task-queue",
        workflows=[GreetingWorkflow]
    )
    
    print("Worker started. Listening on 'greeting-task-queue'...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
