import requests

from simulator.models import Satellite


class GalileoClient:

    """Fetches real-time orbital elements (TLE) for the Galileo constellation from CelesTrak using TLE format."""

   

    CELESTRAK_GALILEO_TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=galileo&FORMAT=tle"


    @classmethod

    def fetch_galileo_satellites(cls, limit: int = 5) -> list[Satellite]:

        """Downloads real Galileo TLE text data and parses it into Satellite objects."""

        try:

            headers = {

                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MissionSimulator/1.0"

            }

            response = requests.get(cls.CELESTRAK_GALILEO_TLE_URL, headers=headers, timeout=10)

            response.raise_for_status()

           

            lines = [line.strip() for line in response.text.splitlines() if line.strip()]

           

            satellites = []

            # CelesTrak TLE format returns blocks of 3 lines: Name, Line 1, Line 2

            for i in range(0, len(lines) - 2, 3):

                if len(satellites) >= limit:

                    break

               

                sat_name = lines[i]

                tle1 = lines[i+1]

                tle2 = lines[i+2]

               

                # Basic validation that lines start with 1 and 2

                if tle1.startswith("1 ") and tle2.startswith("2 "):

                    satellites.append(Satellite(sat_id=sat_name, tle_line1=tle1, tle_line2=tle2))

           

            if not satellites:

                raise ValueError("No valid TLE 3-line blocks parsed from CelesTrak response.")

               

            return satellites

           

        except Exception as e:

            print(f"[WARNING] Failed to fetch real Galileo data ({e}). Falling back to mock operational satellite.")

            fallback_tle1 = "1 40130U 14048A   26100.50000000  .00000000  00000-0  00000-0 0    05"

            fallback_tle2 = "2 40130  55.0000 120.0000 0001000   0.0000   0.0000 15.00000000    05"

            return [Satellite(sat_id="GALILEO-FALLBACK", tle_line1=fallback_tle1, tle_line2=fallback_tle2)] 