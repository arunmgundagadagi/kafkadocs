import concurrent.futures
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activites_sync import TranslateActivities # type: ignore
from workflow_sync import GreetSomeone         # type: ignore


async def main():
    client = await Client.connect("localhost:7233", namespace="default")

    # running the worker
    activities = TranslateActivities()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue="greeting-tasks",
            workflows=[GreetSomeone],
            activities=[activities.greet_in_spanish],
            activity_executor=activity_executor,
        )
        print("Starting the worker....")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())