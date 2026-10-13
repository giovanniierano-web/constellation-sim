from datetime import datetime, timedelta
from simulator.models import GroundStation, ContactRequest
from simulator.scheduler import MissionScheduler

def test_scheduler_priority_and_conflicts():
    """
    Test that higher priority requests correctly override 
    or reject overlapping lower priority requests.
    """
    gs_list = [GroundStation("Station_North", 48.1351, 11.5820)]
    scheduler = MissionScheduler(gs_list)
    
    base_time = datetime(2026, 10, 13, 10, 0, 0)
    
    req1 = ContactRequest("GALILEO-01", "Station_North", base_time, 15, priority=1)
    req2 = ContactRequest("GALILEO-02", "Station_North", base_time + timedelta(minutes=5), 10, priority=5)
    
    scheduler.add_request(req1)
    scheduler.add_request(req2)
    
    schedule = scheduler.optimize_schedule()
    
    assert len(schedule) == 1
    assert schedule[0].sat_id == "GALILEO-02"
    assert schedule[0].priority == 5