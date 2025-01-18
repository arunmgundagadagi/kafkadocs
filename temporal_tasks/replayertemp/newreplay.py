from temporalio.client import Client
import asyncio
from fstflow import ParallelWorkflow
from temporalio.worker import Replayer
from temporalio.client import WorkflowHistory
from starter import hello

async def main():
    client = await Client.connect("localhost:7233")

    # Fetch the histories of the workflows to be replayed
    workflows = client.list_workflows('WorkflowId="parallel-workflow-001"')
    histories = workflows.map_histories()
    replayer = Replayer(workflows=[ParallelWorkflow])
    results = await replayer.replay_workflows(histories, raise_on_replay_failure=False)
    print(results)
    #client = await hello()YourWorkflowYourWorkflowYoYourWorkflowurWorkflow

    # Create a Replayer instance with your Workflow class
    #replayer = Replayer(
    #    workflows=[ParallelWorkflow]
    #)

    # Fetch the Workflow history
    #history = await client.get_workflow_handle(
    #    "parallel-workflow-001"
    #).fetch_history()

    # Replay the Workflow
     
    #try : 
    #    await replayer.replay_workflow(history)
    #    print("replayed successfully  ")
    #except AttributeError as e:
    #    print("something went wrong please try later")
            
if __name__ == "__main__":
    asyncio.run(main())    
    print("Workflow history fetched successfully.")    
