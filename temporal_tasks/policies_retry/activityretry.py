from temporalio import activity
import logging
logging.basicConfig(filename='error_handling.txt',level=logging.INFO)

@activity.defn
async def correct_id(name: str) -> str:
    print(f"you have entered the name : {name}")
    if name != "Arun123":
        print("not correct ")
        logging.error("accountname is not correct sir")
    else:
        logging.info( f"Hello, {name}! correct_id  you can enter now passwd .")