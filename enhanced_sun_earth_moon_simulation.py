#!/usr/bin/env python3
"""
Enhanced Sun-Earth-Moon System Simulation
Using precise ephemeris data from astropy for accurate celestial mechanics.

This script creates a 3D animation with configurable parameters and phases:
1. First 1/3: Sun only
2. Second 1/3: Sun + Earth orbit
3. Final 1/3: Sun + Earth + Moon with zoom to Earth-Moon system

Author: AI Assistant
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
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

class EnhancedSolarSystemSimulation:
    def __init__(self, start_date_str, duration_days=30, time_step_hours=1):
        """
        Initialize the enhanced solar system simulation.
        
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
            print(f"🕐 Simulation starting from: {self.start_time.iso}")
        except Exception as e:
            raise ValueError(f"Invalid date format '{start_date_str}'. Use YYYY-MM-DD format. Error: {e}")
        
        # Calculate time array
        total_hours = duration_days * 24
        self.num_frames = int(total_hours / time_step_hours)
        self.time_array = self.start_time + np.arange(self.num_frames) * time_step_hours * u.hour
        
        # Animation phases - more balanced timing
        self.phase1_frames = max(50, self.num_frames // 6)  # Sun only (shorter)
        self.phase2_frames = max(100, self.num_frames // 2)  # Sun + Earth (longer)
        self.phase3_frames = self.num_frames  # Sun + Earth + Moon
        
        print(f"📊 Total frames: {self.num_frames}")
        print(f"Phase 1 (Sun only): 0 to {self.phase1_frames}")
        print(f"Phase 2 (Sun+Earth): {self.phase1_frames} to {self.phase2_frames}")
        print(f"Phase 3 (All bodies): {self.phase2_frames} to {self.phase3_frames}")
        
        # Body sizes for scatter plots (in points squared for matplotlib)
        self.sun_size = 200      # Large yellow circle
        self.earth_size = 50     # Medium blue circle
        self.moon_size = 20      # Small gray circle
        
        # Trail parameters
        self.max_trail_points = 200
        
        # View rotation parameters
        self.rotation_speed = 0.5  # degrees per frame
        
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
            if i % 100 == 0:
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
    
    def _setup_plot(self):
        """Set up the 3D matplotlib figure and axes."""
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set initial view
        self.ax.view_init(elev=20, azim=0)
        
        # Initialize scatter plot elements (empty initially)
        self.sun_scatter = self.ax.scatter([], [], [], s=self.sun_size, c='yellow', 
                                         alpha=0.9, edgecolors='orange', linewidth=1, label='Sun')
        self.earth_scatter = self.ax.scatter([], [], [], s=self.earth_size, c='blue', 
                                           alpha=0.8, edgecolors='darkblue', linewidth=1, label='Earth')
        self.moon_scatter = self.ax.scatter([], [], [], s=self.moon_size, c='gray', 
                                          alpha=0.8, edgecolors='black', linewidth=1, label='Moon')
        
        # Initialize trail lines
        self.earth_trail, = self.ax.plot([], [], [], 'b-', alpha=0.4, linewidth=1.5, label='Earth Trail')
        self.moon_trail, = self.ax.plot([], [], [], color='gray', alpha=0.4, linewidth=1, label='Moon Trail')
        
        # Text elements
        self.title_text = self.ax.text2D(0.02, 0.98, '', transform=self.ax.transAxes, 
                                       fontsize=14, weight='bold', va='top')
        self.time_text = self.ax.text2D(0.02, 0.93, '', transform=self.ax.transAxes, 
                                      fontsize=11, va='top')
        self.phase_text = self.ax.text2D(0.02, 0.88, '', transform=self.ax.transAxes, 
                                       fontsize=10, color='red', weight='bold', va='top')
        self.info_text = self.ax.text2D(0.02, 0.83, '', transform=self.ax.transAxes, 
                                      fontsize=9, color='blue', va='top')
        
        # Set 3D axes labels
        self.ax.set_xlabel('X (AU)', fontsize=12)
        self.ax.set_ylabel('Y (AU)', fontsize=12)
        self.ax.set_zlabel('Z (AU)', fontsize=12)
        
        # Initial wide view for Sun-Earth system
        self._set_wide_view()
        
        # Add legend
        self.ax.legend(loc='upper right', fontsize=10)
    
    def _set_wide_view(self):
        """Set wide view for Sun-Earth system (±2 AU)."""
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-0.5, 0.5])
    
    def _set_earth_moon_view(self, frame):
        """Set close view centered on Earth for Earth-Moon system (0.003 AU scale)."""
        earth_pos = self.earth_positions[frame]
        scale = 0.003  # AU
        
        self.ax.set_xlim([earth_pos[0] - scale, earth_pos[0] + scale])
        self.ax.set_ylim([earth_pos[1] - scale, earth_pos[1] + scale])
        self.ax.set_zlim([earth_pos[2] - scale/5, earth_pos[2] + scale/5])
    
    def _get_trail_data(self, positions, frame, max_points):
        """Get trail data for plotting, limited to max_points."""
        start_idx = max(0, frame - max_points)
        end_idx = frame + 1
        
        if end_idx > start_idx + 1:
            trail_positions = positions[start_idx:end_idx]
            return trail_positions[:, 0], trail_positions[:, 1], trail_positions[:, 2]
        else:
            return [], [], []
    
    def _update_scatter(self, scatter, positions, frame):
        """Update scatter plot with new positions."""
        if frame < len(positions):
            pos = positions[frame]
            # Remove previous scatter data and add new
            scatter._offsets3d = ([pos[0]], [pos[1]], [pos[2]])
    
    def animate(self, frame):
        """Animation function called for each frame."""
        # Calculate current view rotation
        azim = (frame * self.rotation_speed) % 360
        
        # Current time
        current_time = self.time_array[frame]
        
        # Update title and time display
        self.title_text.set_text(f'Enhanced Sun-Earth-Moon System (Start: {self.start_date_str})')
        self.time_text.set_text(f'Date: {current_time.iso[:10]} {current_time.iso[11:19]} UTC')
        
        # Add frame counter for debugging
        frame_info = f'Frame: {frame+1}/{self.num_frames}'
        
        # Clear previous trail data
        self.earth_trail.set_data([], [])
        self.earth_trail.set_3d_properties([])
        self.moon_trail.set_data([], [])
        self.moon_trail.set_3d_properties([])
        
        # Phase 1: Sun only
        if frame < self.phase1_frames:
            self.phase_text.set_text(f'Phase 1: Sun Only ({frame_info})')
            self.info_text.set_text(f'Establishing heliocentric reference frame')
            self._set_wide_view()
            self.ax.view_init(elev=20, azim=azim)
            
            # Show only Sun
            self._update_scatter(self.sun_scatter, self.sun_positions, frame)
            # Hide other bodies
            self.earth_scatter._offsets3d = ([], [], [])
            self.moon_scatter._offsets3d = ([], [], [])
            
        # Phase 2: Sun + Earth
        elif frame < self.phase2_frames:
            self.phase_text.set_text(f'Phase 2: Sun + Earth Orbit ({frame_info})')
            earth_dist = np.linalg.norm(self.earth_positions[frame])
            self.info_text.set_text(f'Earth distance: {earth_dist:.3f} AU')
            self._set_wide_view()
            self.ax.view_init(elev=20, azim=azim)
            
            # Show Sun and Earth
            self._update_scatter(self.sun_scatter, self.sun_positions, frame)
            self._update_scatter(self.earth_scatter, self.earth_positions, frame)
            self.moon_scatter._offsets3d = ([], [], [])
            
            # Earth trail
            trail_x, trail_y, trail_z = self._get_trail_data(self.earth_positions, frame, self.max_trail_points)
            if trail_x:
                self.earth_trail.set_data(trail_x, trail_y)
                self.earth_trail.set_3d_properties(trail_z)
        
        # Phase 3: Sun + Earth + Moon (zoomed to Earth-Moon system)
        else:
            self.phase_text.set_text(f'Phase 3: Earth-Moon System ({frame_info})')
            moon_earth_dist = np.linalg.norm(self.moon_positions[frame] - self.earth_positions[frame])
            self.info_text.set_text(f'Moon-Earth distance: {moon_earth_dist:.6f} AU')
            self._set_earth_moon_view(frame)
            self.ax.view_init(elev=15, azim=azim)
            
            # Show Earth and Moon (Sun not visible in this close view)
            self.sun_scatter._offsets3d = ([], [], [])
            self._update_scatter(self.earth_scatter, self.earth_positions, frame)
            self._update_scatter(self.moon_scatter, self.moon_positions, frame)
            
            # Both trails (shorter for close view)
            trail_length = min(self.max_trail_points, 100)
            
            # Earth trail
            trail_x, trail_y, trail_z = self._get_trail_data(self.earth_positions, frame, trail_length)
            if trail_x:
                self.earth_trail.set_data(trail_x, trail_y)
                self.earth_trail.set_3d_properties(trail_z)
            
            # Moon trail
            trail_x, trail_y, trail_z = self._get_trail_data(self.moon_positions, frame, trail_length)
            if trail_x:
                self.moon_trail.set_data(trail_x, trail_y)
                self.moon_trail.set_3d_properties(trail_z)
        
        return (self.sun_scatter, self.earth_scatter, self.moon_scatter, 
                self.earth_trail, self.moon_trail, 
                self.title_text, self.time_text, self.phase_text, self.info_text)
    
    def run_simulation(self, save_mp4=False, mp4_filename=None, show_interactive=True):
        """Run the animation simulation."""
        print("🎬 Starting enhanced animation...")
        
        # Create animation
        anim = FuncAnimation(
            self.fig, 
            self.animate, 
            frames=self.num_frames,
            interval=50,   # 50ms between frames (20 FPS) - faster to see all phases
            blit=False,    # Set to False for 3D plots
            repeat=True
        )
        
        # Save as MP4 if requested
        if save_mp4:
            try:
                if mp4_filename is None:
                    mp4_filename = f'enhanced_sun_earth_moon_{self.start_date_str.replace("-", "_")}.mp4'
                
                print(f"💾 Saving animation as MP4: {mp4_filename}")
                
                # Use FFMpegWriter
                writer = FFMpegWriter(fps=10, metadata=dict(artist='Enhanced Solar System Simulation'), 
                                    bitrate=1800)
                anim.save(mp4_filename, writer=writer)
                print(f"✅ Animation saved successfully!")
                
            except Exception as e:
                print(f"❌ Error saving MP4: {e}")
                print("💡 Make sure ffmpeg is installed for MP4 export")
        
        # Show interactive plot if requested
        if show_interactive:
            plt.tight_layout()
            plt.show()
        
        return anim


