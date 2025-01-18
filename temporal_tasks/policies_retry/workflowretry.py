from temporalio import workflow
from temporalio.common import RetryPolicy
from activityretry import correct_id
from datetime import timedelta

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, name: str):
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=12),    # this is the delay to start the our fst retry 
            backoff_coefficient=2.0,            # here every retry delay will be multiplied by this number to set the next retry delay
            maximum_attempts=3,           # maximum number of retries  set to retry  here 3 attempts we have set 
            maximum_interval=timedelta(seconds=50),
        )
        
        try:
            result = await workflow.execute_activity(
                correct_id,
                name,
                start_to_close_timeout=timedelta(seconds=50),          #THIS IS WORKFLOW EXECUTION TIME START TO CLOSE TIME
                schedule_to_close_timeout=timedelta(seconds=60),       #this is whole from scheduling time to closing time of activity task execution (this shoud always grater than the start to close or just littele bit greater than ) 
                retry_policy=retry_policy,    
            )
            return f"Workflow completed: {result}"
        except Exception as e:
            return f"Workflow failed after retries: {str(e)}"
