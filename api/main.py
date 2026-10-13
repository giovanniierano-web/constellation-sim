from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from simulator.simulator import MissionSimulator
from simulator.visualizer import ScheduleVisualizer
import traceback
import os

app = FastAPI(
    title="Galileo Constellation Simulator API",
    description="Industrial-grade Galileo constellation and ground station contact scheduler.",
    version="2.0"
)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>Galileo Constellation Simulator</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🛰️ Galileo Constellation Simulator API</h1>
            <p>Welcome to the mission scheduling simulator API.</p>
            <ul>
                <li><a href="/docs">Swagger API Documentation (/docs)</a></li>
                <li><a href="/chart">View Mission Schedule Gantt Chart (/chart)</a></li>
            </ul>
        </body>
    </html>
    """

@app.post("/simulate")
def run_simulation():
    try:
        simulator = MissionSimulator()
        schedule = simulator.run_default_scenario()
        
        # Genera il diagramma di Gantt con le durate effettive
        visualizer = ScheduleVisualizer()
        visualizer.plot_schedule(schedule, filename="mission_schedule.png")
        
        return {
            "status": "success",
            "scheduled_contacts_count": len(schedule),
            "config_used": simulator.config,
            "schedule": schedule
        }
    except Exception as e:
        # Stampa l'errore completo nel terminale per il debug immediato
        print("\n--- ERROR DURING SIMULATION ---")
        traceback.print_exc()
        print("-------------------------------\n")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/chart", response_class=FileResponse)
def get_chart():
    chart_path = "mission_schedule.png"
    if not os.path.exists(chart_path):
        # Se non esiste ancora, prova a generarla al volo
        try:
            simulator = MissionSimulator()
            schedule = simulator.run_default_scenario()
            ScheduleVisualizer.plot_schedule(schedule, filename=chart_path)
        except Exception:
            raise HTTPException(status_code=404, detail="Schedule chart not found. Run POST /simulate first.")
            
    return FileResponse(chart_path, media_type="image/png", filename="mission_schedule.png")