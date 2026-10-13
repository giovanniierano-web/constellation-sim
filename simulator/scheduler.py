from datetime import datetime
from simulator.models import ContactRequest

class MissionScheduler:
    """Manages ground station resource allocation and conflict resolution."""
    def __init__(self, ground_stations):
        self.ground_stations = {gs.name: gs for gs in ground_stations}
        self.requests = []

    def add_request(self, request: ContactRequest):
        self.requests.append(request)

    def optimize_schedule(self):
        """
        Greedy scheduling algorithm based on priority to resolve resource conflicts.
        """
        sorted_requests = sorted(self.requests, key=lambda x: (-x.priority, x.start_time))
        accepted_schedule = []
        station_busy_until = {name: datetime.min for name in self.ground_stations}

        for req in sorted_requests:
            station = req.station_name
            if req.start_time >= station_busy_until[station]:
                accepted_schedule.append(req)
                station_busy_until[station] = req.end_time
            else:
                print(f"[CONFLICT] Resource busy: unable to schedule {req.sat_id} on {station}")

        return accepted_schedule