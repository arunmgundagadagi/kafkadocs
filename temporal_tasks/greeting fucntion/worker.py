import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import GreetSomeone
import temporalio.converter
import dataclasses
from codec import CompressionCodec
async def main():
    client = await Client.connect("localhost:7233", namespace="default",
            data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=CompressionCodec(),
            failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes,
        ),)
    # Run the worker
    worker = Worker(client, task_queue="greeting-tasks", workflows=[GreetSomeone])
    await worker.run()
if __name__ == "__main__":
    asyncio.run(main())
