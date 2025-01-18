from temporalio import workflow
from hrtactvity import enumerating_bigdata
from datetime import timedelta
@workflow.defn
class FetchNamesWorkflow:
    @workflow.run
    async def run(self, start_id: int, count: int) -> list:
        """
        Workflow that executes the get_names activity.
        """
        return await workflow.execute_activity(
            enumerating_bigdata,
            args=(start_id, count),
            start_to_close_timeout=timedelta(minutes=10),  # Timeout for the activity execution
            heartbeat_timeout=timedelta(seconds=11),
        )