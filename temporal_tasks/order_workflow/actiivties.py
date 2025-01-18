from temporalio import activity
import asyncio

@activity.defn
async def validate_order(order_id: str):
    print(f"Validating order {order_id}")
    # Simulate validation logic
    await asyncio.sleep(3)
    return True

@activity.defn
async def charge_payment(order_id: str, amount: float):
    print(f"Charging ${amount} for order {order_id}")
    # Simulate payment charging
    await asyncio.sleep(3)
    return "Payment successful"

@activity.defn
async def send_confirmation(order_id: str):
    print(f"Sending confirmation email for order {order_id}")
    # Simulate email sending
    await asyncio.sleep(3)
    return "Email sent"