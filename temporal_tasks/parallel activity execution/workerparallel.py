import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflowparallel import OrderWorkflow
from activityparallel import hello

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="order-task-queue_seq",
        workflows=[OrderWorkflow],
        activities=[hello.process_order ,hello.delivery_waiting, hello.dispatch, hello.shipping],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
