import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from seqworkflow import OrderWorkflow
from seqactivity import (process_order ,delivery_waiting, dispatch, shipping)

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="order-task-queue_seq",
        workflows=[OrderWorkflow],
        activities=[process_order ,delivery_waiting, dispatch, shipping],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
