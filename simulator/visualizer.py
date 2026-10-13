import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
import os

class ScheduleVisualizer:
    """Generates professional Gantt charts with transparent overlapping contact bars."""
    
    @staticmethod
    def plot_schedule(schedule, filename="mission_schedule.png"):
        if not schedule:
            print("[INFO] No scheduled contacts to plot.")
            return None
            
        try:
            fig, ax = plt.subplots(figsize=(14, 8))
            
            stations = list(set(item.station_name for item in schedule))
            station_y_map = {station: i for i, station in enumerate(stations)}
            
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                      '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
                      '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']
            
            ax.set_yticks(list(station_y_map.values()))
            ax.set_yticklabels(list(station_y_map.keys()), fontweight='bold', fontsize=11)
            
            all_starts = [item.start_time for item in schedule]
            all_ends = [item.end_time for item in schedule]
            
            for idx, item in enumerate(schedule):
                y_pos = station_y_map.get(item.station_name, 0)
                start = item.start_time
                end = item.end_time
                
                duration_days = (end - start).total_seconds() / 86400.0
                start_num = mdates.date2num(start)
                
                ax.barh(
                    y_pos, 
                    duration_days, 
                    left=start_num, 
                    height=0.35,
                    color=colors[idx % len(colors)],
                    edgecolor='black',
                    linewidth=1.2,
                    alpha=0.5,  # Trasparenza al 50% per evidenziare le sovrapposizioni
                    label=item.sat_id
                )
                
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
            
            fig.autofmt_xdate(rotation=45)
            ax.set_xlabel("Time (UTC)", fontweight='bold', fontsize=11)
            ax.set_ylabel("Ground Stations", fontweight='bold', fontsize=11)
            ax.set_title("Galileo Constellation - Ground Station Contacts Schedule", fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, linestyle='--', alpha=0.3)
            
            if all_starts and all_ends:
                ax.set_xlim(mdates.date2num(min(all_starts) - timedelta(hours=1)), 
                            mdates.date2num(max(all_ends) + timedelta(hours=1)))
            
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(
                by_label.values(), 
                by_label.keys(), 
                title="Galileo Satellites", 
                loc='upper center', 
                bbox_to_anchor=(0.5, -0.25), 
                ncol=4, 
                fontsize=8, 
                title_fontsize=9
            )
            
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"[SUCCESS] Transparent plot successfully saved as {filename}")
            return filename
            
        except Exception as e:
            print(f"[ERROR] Failed to generate plot: {e}")
            raise e