import faust
from vehsensorclass import VehicleInfo, SensorData
from datetime import timedelta
from collections import namedtuple 

AvgTempData = namedtuple('AvgTempData', ['total_temp', 'count'])

                        # herre we are defining faust application for to process stream data 
app = faust.App(
    'vehicle_alerts_avg_temp_app',
    broker='kafka://172.18.0.2:9092',  # Replace with your Kafka broker
    value_serializer='json',
)

#  
vehicle_info_topic = app.topic('postgres-jdbc-demo-vehicle', value_type=VehicleInfo)       #this is the vehicle information topic records are from postgresql 
sensor_data_topic = app.topic('sensor_json_demo', value_type=SensorData)                   #this is the sensor data from datagen connector 
avg_temp_topic = app.topic('vehicle-avg-temp-topic', value_type=dict, partitions=1)             #this is last topic we need to send alert messages to the topic 

# creating the vehicle information table 
vehicle_table = app.Table(
    'postgres-jdbc-practice6-vehicle',
    partitions=1,
    default=dict,
)

#
avg_temp_table = app.Table(
    'vehicle_avg_temp_table',
    default=lambda: AvgTempData(total_temp=0.0, count=0),    
    partitions=1,
).tumbling(60, expires=timedelta(minutes=10))  # ######        tumbling window for 10 minutes total time and creating 60 seconds windows to calculate the average temprature 

vehicle_avg_data = {}

# Process vehicle info data and store it in the table
@app.agent(vehicle_info_topic)
async def process_vehicle_info(records):
    async for record in records:
        vehicle_id = record.id
        vehicle_table[vehicle_id] = record 

# appagent is wrapper fucntioon to processes the streams of ddata by subscribing it 
@app.agent(sensor_data_topic)
async def process_sensor_data(records):
    async for record in records:
        vehicle_id = record.vehicle_id
        temperature = record.engine_temperature
        window_set = avg_temp_table[vehicle_id]

        # Access the current window in the WindowSet
        current_window = window_set.now()  # assign teh current   tumbling window record for vehicle id 

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
        vehicle_avg_data[vehicle_id] = updated_data
        

                                                #timer function to calculate the average temperature for each vehicle every 60 seconds
@app.timer(60.0, on_leader=True)  # every 10 seconds
async def check_and_publish_avg_temp():
    for vehicle_id, avg_data in vehicle_avg_data.items():
        total_temp = avg_data.total_temp
        count = avg_data.count
        
        if count > 0:
            avg_temp = total_temp / count
            print(f"Vehicle {vehicle_id} has an average temperature of {avg_temp:.2f}°C")

            if avg_temp > 100:
                vehicle_info = vehicle_table.get(vehicle_id, {})
                if vehicle_info: 
                    avg_temp_message = {
                        "vehicle_id": vehicle_id,
                        "average_temperature": avg_temp,
                        "message": f"Vehicle {vehicle_info.name} ({vehicle_info.registration_number}) "
                                   f"has an average temperature of {avg_temp}°C over the last 1 minutes, exceeding the threshold.",
                        "vehicle_info": {
                            "id": vehicle_info.id,
                            "name": vehicle_info.name,
                            "category": vehicle_info.category,
                            "registration_number": vehicle_info.registration_number,
                            "identification_number": vehicle_info.identification_number,
                        },
                    }
                    await avg_temp_topic.send(key=str(vehicle_id), value=avg_temp_message)
                    print(f"Published: {avg_temp_message}")
        else:
            print(f"No data available for vehicle {vehicle_id}.")

# Start Faust app
if __name__ == '__main__':
    app.main()
