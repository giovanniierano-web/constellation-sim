from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint of the API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Constellation Simulation and Planning API"}

def test_run_simulation():
    """Test the simulation endpoint using real/fallback TLE data and verify JSON structure."""
    response = client.post("/simulate")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "scheduled_contacts_count" in data
    assert "schedule" in data
    assert isinstance(data["schedule"], list)
    
    # If the simulation generated contacts, check their structure
    if data["scheduled_contacts_count"] > 0:
        first_contact = data["schedule"][0]
        assert "satellite" in first_contact
        assert "station" in first_contact
        assert "start_time" in first_contact
        assert "end_time" in first_contact
        assert "priority" in first_contact