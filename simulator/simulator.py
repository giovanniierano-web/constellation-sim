from datetime import datetime, timedelta

from sgp4.api import Satrec

from simulator.galileo_client import GalileoClient

from simulator.models import GroundStation, ContactRequest

from simulator.config_loader import ConfigLoader

from simulator.geometry import OrbitalGeometry


class MissionSimulator:

    """Essential mission simulator using direct 0° horizon pass detection."""

   

    AVAILABLE_STATIONS = {

        "Station_North": GroundStation(name="Station_North", lat=48.1351, lon=11.5820),

        "Station_South": GroundStation(name="Station_South", lat=-35.2809, lon=149.1300)

    }


    def __init__(self, config_path: str = "config.json"):

        self.config = ConfigLoader.load_config(config_path)

       

        satellite_limit = self.config.get("satellite_limit", 5)

        station_names = self.config.get("stations", ["Station_North", "Station_South"])

       

        self.satellites = GalileoClient.fetch_galileo_satellites(limit=satellite_limit)

       

        self.ground_stations = [

            self.AVAILABLE_STATIONS[name] for name in station_names if name in self.AVAILABLE_STATIONS

        ]

       

        if not self.ground_stations:

            raise ValueError("No valid ground stations configured.")


    def run_default_scenario(self):

        scan_start = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

        scan_end = scan_start + timedelta(hours=24)

       

        schedule = []

        station_count = len(self.ground_stations)

       

        for i, sat in enumerate(self.satellites):

            satrec = Satrec.twoline2rv(sat.tle_line1, sat.tle_line2)

            target_station = self.ground_stations[i % station_count]

           

            # Cerca direttamente i passaggi a soglia 0° (orizzonte)

            passes = OrbitalGeometry.find_passes(

                satrec, scan_start, scan_end, target_station.lat, target_station.lon, min_elevation=0.0

            )

           

            if passes:

                aos, los = passes[0]

                duration_mins = int((los - aos).total_seconds() / 60)

            else:

                aos = scan_start + timedelta(hours=i * 1.5)

                duration_mins = 15

               

            duration_mins = max(5, min(duration_mins, 60))

           

            schedule.append(

                ContactRequest(

                    sat_id=sat.sat_id,

                    station_name=target_station.name,

                    start_time=aos,

                    duration_minutes=duration_mins,

                    priority=(i % 5) + 1

                )

            )


        schedule.sort(key=lambda x: x.start_time)

        return schedule 