from temporalio import workflow
from actvity import SquareActivities
from datetime import timedelta
@workflow.defn
class SumOfSquaresWorkflow:
    @workflow.run
    async def calculate_sum_of_squares(self, first: int, second: int) -> int:

        square_one = await workflow.execute_activity_method(
            SquareActivities.square,
            first,
            start_to_close_timeout=timedelta(seconds=5),
        )

        square_two = await workflow.execute_activity_method(
            SquareActivities.square,
            second,
            start_to_close_timeout=timedelta(seconds=5),
        )

        return square_one + square_two