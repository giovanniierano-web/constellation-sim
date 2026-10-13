from datetime import datetime, timedelta
from simulator.models import Satellite, GroundStation, ContactRequest
from simulator.scheduler import MissionScheduler

class MissionSimulator:
    """Coordinates satellites, ground stations, and the scheduler for a scenario."""
    def __init__(self):
        self.satellites = [Satellite("SAT-01"), Satellite("SAT-02"), Satellite("SAT-03")]
        self.ground_stations = [
            GroundStation("Station_North", 48.1351, 11.5820),
            GroundStation("Station_South", -35.2809, 149.1300)
        ]
        self.scheduler = MissionScheduler(self.ground_stations)

    def run_default_scenario(self):
        base_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        # Adding sample requests (including overlapping/conflicting ones)
        self.scheduler.add_request(ContactRequest("SAT-01", "Station_North", base_time, 15, priority=1))
        self.scheduler.add_request(ContactRequest("SAT-02", "Station_North", base_time + timedelta(minutes=5), 10, priority=5))
        self.scheduler.add_request(ContactRequest("SAT-03", "Station_South", base_time, 20, priority=2))
        
        return self.scheduler.optimize_schedule()