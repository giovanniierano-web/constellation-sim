from pydantic import BaseModel

from datetime import datetime


class GroundStation(BaseModel):

    name: str

    lat: float

    lon: float


class SatelliteData(BaseModel):

    sat_id: str

    tle_line1: str

    tle_line2: str


# Alias per compatibilità con GalileoClient

Satellite = SatelliteData


class ContactRequest(BaseModel):

    sat_id: str

    station_name: str

    start_time: datetime

    end_time: datetime

    priority: int


    def __init__(self, **data):

        if "duration_minutes" in data and "end_time" not in data and "start_time" in data:

            from datetime import timedelta

            data["end_time"] = data["start_time"] + timedelta(minutes=data.pop("duration_minutes"))

        super().__init__(**data) 