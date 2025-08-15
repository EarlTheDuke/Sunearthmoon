#!/usr/bin/env python3
"""
Test version: All bodies (Sun, Earth, Moon) visible from the start
This version skips phases and shows everything immediately for debugging visibility issues.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import warnings

# Astropy imports
try:
    from astropy.time import Time
    from astropy.coordinates import get_body_barycentric
    from astropy import units as u
    print("✅ Astropy imported successfully")
except ImportError as e:
    print(f"❌ Error importing astropy: {e}")
    print("Please install astropy: pip install astropy")
    exit(1)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class TestAllVisibleSimulation:
    def __init__(self, start_date_str, duration_days=5, time_step_hours=1):
        """
        Initialize the test simulation - ALL BODIES VISIBLE FROM START.
        
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
            print(f"🕐 Test simulation starting from: {self.start_time.iso}")
        except Exception as e:
            raise ValueError(f"Invalid date format '{start_date_str}'. Use YYYY-MM-DD format. Error: {e}")
        
        # Calculate time array
        total_hours = duration_days * 24
        self.num_frames = int(total_hours / time_step_hours)
        self.time_array = self.start_time + np.arange(self.num_frames) * time_step_hours * u.hour
        
        print(f"📊 Total frames: {self.num_frames}")
        print("🚨 TEST MODE: All bodies visible from frame 1!")
        
        # Trail parameters
        self.max_trail_points = 100
        
        # View rotation parameters
        self.rotation_speed = 1.0  # degrees per frame (faster for testing)
        
        # Initialize position arrays
        self.sun_positions = np.zeros((self.num_frames, 3))
        self.earth_positions = np.zeros((self.num_frames, 3))
        self.moon_positions = np.zeros((self.num_frames, 3))
        
        # Precompute all positions
        self._precompute_positions()
        
        # Set up the plot
        self._setup_plot()
    
    def _precompute_positions(self):
        """Precompute heliocentric positions for all bodies using astropy ephemeris."""
        print("🔄 Precomputing ephemeris positions...")
        
        for i, time in enumerate(self.time_array):
            if i % 20 == 0:
                print(f"Processing frame {i}/{self.num_frames}")
            
            try:
                # Get barycentric positions
                sun_pos = get_body_barycentric('sun', time)
                earth_pos = get_body_barycentric('earth', time)
                moon_pos = get_body_barycentric('moon', time)
                
                # Convert to heliocentric coordinates (Sun at origin)
                sun_helio = np.array([0.0, 0.0, 0.0])  # Sun at origin
                earth_helio = (earth_pos - sun_pos).xyz.to(u.AU).value
                moon_helio = (moon_pos - sun_pos).xyz.to(u.AU).value
                
                self.sun_positions[i] = sun_helio
                self.earth_positions[i] = earth_helio
                self.moon_positions[i] = moon_helio
                
            except Exception as e:
                print(f"⚠️ Error calculating positions at frame {i}: {e}")
                # Use previous values if available
                if i > 0:
                    self.sun_positions[i] = self.sun_positions[i-1]
                    self.earth_positions[i] = self.earth_positions[i-1]
                    self.moon_positions[i] = self.moon_positions[i-1]
        
        print("✅ Ephemeris precomputation complete!")
        
        # Print first frame positions for debugging
        print("\n🔍 First frame positions:")
        print(f"Sun: ({self.sun_positions[0][0]:.6f}, {self.sun_positions[0][1]:.6f}, {self.sun_positions[0][2]:.6f}) AU")
        print(f"Earth: ({self.earth_positions[0][0]:.6f}, {self.earth_positions[0][1]:.6f}, {self.earth_positions[0][2]:.6f}) AU")
        print(f"Moon: ({self.moon_positions[0][0]:.6f}, {self.moon_positions[0][1]:.6f}, {self.moon_positions[0][2]:.6f}) AU")
    
    def _setup_plot(self):
        """Set up the 3D matplotlib figure and axes."""
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set initial view
        self.ax.view_init(elev=20, azim=0)
        
        # Initialize plot elements for celestial bodies - CLEAN CIRCLES WITHOUT RINGS
        self.sun_plot, = self.ax.plot([], [], [], 'o', color='yellow', markersize=15, label='Sun', alpha=0.9)
        self.earth_plot, = self.ax.plot([], [], [], 'o', color='blue', markersize=12, label='Earth', alpha=0.9)
        self.moon_plot, = self.ax.plot([], [], [], 'o', color='gray', markersize=8, label='Moon', alpha=0.9)
        
        # Initialize trail lines
        self.earth_trail, = self.ax.plot([], [], [], 'b-', alpha=0.6, linewidth=2, label='Earth Trail')
        self.moon_trail, = self.ax.plot([], [], [], color='gray', alpha=0.6, linewidth=1.5, label='Moon Trail')
        
        # Text elements
        self.title_text = self.ax.text2D(0.02, 0.98, '', transform=self.ax.transAxes, 
                                       fontsize=14, weight='bold', va='top')
        self.time_text = self.ax.text2D(0.02, 0.93, '', transform=self.ax.transAxes, 
                                      fontsize=11, va='top')
        self.info_text = self.ax.text2D(0.02, 0.88, '', transform=self.ax.transAxes, 
                                      fontsize=10, color='red', weight='bold', va='top')
        self.debug_text = self.ax.text2D(0.02, 0.83, '', transform=self.ax.transAxes, 
                                       fontsize=9, color='green', va='top')
        
        # Set 3D axes labels
        self.ax.set_xlabel('X (AU)', fontsize=12)
        self.ax.set_ylabel('Y (AU)', fontsize=12)
        self.ax.set_zlabel('Z (AU)', fontsize=12)
        
        # Set wide view to see all bodies
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-0.5, 0.5])
        
        # Add legend
        self.ax.legend(loc='upper right', fontsize=10)
        
        # Set background color for better visibility
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        
        # Make pane edges more visible
        self.ax.xaxis.pane.set_edgecolor('gray')
        self.ax.yaxis.pane.set_edgecolor('gray')
        self.ax.zaxis.pane.set_edgecolor('gray')
        self.ax.xaxis.pane.set_alpha(0.1)
        self.ax.yaxis.pane.set_alpha(0.1)
        self.ax.zaxis.pane.set_alpha(0.1)
    
    def _get_trail_data(self, positions, frame, max_points):
        """Get trail data for plotting, limited to max_points."""
        start_idx = max(0, frame - max_points)
        end_idx = frame + 1
        
        if end_idx > start_idx + 1:
            trail_positions = positions[start_idx:end_idx]
            return trail_positions[:, 0], trail_positions[:, 1], trail_positions[:, 2]
        else:
            return [], [], []
    
    def _update_plot(self, plot_obj, positions, frame):
        """Update plot object with new positions."""
        if frame < len(positions):
            pos = positions[frame]
            plot_obj.set_data([pos[0]], [pos[1]])
            plot_obj.set_3d_properties([pos[2]])
            return pos
        else:
            # Hide the object if no data
            plot_obj.set_data([], [])
            plot_obj.set_3d_properties([])
            return None
    
    def animate(self, frame):
        """Animation function called for each frame - ALL BODIES ALWAYS VISIBLE."""
        # Calculate current view rotation
        azim = (frame * self.rotation_speed) % 360
        
        # Current time
        current_time = self.time_array[frame]
        
        # Update title and time display
        self.title_text.set_text(f'🧪 TEST MODE: All Bodies Visible (Start: {self.start_date_str})')
        self.time_text.set_text(f'Date: {current_time.iso[:10]} {current_time.iso[11:19]} UTC')
        self.info_text.set_text(f'Frame: {frame+1}/{self.num_frames} | View Angle: {azim:.1f}°')
        
        # Set view
        self.ax.view_init(elev=20, azim=azim)
        
        # Clear previous trail data
        self.earth_trail.set_data([], [])
        self.earth_trail.set_3d_properties([])
        self.moon_trail.set_data([], [])
        self.moon_trail.set_3d_properties([])
        
        # UPDATE ALL BODIES - NO PHASES!
        sun_pos = self._update_plot(self.sun_plot, self.sun_positions, frame)
        earth_pos = self._update_plot(self.earth_plot, self.earth_positions, frame)
        moon_pos = self._update_plot(self.moon_plot, self.moon_positions, frame)
        
        # Show current positions in debug text
        if sun_pos is not None and earth_pos is not None and moon_pos is not None:
            earth_dist = np.linalg.norm(earth_pos)
            moon_earth_dist = np.linalg.norm(moon_pos - earth_pos)
            self.debug_text.set_text(f'Earth dist: {earth_dist:.3f} AU | Moon-Earth: {moon_earth_dist:.6f} AU')
        
        # Add trails for both Earth and Moon
        if frame > 10:  # Start trails after a few frames
            # Earth trail
            trail_x, trail_y, trail_z = self._get_trail_data(self.earth_positions, frame, self.max_trail_points)
            if trail_x:
                self.earth_trail.set_data(trail_x, trail_y)
                self.earth_trail.set_3d_properties(trail_z)
            
            # Moon trail
            trail_x, trail_y, trail_z = self._get_trail_data(self.moon_positions, frame, self.max_trail_points)
            if trail_x:
                self.moon_trail.set_data(trail_x, trail_y)
                self.moon_trail.set_3d_properties(trail_z)
        
        return (self.sun_plot, self.earth_plot, self.moon_plot, 
                self.earth_trail, self.moon_trail, 
                self.title_text, self.time_text, self.info_text, self.debug_text)
    
    def run_simulation(self, show_interactive=True):
        """Run the test animation simulation."""
        print("🧪 Starting TEST animation - all bodies visible from start...")
        
        # Create animation
        anim = FuncAnimation(
            self.fig, 
            self.animate, 
            frames=self.num_frames,
            interval=100,   # 100ms between frames
            blit=False,     # Set to False for 3D plots
            repeat=True
        )
        
        # Show interactive plot
        if show_interactive:
            plt.tight_layout()
            plt.show()
        
        return anim


