import asyncio

from temporalio.client import Client
from another_workflow import GreetingWorkflow

async def main():
    # we need to create connection betwen cleint and server 
    client = await Client.connect("localhost:7233")

# Execution
    workflow_handle = await client.start_workflow(
        GreetingWorkflow.run,
        "Platformatory",
        id="greeting-workflow",
        task_queue="greeting-task-queue"
    )
    result = await workflow_handle.result()
    print(f"Workflow result: {result}")

    # Query the workflow
    greeting = await workflow_handle.query(GreetingWorkflow.get_greeting)
    print(f"Current greeting: {greeting}")

if __name__ == "__main__":
    asyncio.run(main())
