import faust
from alertmesgformat import AlertMessage #type:ignore 

# Define Faust application
app = faust.App(
    'vehicle_avg_temp_app',
    broker='kafka://172.18.0.2:9092',  
    value_serializer='json',
)

# Defining topics
alert_topic = app.topic('vehicle-alerts-topic', value_type=AlertMessage, internal=True)  # input topic
avg_temp_topic = app.topic('vehicle-avg-temp-topic', value_type=dict, internal=True)  # output topic

#define windowed table for calculate avg tempr
avg_temp_table = app.Table(
    'vehicle_avg_temp_table',
    default=lambda: {"total_temp": 0, "count": 0},
    partitions=1,
).tumbling(10 * 6)  # tumbling window 

@app.agent(alert_topic)
async def process_alert_records(records):
    """Process alert topic records and calculate average temperature."""
    async for record in records:
        vehicle_id = record.vehicle_id
        temperature = record.temperature

        # update windowed table for the current vehicle
        avg_data = avg_temp_table[vehicle_id].now()
        avg_data["total_temp"] += temperature 
        avg_data["count"] += 1
        avg_temp_table[vehicle_id].now().update(avg_data)  # saving it back to the table

@app.timer(interval=600.0)  # every 10 minutes
async def check_and_publish_avg_temp():
    """Check average temperatures and publish to a new topic if above threshold."""
    for vehicle_id, window in avg_temp_table.items():
        for timestamp, avg_data in window.items():
            total_temp = avg_data["total_temp"]
            count = avg_data["count"]

            if count > 0:
                avg_temp = total_temp / count
                if avg_temp > 100:
                    # Create message for the output topic
                    avg_temp_message = {
                        "vehicle_id": vehicle_id,
                        "average_temperature": avg_temp,
                        "timestamp": timestamp,
                        "message": f"Vehicle {vehicle_id} has an average temperature of {avg_temp}°C over the last 10 minutes, exceeding the threshold.",
                    }

                    # Send to the output topic
                    await avg_temp_topic.send(value=avg_temp_message)
                    print(f"Published: {avg_temp_message}")

if __name__ == '__main__':
    app.main()