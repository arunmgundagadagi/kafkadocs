import asyncio
from temporalio.client import Client
from seqworkflow import OrderWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        OrderWorkflow.run,
        "ORDER123",
        id="order-workflow-123",
        task_queue="order-task-queue_seq",
    )
    print(f"Started workflow. Workflow ID: {handle.id}, Run ID: {handle.result_run_id}")

    # Wait for the workflow to complete
    result = await handle.result()
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
