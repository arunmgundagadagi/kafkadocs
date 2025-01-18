import asyncio
from temporalio.client import Client
from workflowcancel import OrderProcessingWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    # start workflow
    handle = await client.start_workflow(
        OrderProcessingWorkflow.run,
        "order-12345",
        id="order-workflow-12345",
        task_queue="order-task-queue",
    )
    print(f"Workflow started.")

    
    await asyncio.sleep(45)
    await handle.cancel()
    print("Workflow canceled.")


if __name__ == "__main__":
    asyncio.run(main())
