import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from datetime import datetime

class ScheduleVisualizer:
    @staticmethod
    def plot_schedule(
        schedule, 
        filename="mission_schedule.png"
    ):
        fig, ax = plt.subplots(figsize=(14, 7))
        if not schedule:
            ax.text(0.5, 0.5, "No scheduled passes available", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes, fontsize=12)
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close(fig)
            return filename

        stations = sorted(list(set(c.station_name if not isinstance(c, dict) else c["station_name"] for c in schedule)))
        station_map = {st: i for i, st in enumerate(stations)}
        satellites = sorted(list(set(c.sat_id if not isinstance(c, dict) else c["sat_id"] for c in schedule)))        
        cmap = plt.get_cmap('tab10')
        sat_colors = {sat: cmap(i % 10) for i, sat in enumerate(satellites)}
        for contact in schedule:
            if isinstance(contact, dict):
                start = datetime.fromisoformat(contact["start_time"])
                end = datetime.fromisoformat(contact["end_time"])
                station = contact["station_name"]
                sat_id = contact["sat_id"]
            else:
                start = contact.start_time
                end = contact.end_time
                station = contact.station_name
                sat_id = contact.sat_id
            y = station_map.get(station, 0)
            duration = end - start
            color = sat_colors.get(sat_id, 'skyblue')            
            ax.barh(y, duration, left=start, height=0.45, alpha=0.7, edgecolor='black', linewidth=0.6, color=color)
        ax.set_yticks(list(station_map.values()))
        ax.set_yticklabels(list(station_map.keys()), fontsize=10, fontweight='bold')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.set_xlabel("Time (UTC)", fontsize=11, fontweight='bold')
        ax.set_ylabel("Ground Stations", fontsize=11, fontweight='bold')
        ax.set_title("Galileo Constellation - Ground Station Visibility Schedule", fontsize=13, fontweight='bold', pad=15)

        legend_elements = [
            Patch(facecolor=sat_colors[sat], edgecolor='black', alpha=0.7, label=sat)
            for sat in satellites
        ]
        ax.legend(handles=legend_elements, title="Satellites", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9, title_fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        fig.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return filename