def main():
    """Main function to run the test simulation."""
    print("🧪 TEST SIMULATION: All Bodies Visible From Start")
    print("=" * 55)
    print("This version shows Sun, Earth, and Moon immediately!")
    print()
    
    try:
        # Use a short test period
        start_date = "2025-08-14"  # Your original date
        duration = 3  # Just 3 days for quick testing
        
        print(f"📅 Start date: {start_date}")
        print(f"⏱️ Duration: {duration} days")
        print(f"🔍 Purpose: Test if Earth and Moon are visible")
        
        # Create test simulation
        sim = TestAllVisibleSimulation(
            start_date_str=start_date,
            duration_days=duration,
            time_step_hours=1
        )
        
        # Run simulation
        anim = sim.run_simulation(show_interactive=True)
        
        print("\n✅ Test simulation complete!")
        print("\n🔍 What you should see:")
        print("• Yellow Sun at center (large)")
        print("• Blue Earth orbiting Sun (medium)")
        print("• Gray Moon near Earth (small)")
        print("• All three bodies visible from frame 1")
        print("• Trails showing their paths")
        
    except Exception as e:
        print(f"❌ Error running test simulation: {e}")
        print("💡 Make sure you have all required packages installed:")
        print("pip install astropy matplotlib numpy")
    
    except KeyboardInterrupt:
        print("\n👋 Test simulation interrupted by user.")


if __name__ == "__main__":
    main()
