from temporalio import workflow
from activityfile import place_order_activity, process_payment_activity

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str, amount: float):
        try:
            
            order_status = await workflow.execute_activity(
                place_order_activity,
                order_id,
                start_to_close_timeout=5,
            )
            
            payment_status = await workflow.execute_activity(
                process_payment_activity,
                order_id,
                amount,
                start_to_close_timeout=5,
            )
            return f"Workflow completed: {order_status}, {payment_status}"
        except Exception as e:
            return f"Workflow failed with error: {str(e)}"
