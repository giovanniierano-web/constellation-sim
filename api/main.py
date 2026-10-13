from fastapi import FastAPI
from fastapi.responses import FileResponse
from simulator.simulator import MissionSimulator
from simulator.visualizer import ScheduleVisualizer
import os

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

@app.post("/simulate/plot")
def generate_schedule_plot():
    """Generates and returns a Gantt chart image of the optimized mission schedule."""
    sim = MissionSimulator()
    schedule = sim.run_default_scenario()
    
    plot_filename = "mission_schedule.png"
    ScheduleVisualizer.plot_schedule(schedule, filename=plot_filename)
    
    if os.path.exists(plot_filename):
        return FileResponse(plot_filename, media_type="image/png", filename="mission_schedule.png")
    
    return {"status": "error", "message": "Failed to generate schedule plot."}