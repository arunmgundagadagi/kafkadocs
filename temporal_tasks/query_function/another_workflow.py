from temporalio import workflow

@workflow.defn
class GreetingWorkflow:
    def __init__(self):
        self.greeting = "Hello"

    @workflow.query
    def get_greeting(self) -> str:
        return self.greeting

    @workflow.run
    async def run(self, name: str) -> str:
        return f"{self.greeting}, {name}!"