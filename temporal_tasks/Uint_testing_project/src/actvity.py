from temporalio import activity

class SquareActivities:
    @activity.defn
    async def square(self, number: int) -> int:
        return number * number