import faust

class VehicleInfo(faust.Record, serializer='json'):
    id: int
    created: int
    modified: int
    name: str
    category: str
    registration_number: str
    identification_number: str

class SensorData(faust.Record, serializer='json'):
    vehicle_id: int
    engine_temperature: int
    engine_rotation: int
    ts: int