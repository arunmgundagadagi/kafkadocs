from temporalio.worker import Worker
from temporalio.client import Client
import asyncio
from workflowcancel import OrderProcessingWorkflow # type:ignore
from activitycancel import process_order_activity, cleanup_order_activity   # type:ignore


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="order-task-queue",
        workflows=[OrderProcessingWorkflow],
        activities=[process_order_activity, cleanup_order_activity],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
