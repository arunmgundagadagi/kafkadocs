from temporalio import workflow
import asyncio
@workflow.defn
class GreetSomeone():
    @workflow.run
    async def run(self, name:str) -> str:
        await asyncio.sleep(10)                         #this is added
        return f"Hello {name}!"
