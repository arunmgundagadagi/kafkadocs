from temporalio.client import Client
import asyncio
from flow import GreetingWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    # Start the workflow
    handle = await client.start_workflow(
        GreetingWorkflow.run,
        id="greeting-workflow-id",
        task_queue="greeting-task-queue"
    )
    print(f"Workflow started with ID: {handle.id}")


asyncio.run(main())
