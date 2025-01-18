from temporalio import workflow
from seqactivity import (process_order ,delivery_waiting, dispatch, shipping)
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Synchronous execution of the activity
        result1 = await workflow.execute_activity(
            process_order,
            order_id,
            task_queue="order-task-queue_seq",
            start_to_close_timeout=timedelta(seconds=20),
        )
        print(result1)
        result2 = await workflow.execute_activity(
            delivery_waiting,
            order_id,
            task_queue="order-task-queue_seq",
            start_to_close_timeout=timedelta(seconds=20),
        ) 
        print(result2)
        result3 = await workflow.execute_activity(
            dispatch,
            order_id,
            task_queue="order-task-queue_seq",
            start_to_close_timeout=timedelta(seconds=20),
        )
        print(result3)
        result4 = await workflow.execute_activity(
            shipping,
            order_id,
            task_queue="order-task-queue_seq",
            start_to_close_timeout=timedelta(seconds=20),
        )
        print(result4)
        return  "workflow execution completed"
        
        
