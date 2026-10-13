from fastapi import FastAPI
from simulator.simulator import MissionSimulator

app = FastAPI(title="Constellation Mission Control API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Constellation Simulation and Planning API"}

@app.post("/simulate")
def run_simulation():
    sim = MissionSimulator()
    schedule = sim.run_default_scenario()
    
    result = [
        {
            "satellite": r.sat_id,
            "station": r.station_name,
            "start_time": r.start_time.isoformat(),
            "end_time": r.end_time.isoformat(),
            "priority": r.priority
        }
        for r in schedule
    ]
    
    return {
        "status": "success",
        "scheduled_contacts_count": len(result),
        "schedule": result
    }