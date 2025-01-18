from temporalio import activity
import asyncio
import logging
logging.basicConfig(filename='logging.txt',level=logging.INFO)


@activity.defn
async def process_order_activity(order_id: str) -> str:
    logging.info(f"Processing order {order_id}")
    await asyncio.sleep(10)  
    return f"Order {order_id} processed successfully."


@activity.defn
async def cleanup_order_activity(order_id: str) -> str:
    logging.info(f"Cleaning up order {order_id}")
    await asyncio.sleep(1)  
    return f"Cleanup for order {order_id} completed."
