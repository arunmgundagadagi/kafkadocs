from temporalio.client import Client
import asyncio
from fstflow import ParallelWorkflow
async def hello():
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233")

    # Start the workflow
    result = await client.execute_workflow(
        ParallelWorkflow.run,
        "aaabbbb",
        id="parallel-workflow-001",
        task_queue="parallel-task-queue",
    )

    # Print the result
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(hello())
        