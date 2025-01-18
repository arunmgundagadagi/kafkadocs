import asyncio
import sys
from workflow import GreetSomeone
from temporalio.client import Client

import temporalio.converter
import dataclasses
from codec import CompressionCodec
async def main():
    
    client = await Client.connect("localhost:7233",
            data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=CompressionCodec(),
            failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes,
        ),      )
    handle = await client.start_workflow(
        GreetSomeone.run,
        sys.argv[1],
        id="greeting-workflow",
        task_queue="greeting-tasks",
    )
    print(f"Started workflow. Workflow ID: {handle.id}, RunID {handle.result_run_id}")
    result = await handle.result()
    print(f"Result: {result}")
if __name__ == "__main__":
    asyncio.run(main())

