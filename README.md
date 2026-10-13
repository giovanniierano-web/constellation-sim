# Galileo Constellation Simulator API

An industrial-grade satellite constellation simulator designed to compute realistic, variable-length orbital passes and visualize overlapping ground station contacts.

---

## 🛰️ Core Pipeline & Architecture

The system calculates line-of-sight passes by executing a strict sequence of spatial propagation, geographic mapping, and geometric thresholding:

1. **Spatial Propagation (SGP4 & TLE)**
   * **Input:** Real-time satellite **TLE (Two-Line Elements)** fetched from CelesTrak.
   * **Execution:** Utilizes the industry-standard `sgp4` library to propagate orbital elements over a 24-hour window.
   * **Output:** Instantaneous 3D Cartesian coordinates in **ECI (Earth-Centered Inertial)** format $(x, y, z)$ relative to the Earth's center.

2. **Geographic Mapping (GMST & Rotation)**
   * **Challenge:** Inertial ECI coordinates must account for the Earth's continuous rotation.
   * **Execution:** Combines satellite equatorial height with **GMST (Greenwich Mean Sidereal Time)** to calculate precise terrestrial coordinates $(\text{lat}, \text{lon})$ of the sub-satellite point.

3. **Visibility & Footprint Threshold ($0^\circ$ Horizon)**
   * **Execution:** Computes the **great-circle distance** along the Earth's spherical curvature between the ground station and the satellite's surface projection.
   * **Rule:** If the distance $\le 2500\text{ km}$ (the MEO coverage footprint radius), the satellite is within direct line-of-sight ($\ge 0^\circ$ elevation).

4. **Pass Detection (AOS / LOS)**
   * **AOS (Acquisition of Signal):** The precise timestamp when surface distance drops below $2500\text{ km}$ (satellite rises above the $0^\circ$ horizon).
   * **LOS (Loss of Signal):** The timestamp when surface distance exceeds $2500\text{ km}$ (satellite sets below the horizon).
   * **Output:** True variable-length contact windows.

---

## 📖 Technical Glossary & Interview Key Terms

* **TLE (Two-Line Elements):** Standard data format encoding orbital elements of an Earth-orbiting object.
* **SGP4 (Simplified General Perturbations v4):** Analytical orbit propagation model used to predict satellite positions.
* **ECI (Earth-Centered Inertial):** 3D Cartesian coordinate system fixed relative to the stars, centered at Earth's center of mass.
* **GMST (Greenwich Mean Sidereal Time):** Measure of Earth's rotation angle used to translate inertial coordinates into geographic locations.
* **Footprint:** Maximum surface area within direct line-of-sight (~$2500\text{ km}$ radius for MEO Galileo satellites).
* **AOS / LOS:** Acquisition of Signal / Loss of Signal, defining the temporal boundaries of a contact pass.
* **Great-circle distance (Distanza ortodromica):** The shortest path between two points along the surface of a sphere.

---

## 🛠️ Stack & Endpoints

* **Backend Framework:** FastAPI (Python 3.11+)
* **Data Validation:** Pydantic
* **Orbital Engine:** `sgp4`
* **Visualization:** `matplotlib` (Gantt charts rendered with 50% opacity `alpha=0.5` to clearly highlight concurrent contact overlaps).

### API Endpoints
* `POST /simulate` : Executes the 24-hour constellation simulation and returns the schedule of geometrically computed passes in JSON format.
* `GET /chart` : Generates and streams the Gantt chart visualization (`PNG`) reflecting active contact schedules.

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python main.py
```
* Access Swagger Documentation: `http://localhost:8000/docs`