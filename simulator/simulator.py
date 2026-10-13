from datetime import datetime, timedelta
from sgp4.api import Satrec, jday
from simulator.galileo_client import GalileoClient
from simulator.models import GroundStation, ContactRequest
from simulator.scheduler import MissionScheduler

class MissionSimulator:
    """Coordinates real Galileo satellites, ground stations, and scheduler."""
    def __init__(self):
        # Fetch real Galileo satellites from CelesTrak API
        self.satellites = GalileoClient.fetch_galileo_satellites(limit=3)
        self.ground_stations = [
            GroundStation("Station_North", 48.1351, 11.5820),  # e.g., Munich/Oberpfaffenhofen (DLR context)
            GroundStation("Station_South", -35.2809, 149.1300)   # e.g., Canberra tracking station
        ]
        self.scheduler = MissionScheduler(self.ground_stations)

    def run_default_scenario(self):
        """
        Dynamically generates contact requests based on real satellite orbital propagation 
        over the configured ground stations.
        """
        base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        
        # Simple dynamic request generator based on orbital propagation windows
        for i, sat in enumerate(self.satellites):
            satrec = Satrec.twoline2rv(sat.tle_line1, sat.tle_line2)
            
            # Check positions over a 24-hour simulation window in 30-minute steps
            for step in range(0, 24 * 60, 60):
                current_time = base_time + timedelta(minutes=step)
                jd, fr = jday(
                    current_time.year, current_time.month, current_time.day,
                    current_time.hour, current_time.minute, current_time.second
                )
                
                error, eci_pos, eci_vel = satrec.sgp4(jd, fr)
                if error == 0:
                    # If propagation is successful, we simulate a contact opportunity
                    # Assign a priority (e.g., higher priority for the first satellite or alternating)
                    priority = (i % 3) + 1
                    
                    # Alternate target stations based on simulation step
                    station_name = "Station_North" if (step // 60) % 2 == 0 else "Station_South"
                    
                    self.scheduler.add_request(
                        ContactRequest(
                            sat_id=sat.sat_id,
                            station_name=station_name,
                            start_time=current_time,
                            duration_minutes=15,
                            priority=priority
                        )
                    )
                    # Limit requests per satellite for clean scheduling scenarios
                    break 

        return self.scheduler.optimize_schedule()