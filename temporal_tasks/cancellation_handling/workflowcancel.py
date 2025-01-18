from datetime import timedelta
import asyncio
from temporalio import workflow
from temporalio.exceptions import CancelledError
from activitycancel import process_order_activity, cleanup_order_activity
import logging 

logging.basicConfig(filename='logging.txt',level=logging.WARNING)

@workflow.defn
class OrderProcessingWorkflow:
    def __init__(self):
        self.order_id = None

    @workflow.run
    async def run(self, order_id: str) -> None:
        self.order_id = order_id

        try:
            # Step 1: Process the order
            await workflow.execute_activity(
                process_order_activity,
                self.order_id,
                start_to_close_timeout=timedelta(seconds=30),
            )

            while True:
                workflow.logging.info(f"Waiting for additional steps on order {self.order_id}")
                await asyncio.sleep(60)

        except asyncio.CancelledError:
            logging.warning(f"Workflow for order {self.order_id} canceled. Cleaning up.")
            
            
            cancel = await workflow.execute_activity(
                cleanup_order_activity,
                self.order_id,
                start_to_close_timeout=timedelta(seconds=30),
            )
            return cancel

