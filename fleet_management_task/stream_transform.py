import faust
from vehsensorclass import VehicleInfo, SensorData  

# Define Faust application
app = faust.App(
    'vehicle_alerts_app',
    broker='kafka://172.18.0.2:9092',  # Replace with your Kafka broker
    value_serializer='json',
    
)


vehicle_info_topic = app.topic('postgres-jdbc-practice2-vehicle', value_type=VehicleInfo)             # Define input topic for the vehicle info data from postgresql databse
print(f'vehicle_info_topic: {vehicle_info_topic}')                                                 # Define input topic sensor mock data using datagen connector 
sensor_data_topic = app.topic('sensor_json_practice2', value_type=SensorData)


alert_topic = app.topic('vehicle-alerts-topic', value_type=dict)        # Define output topic


vehicle_table = app.Table('postgres-jdbc-practice2-vehicle',partitions=1,                           # Tables for storing vehicle info and joining
                           default=dict)


@app.agent(vehicle_info_topic)
async def process_vehicle_info(records):
    """Process vehicle info data and store it in the table."""
    async for record in records:
        vehicle_id = record.id
        vehicle_table[vehicle_id] = record


@app.agent(sensor_data_topic)
async def process_sensor_data(records):
    """Process sensor data and send alerts if necessary."""
    async for record in records:
        vehicle_id = record.vehicle_id
        temperature = record.engine_temperature
        rotation = record.engine_rotation
        timestamp = record.ts

        # Check if temperature exceeds the threshold
        if temperature > 100:
            # Get vehicle info from the table
            vehicle_info = vehicle_table.get(vehicle_id, {})
            if vehicle_info:
                # Construct the alert message
                alert_message = {
                    "alert": f"Vehicle {vehicle_info.name} ({vehicle_info.registration_number}) "
                             f"has exceeded the temperature threshold.",
                    "vehicle_id": vehicle_id,
                    "temperature": temperature,
                    "rotation": rotation,
                    "timestamp": timestamp,
                    "service_center": "Please proceed to the nearest service center.",
                    "vehicle_info":{
                            "id": vehicle_info.id,
                            "name": vehicle_info.name,
                            "category": vehicle_info.category,
                            "registration_number": vehicle_info.registration_number,
                            "identification_number": vehicle_info.identification_number,
                },
                }

                
                await alert_topic.send( value=alert_message)    # Send alert message to the alert topic        key=str(vehicle_id),


if __name__ == '__main__':
    app.main()
