from temporalio import workflow
from datetime import timedelta
import asyncio
from activity111 import activity_one, activity_two

@workflow.defn
class ParallelWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        
        # Start activities in parallel
        results = await asyncio.gather(
            workflow.execute_activity(
                activity_one, name, schedule_to_close_timeout=timedelta(seconds=10)
            ),
            workflow.execute_activity(
                activity_two, name, schedule_to_close_timeout=timedelta(seconds=10)
            )
        )
        # Combine and return results
        return " | ".join(results)