def get_user_input():
    """Get user input for simulation parameters."""
    print("🌍 Enhanced Sun-Earth-Moon System Simulation")
    print("=" * 55)
    print("Using precise ephemeris data from astropy")
    print()
    
    # Get start date
    while True:
        try:
            start_date = input("Enter start date (YYYY-MM-DD, e.g., 2025-08-14): ").strip()
            if not start_date:
                start_date = "2025-08-14"
                print(f"Using default: {start_date}")
            
            # Validate date format
            datetime.strptime(start_date, '%Y-%m-%d')
            break
            
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD format")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            return None, None, None, None, None
    
    # Get duration
    while True:
        try:
            duration_input = input("Enter duration in days (default 30): ").strip()
            if not duration_input:
                duration_days = 30
            else:
                duration_days = int(duration_input)
                if duration_days <= 0:
                    raise ValueError("Duration must be positive")
            break
        except ValueError:
            print("❌ Please enter a valid positive number for duration")
    
    # Get time step
    while True:
        try:
            timestep_input = input("Enter time step in hours (default 1): ").strip()
            if not timestep_input:
                time_step_hours = 1
            else:
                time_step_hours = float(timestep_input)
                if time_step_hours <= 0:
                    raise ValueError("Time step must be positive")
            break
        except ValueError:
            print("❌ Please enter a valid positive number for time step")
    
    # Get save option
    save_choice = input("Save animation as MP4? (y/n, default n): ").strip().lower()
    save_mp4 = save_choice in ['y', 'yes']
    
    mp4_filename = None
    if save_mp4:
        filename_input = input("Enter MP4 filename (or press Enter for auto): ").strip()
        if filename_input:
            if not filename_input.endswith('.mp4'):
                filename_input += '.mp4'
            mp4_filename = filename_input
    
    return start_date, duration_days, time_step_hours, save_mp4, mp4_filename


