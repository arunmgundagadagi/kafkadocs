from temporalio import workflow
import asyncio
from activityparallel import hello
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> list:
        # parallel execution of the activity
        results = await asyncio.gather(
            workflow.execute_activity(hello.process_order,order_id,start_to_close_timeout=timedelta(seconds=5)),
            workflow.execute_activity(hello.delivery_waiting,order_id,start_to_close_timeout=timedelta(seconds=5)),
            workflow.execute_activity(hello.dispatch,order_id,start_to_close_timeout=timedelta(seconds=5)),
            workflow.execute_activity(hello.shipping,order_id,start_to_close_timeout=timedelta(seconds=5))
        )
        
        return results   


        
        
        
    
        
        
