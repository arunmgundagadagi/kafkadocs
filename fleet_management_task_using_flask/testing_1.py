import faust
from vehsensorclass import VehicleInfo, SensorData  # Import your custom record classes
import asyncio
from datetime import datetime, timedelta
from collections import namedtuple

AvgTempData = namedtuple('AvgTempData', ['total_temp', 'count'])

# Define Faust application
app = faust.App(
    'vehicle_alerts_avg_temp_app',
    broker='kafka://172.18.0.2:9092',  # Replace with your Kafka broker
    value_serializer='json',
)

# Define input and output topics
vehicle_info_topic = app.topic('postgres-jdbc-practice6-vehicle', value_type=VehicleInfo)
sensor_data_topic = app.topic('sensor_json_practice6', value_type=SensorData)
avg_temp_topic = app.topic('vehicle-avg-temp-topic', value_type=dict, partitions=1)

# Define tables
vehicle_table = app.Table(
    'postgres-jdbc-practice6-vehicle',
    partitions=1,
    default=dict,
)

avg_temp_table = app.Table(
    'vehicle_avg_temp_table',
    default=lambda: AvgTempData(total_temp=0.0, count=0),
    partitions=1,
).tumbling(60, expires=timedelta(minutes=10))  # tumbling window for 10 minutes

# Process vehicle info data and store it in the table
@app.agent(vehicle_info_topic)
async def process_vehicle_info(records):
    async for record in records:
        vehicle_id = record.id
        vehicle_table[vehicle_id] = record



# Process sensor data and update average temperature table
@app.agent(sensor_data_topic)
async def process_sensor_data(records):
    async for record in records:
        vehicle_id = record.vehicle_id
        temperature = record.engine_temperature
        window_set = avg_temp_table[vehicle_id]

        # Access the current window in the WindowSet
        current_window = window_set.now()  # Retrieves the current tumbling window

        # Check if the current window already has data
        if current_window is None or not isinstance(current_window, AvgTempData):
            current_window = AvgTempData(total_temp=0.0, count=0)

        # Update the average temperature data
        updated_data = AvgTempData(
            total_temp=current_window.total_temp + temperature,  # Add the new temperature to total
            count=current_window.count + 1  # Increment the count of temperature readings
        )

        # Store the updated data back in the table for the current window
        avg_temp_table[vehicle_id].now()  # Access the current window explicitly
        avg_temp_table[vehicle_id] = updated_data  
        print(f"Updated table for vehicle {vehicle_id}: {updated_data}")
        # Send alert if temperature exceeds threshold
        
        #print(f"Updated table for vehicle {vehicle_id}:")
        #else:
        #    avg_data = {"total_temp": temperature, "count": 1}  # Initialize if no data exists
        
        # Ensure that the table gets updated after modifying avg_data
        #avg_temp_table[vehicle_id].now().update(avg_data)
        
        #print(f"Updated table for vehicle {vehicle_id}: {avg_data}")

        # After updating the table, calculate the average temptotal_temp = avg_data["total_temp"]
        #total_count = avg_data["count"]

@app.timer(10.0, on_leader=True)  # every 10 minutes
async def check_and_publish_avg_temp():
    for vehicle_id in avg_temp_table.keys():
        # Access the window set for the vehicle_id
        window_set = avg_temp_table[vehicle_id].now()  # Ensure you're accessing the current window

        # Iterate over windows in the window set
        for timestamp, avg_data in window_set.items():
            # Safely access total_temp and count attributes
            total_temp = getattr(avg_data, 'total_temp', 0.0)
            count = getattr(avg_data, 'count', 0)                                 
                                                    # for vehicle_id, window in avg_temp_table.items():
                                                    #print(f"{vehicle_id}, {avg_temp_table}")
                                                    #print("window table has data")
                                                #for timestamp, avg_data in window.items():                                   
                                                    #total_temp = avg_data["total_temp"]
                                                    #count = avg_data["count"]

            if count > 0:
                avg_temp = total_temp / count
                if avg_temp > 100:
                    vehicle_info = vehicle_table.get(vehicle_id, {})
                    if vehicle_info: 
                        avg_temp_message = {
                            "vehicle_id": vehicle_id,
                            "average_temperature": avg_temp,
                            "timestamp": timestamp,
                            "message": f"Vehicle {vehicle_info.name} ({vehicle_info.registration_number}) "
                                       f"has an average temperature of {avg_temp}°C over the last 10 minutes, exceeding the threshold.",
                            "vehicle_info": {
                                "id": vehicle_info.id,
                                "name": vehicle_info.name,
                                "category": vehicle_info.category,
                                "registration_number": vehicle_info.registration_number,
                                "identification_number": vehicle_info.identification_number,
                            },
                        }
                        await avg_temp_topic.send(key=str(vehicle_id),value=avg_temp_message)
                        print(f"Published: {avg_temp_message}")
            else:
                print(f"No data for window at {timestamp} for vehicle_id={vehicle_id}")


# Start Faust app
if __name__ == '__main__':
    app.main()
