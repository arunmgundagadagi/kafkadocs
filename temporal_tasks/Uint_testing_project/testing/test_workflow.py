import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from src.workflow import SumOfSquaresWorkflow
from src.actvity import SquareActivities

@pytest.mark.asyncio
async def test_sum_of_squares_positive():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        activities = SquareActivities()
        async with Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[SumOfSquaresWorkflow],
            activities=[activities.square],
        ):
            result = await env.client.execute_workflow(
                SumOfSquaresWorkflow.calculate_sum_of_squares,
                5,
                6,
                id="test-sum-of-squares",
                task_queue="test-math-queue",
            )

            assert 61 == result

@pytest.mark.asyncio
async def test_sum_of_squares_negative():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        activities = SquareActivities()
        async with Worker(
            env.client,
            task_queue="test-math-queue",
            workflows=[SumOfSquaresWorkflow],
            activities=[activities.square],
        ):
            result = await env.client.execute_workflow(
                SumOfSquaresWorkflow.calculate_sum_of_squares,
                5,
                -9,
                id="test-sum-of-squares",
                task_queue="test-math-queue",
            )

            assert 106 == result
