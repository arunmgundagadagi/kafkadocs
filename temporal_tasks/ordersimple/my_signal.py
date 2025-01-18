from temporalio.client import Client
from flowofwork import cancel_order
import asyncio
async def send_cancel_signal():
    client = await Client.connect("localhost:7233")
    await client.signal_workflow(
        workflow_id="order-workflow-101010",
        signal=cancel_order, 
    )
    print("Cancel signal sent.")
#if __name__ == __main__ :
#    asyncio.run(send_cancel_signal())

