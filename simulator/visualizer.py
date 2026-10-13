import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class ScheduleVisualizer:
    """Generates visual charts (Gantt-style) for mission schedules and resource allocation."""
    
    @staticmethod
    def plot_schedule(schedule, filename="mission_schedule.png"):
        if not schedule:
            print("[INFO] No scheduled contacts to plot.")
            return None

        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Prepare data for plotting
        stations = list(set(r.station_name for r in schedule))
        station_y_mapping = {station: i for i, station in enumerate(stations)}
        
        for req in schedule:
            y_pos = station_y_mapping[req.station_name]
            start_num = mdates.date2num(req.start_time)
            end_num = mdates.date2num(req.end_time)
            duration_num = end_num - start_num
            
            # Draw horizontal bar representing the contact window
            ax.barh(
                y_pos, 
                duration_num, 
                left=start_num, 
                height=0.4, 
                align='center', 
                color='skyblue', 
                edgecolor='navy',
                alpha=0.8
            )
            
            # Label the bar with satellite ID and priority
            ax.text(
                start_num + duration_num / 2, 
                y_pos, 
                f"{req.sat_id} (P:{req.priority})", 
                ha='center', 
                va='center', 
                color='black', 
                fontsize=9, 
                fontweight='bold'
            )

        ax.set_yticks(list(station_y_mapping.values()))
        ax.set_yticklabels(list(station_y_mapping.keys()))
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        ax.set_xlabel("Time (UTC)")
        ax.set_ylabel("Ground Stations")
        ax.set_title("Ground Segment Resource Allocation & Conflict Resolution")
        ax.grid(True, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"[SUCCESS] Schedule plot saved as {filename}")
        return filename