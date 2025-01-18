import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflowfile import OrderWorkflow
from activityfile import place_order_activity, process_payment_activity

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="order-task-queue",
        workflows=[OrderWorkflow],
        activities=[place_order_activity, process_payment_activity],
    )
    print("Worker started. Waiting for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())