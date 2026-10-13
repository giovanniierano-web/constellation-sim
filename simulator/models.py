from datetime import datetime, timedelta

class Satellite:
    """Represents a constellation satellite with real TLE orbital parameters."""
    def __init__(self, sat_id: str, tle_line1: str, tle_line2: str):
        self.sat_id = sat_id
        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2

class GroundStation:
    """Represents a ground station with geographic coordinates."""
    def __init__(self, name: str, latitude: float, longitude: float, altitude_m: float = 0.0):
        self.name = name
        self.latitude = latitude      # Degrees
        self.longitude = longitude    # Degrees
        self.altitude_m = altitude_m  # Meters

class ContactRequest:
    """Represents an automated or predicted communication contact request."""
    def __init__(self, sat_id: str, station_name: str, start_time: datetime, duration_minutes: int, priority: int):
        self.sat_id = sat_id
        self.station_name = station_name
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=duration_minutes)
        self.priority = priority