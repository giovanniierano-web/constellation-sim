from simulator.simulator import MissionSimulator

def test_simulator_initialization():
    """Test that MissionSimulator initializes correctly."""
    sim = MissionSimulator()
    assert len(sim.satellites) > 0
    assert sim.satellites[0].sat_id is not None
    assert sim.satellites[0].tle_line1.startswith("1 ")
    assert sim.satellites[0].tle_line2.startswith("2 ")

def test_run_scenario():
    """Test running a full simulation scenario."""
    sim = MissionSimulator()
    schedule = sim.run_default_scenario()
    assert isinstance(schedule, list)