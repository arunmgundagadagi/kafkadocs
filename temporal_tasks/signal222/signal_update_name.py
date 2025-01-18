from temporalio.client import Client
import asyncio

async def send_signal():
    # Connecting to Temporal server
    client = await Client.connect("localhost:7233")

    # Reference the running workflow
    workflow_id = "greeting-workflow-id"  #we have to uuuse the corect worflow id
    workflow = client.get_workflow_handle(workflow_id)

    #i am Sending a signal to update the name
    new_name = "Arun"
    print(f"Sending signal to update name to: {new_name}")
    await workflow.signal("update_name", new_name)

    print("Signal sent successfully.")

if __name__ == "__main__":
    asyncio.run(send_signal())
