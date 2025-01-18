from temporalio import activity

@activity.defn
async def place_order_activity(order_id: str) -> str:
    try:
        # Simulate placing an order
        if not order_id:
            raise ValueError("Order ID is invalid!")
        return f"Order {order_id} placed successfully."
    except Exception as e:
        raise activity.ActivityError(f"Place order failed: {str(e)}")

@activity.defn
async def process_payment_activity(order_id: str, amount: float) -> str:
    try:
        # Simulate payment processing
        if amount <= 0:
            raise ValueError("Amount must be greater than zero!")
        return f"Payment for order {order_id} of ${amount} processed successfully."
    except Exception as e:
        raise activity.ActivityError(f"Payment processing failed: {str(e)}")