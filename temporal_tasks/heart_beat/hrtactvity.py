from temporalio import activity
import asyncio
import json

@activity.defn
async def enumerating_bigdata(start_id: int, count: int) -> list:
    try:
        with open('/home/charan/temporal_tasks/heart_beat/first_names.json', 'r') as f:
            first_names = json.load(f)
        name_list = list(first_names.keys())
        end_id = start_id + count 
        result = []
        for i in range(start_id,end_id):
            
            result.append({"id": i, "name": name_list[i]})
            
            activity.heartbeat("this is heartbeat")
            
            print(f"this is heartnbeat of current_id: {i}, progress: {len(result)}")
            await asyncio.sleep(0)
            
        return result   

    except Exception as e:
        raise Exception(f"An error occurred while fetching names: {e}")