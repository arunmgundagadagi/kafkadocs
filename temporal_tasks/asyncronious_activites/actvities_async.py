#import aiohttp           
import urllib.parse
from temporalio import activity


class TranslateActivities:
    def __init__(self, session):
        self.session = session
        
    @activity.defn
    async def greet_in_spanish(self, name: str) -> str:
        base = f"http://localhost:9999/get-spanish-greeting"
        url = f"{base}?name={urllib.parse.quote(name)}"
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    #@activity.defn
    #async def greet_in_spanish(self, name: str) -> str:
    #    greeting = await self.call_service("get-spanish-greeting", name)
    #    return greeting

    # Utility method for making calls to the microservices
    #async def call_service(self, stem: str, name: str) -> str:
    #    base = f"http://localhost:9999/{stem}"
    #    url = f"{base}?name={urllib.parse.quote(name)}"

    #    async with self.session.get(url) as response:
    #        translation = await response.text()

    #        if response.status >= 400:
     #           raise ApplicationError(                     # type: ignore
      #              f"HTTP Error {response.status}: {translation}",
       #             
        #            non_retryable=response.status < 500,
            

            