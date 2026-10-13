from datetime import datetime, timedelta

class Satellite:
    """Represents a constellation satellite."""
    def __init__(self, sat_id: str, altitude_km: float = 550.0):
        self.sat_id = sat_id
        self.altitude_km = altitude_km

class GroundStation:
    """Represents a ground station for downlink/uplink contacts."""
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

class ContactRequest:
    """Represents a communication contact request with a priority level."""
    def __init__(self, sat_id: str, station_name: str, start_time: datetime, duration_minutes: int, priority: int):
        self.sat_id = sat_id
        self.station_name = station_name
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=duration_minutes)
        self.priority = priority  # Higher value means higher priority