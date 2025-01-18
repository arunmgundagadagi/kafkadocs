from temporalio.client import Client
from temporalio.worker import Worker
import asyncio 
from workflow111 import OrderWorkflow
from actiivties import validate_order, charge_payment, send_confirmation
async def main():
    
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="Arun-order-task-queue",
        workflows=[OrderWorkflow],
        activities=[validate_order, charge_payment, send_confirmation],
    )
    print("Worker started. Listening for tasks...")
    await worker.run()


    
asyncio.run(main())    