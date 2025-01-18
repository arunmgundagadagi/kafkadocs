import faust
from vehsensorclass import VehicleInfo, SensorData  # Import your custom record classes
import asyncio
from datetime import datetime



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
    default=lambda: {"total_temp": 0, "count": 0},
    partitions=1,
).tumbling(10 * 60)  # tumbling window for 10 minutes

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
        avg_data = avg_temp_table[vehicle_id].now()
        # Update the windowed table for the current vehicle
        # `now()` gets the current state of the window for the vehicle.
        avg_data["total_temp"] += temperature
        avg_data["count"] += 1

        # Write the updated state back to the table
        avg_temp_table[vehicle_id].now().update(avg_data)

        print(f"Updated table for vehicle {vehicle_id}: {avg_data}")
        #else:
        #    avg_data = {"total_temp": temperature, "count": 1}  # Initialize if no data exists
        
        # Ensure that the table gets updated after modifying avg_data
        #avg_temp_table[vehicle_id].now().update(avg_data)
        
        print(f"Updated table for vehicle {vehicle_id}: {avg_data}")

        # After updating the table, calculate the average temperature
        total_temp = avg_data["total_temp"]
        total_count = avg_data["count"]

        if total_count > 0:
            avg_temp = total_temp / total_count
            print(f"Vehicle {vehicle_id} has average temperature: {avg_temp}")

            # Check if the average temperature exceeds the threshold
            if avg_temp > 100:
                # Fetch vehicle info from the vehicle_table
                vehicle_info = vehicle_table.get(vehicle_id, {})
                if vehicle_info:
                    avg_temp_message = {
                        "vehicle_id": vehicle_id,
                        "average_temperature": avg_temp,
                        "timestamp": datetime.now().isoformat(),  # Get the current timestamp
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
                    # Send the alert message to the output topic
                    await avg_temp_topic.send(key=str(vehicle_id), value=avg_temp_message)
                    print(f"Published: {avg_temp_message}")


# Start Faust app
if __name__ == '__main__':
    app.main()