def main():
    """Main function to run the enhanced simulation."""
    try:
        # Get user input
        params = get_user_input()
        if params[0] is None:  # User cancelled
            return
        
        start_date, duration_days, time_step_hours, save_mp4, mp4_filename = params
        
        print(f"\n🚀 Initializing enhanced simulation...")
        print(f"📅 Start date: {start_date}")
        print(f"⏱️ Duration: {duration_days} days")
        print(f"🕐 Time step: {time_step_hours} hours")
        print(f"💾 Save MP4: {'Yes' if save_mp4 else 'No'}")
        
        # Create simulation
        sim = EnhancedSolarSystemSimulation(
            start_date_str=start_date,
            duration_days=duration_days,
            time_step_hours=time_step_hours
        )
        
        # Run simulation
        anim = sim.run_simulation(
            save_mp4=save_mp4, 
            mp4_filename=mp4_filename, 
            show_interactive=True
        )
        
        print("\n✅ Enhanced simulation complete!")
        print("\n📋 Animation features:")
        print("• Three distinct phases with automatic transitions")
        print("• Slow view rotation for better 3D perspective")
        print("• Real-time date display and distance measurements")
        print("• Orbital trails with configurable length")
        print("• Automatic zoom to Earth-Moon system in final phase")
        print("• Sized scatter points representing actual celestial bodies")
        
    except Exception as e:
        print(f"❌ Error running enhanced simulation: {e}")
        print("💡 Make sure you have all required packages installed:")
        print("pip install astropy matplotlib numpy")
    
    except KeyboardInterrupt:
        print("\n👋 Enhanced simulation interrupted by user.")


if __name__ == "__main__":
    main()
