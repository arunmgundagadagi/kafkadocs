from faust import Record

class AlertMessage(Record, serializer='json'):
    alert: str
    vehicle_id: int
    temperature: float
    rotation: float
    timestamp: int
    service_center: str
    vehicle_info: dict