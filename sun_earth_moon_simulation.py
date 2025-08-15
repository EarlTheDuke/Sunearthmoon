#!/usr/bin/env python3
"""
Realistic 3D Sun-Earth-Moon System Simulation
Using precise ephemeris data from astropy for accurate celestial mechanics.

This script creates a sequential animation showing:
1. First 1/3: Sun only
2. Second 1/3: Sun + Earth orbit
3. Final 1/3: Sun + Earth + Moon orbit (zoomed view)

Author: AI Assistant
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
import warnings

# Astropy imports
try:
    from astropy.time import Time
    from astropy.coordinates import get_body_barycentric
    from astropy import units as u
    print("Astropy imported successfully")
except ImportError as e:
    print(f"Error importing astropy: {e}")
    print("Please install astropy: pip install astropy")
    exit(1)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class SolarSystemSimulation:
    def __init__(self, start_date_str, duration_days=30, time_step_hours=1):
        """
        Initialize the solar system simulation.
        
        Parameters:
        - start_date_str: Starting date in YYYY-MM-DD format
        - duration_days: Total simulation duration in days
        - time_step_hours: Time step between frames in hours
        """
        self.start_date_str = start_date_str
        self.duration_days = duration_days
        self.time_step_hours = time_step_hours
        
        # Parse and validate the start date
        try:
            self.start_time = Time(start_date_str)
            print(f"Simulation starting from: {self.start_time.iso}")
        except Exception as e:
            raise ValueError(f"Invalid date format '{start_date_str}'. Use YYYY-MM-DD format. Error: {e}")
        
        # Calculate time array
        total_hours = duration_days * 24
        self.num_frames = int(total_hours / time_step_hours)
        self.time_array = self.start_time + np.arange(self.num_frames) * time_step_hours * u.hour
        
        # Animation phases
        self.phase1_frames = self.num_frames // 3  # Sun only
        self.phase2_frames = 2 * self.num_frames // 3  # Sun + Earth
        self.phase3_frames = self.num_frames  # Sun + Earth + Moon
        
        print(f"Total frames: {self.num_frames}")
        print(f"Phase 1 (Sun only): 0 to {self.phase1_frames}")
        print(f"Phase 2 (Sun+Earth): {self.phase1_frames} to {self.phase2_frames}")
        print(f"Phase 3 (All bodies): {self.phase2_frames} to {self.phase3_frames}")
        
        # Physical parameters (in AU)
        self.sun_radius = 0.00465  # ~696,000 km
        self.earth_radius = 4.26e-5  # ~6,371 km
        self.moon_radius = 1.16e-5  # ~1,737 km
        
        # Scale up for visibility
        self.sun_size = self.sun_radius * 100
        self.earth_size = self.earth_radius * 2000
        self.moon_size = self.moon_radius * 3000
        
        # Trail length for orbits
        self.trail_length = 100
        
        # Initialize position arrays
        self.sun_positions = np.zeros((self.num_frames, 3))
        self.earth_positions = np.zeros((self.num_frames, 3))
        self.moon_positions = np.zeros((self.num_frames, 3))
        
        # Calculate all positions
        self._calculate_positions()
        
        # Set up the plot
        self._setup_plot()
    
    def _calculate_positions(self):
        """Calculate positions for all bodies using astropy ephemeris."""
        print("Calculating ephemeris positions...")
        
        for i, time in enumerate(self.time_array):
            if i % 100 == 0:
                print(f"Processing frame {i}/{self.num_frames}")
            
            try:
                # Get barycentric positions
                sun_pos = get_body_barycentric('sun', time)
                earth_pos = get_body_barycentric('earth', time)
                moon_pos = get_body_barycentric('moon', time)
                
                # Convert to heliocentric coordinates (subtract Sun's position)
                sun_helio = np.array([0.0, 0.0, 0.0])  # Sun at origin in heliocentric
                earth_helio = (earth_pos - sun_pos).xyz.to(u.AU).value
                moon_helio = (moon_pos - sun_pos).xyz.to(u.AU).value
                
                self.sun_positions[i] = sun_helio
                self.earth_positions[i] = earth_helio
                self.moon_positions[i] = moon_helio
                
            except Exception as e:
                print(f"Error calculating positions at frame {i}: {e}")
                # Use previous values if available
                if i > 0:
                    self.sun_positions[i] = self.sun_positions[i-1]
                    self.earth_positions[i] = self.earth_positions[i-1]
                    self.moon_positions[i] = self.moon_positions[i-1]
        
        print("Ephemeris calculation complete!")
    
    def _setup_plot(self):
        """Set up the 3D matplotlib figure and axes."""
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set initial view
        self.ax.view_init(elev=20, azim=45)
        
        # Initialize plot elements
        self.sun_plot, = self.ax.plot([], [], [], 'yo', markersize=15, label='Sun')
        self.earth_plot, = self.ax.plot([], [], [], 'bo', markersize=8, label='Earth')
        self.moon_plot, = self.ax.plot([], [], [], 'o', color='gray', markersize=4, label='Moon')
        
        # Trail lines
        self.earth_trail, = self.ax.plot([], [], [], 'b-', alpha=0.6, linewidth=1)
        self.moon_trail, = self.ax.plot([], [], [], '-', color='gray', alpha=0.6, linewidth=1)
        
        # Text elements
        self.title_text = self.ax.text2D(0.05, 0.95, '', transform=self.ax.transAxes, fontsize=12, weight='bold')
        self.time_text = self.ax.text2D(0.05, 0.90, '', transform=self.ax.transAxes, fontsize=10)
        self.phase_text = self.ax.text2D(0.05, 0.85, '', transform=self.ax.transAxes, fontsize=10, color='red')
        
        # Set labels
        self.ax.set_xlabel('X (AU)')
        self.ax.set_ylabel('Y (AU)')
        self.ax.set_zlabel('Z (AU)')
        
        # Initial wide view for Sun-Earth system
        self._set_wide_view()
    
    def _set_wide_view(self):
        """Set wide view for Sun-Earth system."""
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-0.5, 0.5])
    
    def _set_close_view(self, frame):
        """Set close view centered on Earth for Earth-Moon system."""
        earth_pos = self.earth_positions[frame]
        margin = 0.1  # AU
        
        self.ax.set_xlim([earth_pos[0] - margin, earth_pos[0] + margin])
        self.ax.set_ylim([earth_pos[1] - margin, earth_pos[1] + margin])
        self.ax.set_zlim([earth_pos[2] - 0.02, earth_pos[2] + 0.02])
    
    def _get_trail_indices(self, frame, trail_length):
        """Get indices for trail plotting."""
        start_idx = max(0, frame - trail_length)
        return start_idx, frame + 1
    
    def animate(self, frame):
        """Animation function called for each frame."""
        # Clear previous plots
        self.sun_plot.set_data([], [])
        self.sun_plot.set_3d_properties([])
        self.earth_plot.set_data([], [])
        self.earth_plot.set_3d_properties([])
        self.moon_plot.set_data([], [])
        self.moon_plot.set_3d_properties([])
        self.earth_trail.set_data([], [])
        self.earth_trail.set_3d_properties([])
        self.moon_trail.set_data([], [])
        self.moon_trail.set_3d_properties([])
        
        # Current time
        current_time = self.time_array[frame]
        
        # Update title and time
        self.title_text.set_text(f'Sun-Earth-Moon System Simulation (Start: {self.start_date_str})')
        self.time_text.set_text(f'Date: {current_time.iso[:10]} {current_time.iso[11:19]}')
        
        # Phase 1: Sun only
        if frame < self.phase1_frames:
            self.phase_text.set_text('Phase 1: Sun Only')
            self._set_wide_view()
            
            # Show Sun
            sun_pos = self.sun_positions[frame]
            self.sun_plot.set_data([sun_pos[0]], [sun_pos[1]])
            self.sun_plot.set_3d_properties([sun_pos[2]])
            
        # Phase 2: Sun + Earth
        elif frame < self.phase2_frames:
            self.phase_text.set_text('Phase 2: Sun + Earth Orbit')
            self._set_wide_view()
            
            # Show Sun
            sun_pos = self.sun_positions[frame]
            self.sun_plot.set_data([sun_pos[0]], [sun_pos[1]])
            self.sun_plot.set_3d_properties([sun_pos[2]])
            
            # Show Earth
            earth_pos = self.earth_positions[frame]
            self.earth_plot.set_data([earth_pos[0]], [earth_pos[1]])
            self.earth_plot.set_3d_properties([earth_pos[2]])
            
            # Earth trail
            start_idx, end_idx = self._get_trail_indices(frame, self.trail_length)
            if end_idx > start_idx + 1:
                earth_trail_pos = self.earth_positions[start_idx:end_idx]
                self.earth_trail.set_data(earth_trail_pos[:, 0], earth_trail_pos[:, 1])
                self.earth_trail.set_3d_properties(earth_trail_pos[:, 2])
        
        # Phase 3: Sun + Earth + Moon (close view)
        else:
            self.phase_text.set_text('Phase 3: Earth-Moon System (Zoomed)')
            self._set_close_view(frame)
            
            # Show Earth (main focus)
            earth_pos = self.earth_positions[frame]
            self.earth_plot.set_data([earth_pos[0]], [earth_pos[1]])
            self.earth_plot.set_3d_properties([earth_pos[2]])
            
            # Show Moon
            moon_pos = self.moon_positions[frame]
            self.moon_plot.set_data([moon_pos[0]], [moon_pos[1]])
            self.moon_plot.set_3d_properties([moon_pos[2]])
            
            # Moon trail
            start_idx, end_idx = self._get_trail_indices(frame, self.trail_length)
            if end_idx > start_idx + 1:
                moon_trail_pos = self.moon_positions[start_idx:end_idx]
                self.moon_trail.set_data(moon_trail_pos[:, 0], moon_trail_pos[:, 1])
                self.moon_trail.set_3d_properties(moon_trail_pos[:, 2])
            
            # Earth trail (shorter in close view)
            start_idx, end_idx = self._get_trail_indices(frame, 50)
            if end_idx > start_idx + 1:
                earth_trail_pos = self.earth_positions[start_idx:end_idx]
                self.earth_trail.set_data(earth_trail_pos[:, 0], earth_trail_pos[:, 1])
                self.earth_trail.set_3d_properties(earth_trail_pos[:, 2])
        
        return (self.sun_plot, self.earth_plot, self.moon_plot, 
                self.earth_trail, self.moon_trail, 
                self.title_text, self.time_text, self.phase_text)
    
    def run_simulation(self, save_mp4=True, show_plot=True):
        """Run the animation simulation."""
        print("Starting animation...")
        
        # Create animation
        anim = FuncAnimation(
            self.fig, 
            self.animate, 
            frames=self.num_frames,
            interval=50,  # 50ms between frames
            blit=False,   # Set to False for 3D plots
            repeat=True
        )
        
        # Save as MP4 if requested
        if save_mp4:
            try:
                print("Saving animation as MP4...")
                filename = f'sun_earth_moon_simulation_{self.start_date_str.replace("-", "_")}.mp4'
                
                # Try different writers
                writers = ['ffmpeg', 'pillow']
                saved = False
                
                for writer in writers:
                    try:
                        anim.save(filename, writer=writer, fps=20, bitrate=1800)
                        print(f"Animation saved as: {filename}")
                        saved = True
                        break
                    except Exception as e:
                        print(f"Failed to save with {writer}: {e}")
                        continue
                
                if not saved:
                    print("Could not save MP4. Install ffmpeg or use show_plot=True to view interactively.")
                    
            except Exception as e:
                print(f"Error saving animation: {e}")
        
        # Show interactive plot if requested
        if show_plot:
            plt.tight_layout()
            plt.show()
        
        return anim


def main():
    """Main function to run the simulation."""
    print("=== Sun-Earth-Moon System Simulation ===")
    print("Using precise ephemeris data from astropy")
    print()
    
    # Get user input for start date
    while True:
        try:
            start_date = input("Enter start date (YYYY-MM-DD format, e.g., 2025-08-14): ").strip()
            
            # Validate date format
            datetime.strptime(start_date, '%Y-%m-%d')
            break
            
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format (e.g., 2025-08-14)")
        except KeyboardInterrupt:
            print("\nExiting...")
            return
    
    try:
        # Create and run simulation
        print(f"\nInitializing simulation for {start_date}...")
        
        # Check if we should save MP4
        save_choice = input("Save animation as MP4? (y/n, default=y): ").strip().lower()
        save_mp4 = save_choice != 'n'
        
        # Create simulation
        sim = SolarSystemSimulation(
            start_date_str=start_date,
            duration_days=30,
            time_step_hours=1
        )
        
        # Run simulation
        anim = sim.run_simulation(save_mp4=save_mp4, show_plot=True)
        
        print("\nSimulation complete!")
        print("The animation shows three phases:")
        print("1. First 1/3: Sun only")
        print("2. Second 1/3: Sun + Earth orbit")
        print("3. Final 1/3: Earth-Moon system (zoomed view)")
        
    except Exception as e:
        print(f"Error running simulation: {e}")
        print("Make sure you have all required packages installed:")
        print("pip install astropy matplotlib numpy")
    
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")


if __name__ == "__main__":
    main()
