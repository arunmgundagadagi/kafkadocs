import concurrent.futures
import asyncio
import aiohttp
from temporalio.client import Client
from temporalio.worker import Worker

from actvities_async import TranslateActivities # type: ignore
from workflow_async import GreetSomeone         # type: ignore


async def main():
    client = await Client.connect("localhost:7233", namespace="default")

    # Run the workernc wh aioit
    async with aiohttp.ClientSession() as session:
        activities = TranslateActivities(session)

    
        worker = Worker(
            client,
            task_queue="greeting-tasks",
            workflows=[GreetSomeone],
            activities=[TranslateActivities(session).greet_in_spanish],
            
        )
        print("Starting the worker....")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())