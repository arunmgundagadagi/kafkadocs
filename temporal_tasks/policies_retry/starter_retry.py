import asyncio
from temporalio.client import Client
from workflowretry import MyWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        MyWorkflow.run,
        "Arun123",  
        id="retry-workflow-id",
        task_queue="retry-task-queue",
    )
    print(f"Started workflow with ID: {handle.id}")
    result = await handle.result()
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())