import math

from sgp4.api import Satrec, jday

from datetime import datetime, timedelta


class OrbitalGeometry:

    """Essential orbital visibility calculation at 0° horizon."""

   

    @staticmethod

    def calculate_elevation(satrec: Satrec, time_utc: datetime, station_lat: float, station_lon: float) -> float:

        jd, fr = jday(

            time_utc.year, time_utc.month, time_utc.day,

            time_utc.hour, time_utc.minute, time_utc.second + time_utc.microsecond / 1e6

        )

        error, eci_pos, _ = satrec.sgp4(jd, fr)

        if error != 0:

            return -999.0

           

        x, y, z = eci_pos

        r = math.sqrt(x**2 + y**2 + z**2)

        lat_sat = math.degrees(math.asin(z / r))

       

        gmst = (jd - 2451545.0) * 360.9856473 + 280.4606

        lon_sat = (math.degrees(math.atan2(y, x)) - gmst) % 360

        if lon_sat > 180:

            lon_sat -= 360

           

        lat1, lon1 = math.radians(station_lat), math.radians(station_lon)

        lat2, lon2 = math.radians(lat_sat), math.radians(lon_sat)

       

        dlon = lon2 - lon1

        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

        c = 2 * math.asin(math.sqrt(a))

       

        R_earth = 6371.0

        ground_distance = R_earth * c

       

        max_visible_range = 2500.0

        if ground_distance <= max_visible_range:

            elevation = 90.0 * (1.0 - (ground_distance / max_visible_range))

            return max(0.0, elevation)

           

        return -1.0


    @staticmethod

    def find_passes(satrec: Satrec, start_scan: datetime, end_scan: datetime, station_lat: float, station_lon: float, min_elevation: float = 0.0):

        passes = []

        step = timedelta(minutes=2)

        current_time = start_scan

       

        in_pass = False

        pass_start = None

       

        while current_time <= end_scan:

            elev = OrbitalGeometry.calculate_elevation(satrec, current_time, station_lat, station_lon)

           

            if elev >= min_elevation:

                if not in_pass:

                    in_pass = True

                    pass_start = current_time

            else:

                if in_pass:

                    in_pass = False

                    passes.append((pass_start, current_time))

                   

            current_time += step

           

        if in_pass:

            passes.append((pass_start, end_scan))

           

        return passes 