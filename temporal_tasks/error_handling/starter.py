import asyncio
from temporalio.client import Client
from workflowfile import OrderWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        OrderWorkflow.run,
        args=("Arun-order-12345",100.00),          # Amount
        id="order-workflow-id",
        task_queue="order-task-queue",
    )
    print(f"Started workflow with ID: {handle.id}")
    result = await handle.result()
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())