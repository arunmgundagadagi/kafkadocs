from temporalio import activity
import asyncio

# Define the first activity
@activity.defn
async def activity_one(name: str) -> str:
    await asyncio.sleep(5)  # Simulate some delay
    return f"Hello from Activity One, {name}!"

# Define the second activity
@activity.defn
async def activity_two(name: str) -> str:
    await asyncio.sleep(5)  # Simulate some delay
    return f"Hello from Activity Two, {name}!"