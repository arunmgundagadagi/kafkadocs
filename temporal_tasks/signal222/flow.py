from temporalio import workflow
from datetime import timedelta
import asyncio

@workflow.defn
class GreetingWorkflow:
    def __init__(self):
        self.name = "platformatory"

    @workflow.run
    async def run(self):
        #while True:
        await asyncio.sleep(5)
        while True:
            await asyncio.sleep(2)
            print(f"Greeting: Hello, {self.name}!")
            

    @workflow.signal
    async def update_name(self, new_name: str):
        self.name = new_name
        print(f"Signal received. Updated name to: {self.name}")
