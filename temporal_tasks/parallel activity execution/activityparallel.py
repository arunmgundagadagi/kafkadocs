from temporalio import activity
import asyncio

class hello:
    @activity.defn
    async def process_order(order_id: str) -> str:
        await asyncio.sleep(2)
        return f"Order {order_id} has been processed successfully!"
    @activity.defn
    async def delivery_waiting(order_id: str) -> str:
        await asyncio.sleep(2)
        return f"Order {order_id} has been waiting for delivery"
    @activity.defn
    async def dispatch(order_id: str) -> str:
        await asyncio.sleep(2)
        return f"Order {order_id} has been dispatched"
    @activity.defn
    async def shipping(order_id: str) -> str:
        await asyncio.sleep(2)
        return f"Order {order_id}  shipped at xxxxxx"

