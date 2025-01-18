import asyncio
from temporalio.client import Client
from workflow111 import OrderWorkflow

async def start_workflow():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Start the workflow
    result = await client.start_workflow(
        OrderWorkflow.run,
        args=("Arunorder123", 500.0),  #Arun oredr     # amount
        id="order-workflow-101010",
        task_queue="Arun-order-task-queue",
    )
    print(f"Workflow started with Run ID: {result.run_id}")

asyncio.run(start_workflow())