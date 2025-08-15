#!/usr/bin/env python3
"""
Test script to verify Earth and Moon visibility during animation
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def test_plot_visibility():
    """Test that plot objects show up properly in 3D."""
    
    print("🧪 Testing 3D plot visibility...")
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Test data - Sun at origin, Earth at 1 AU
    sun_pos = [0, 0, 0]
    earth_pos = [1.0, 0, 0]
    moon_pos = [1.003, 0, 0]  # Moon near Earth
    
    # Create plot objects (same as in simulation)
    sun_plot, = ax.plot([sun_pos[0]], [sun_pos[1]], [sun_pos[2]], 'o', 
                       color='yellow', markersize=12, markeredgecolor='orange', 
                       markeredgewidth=1, label='Sun')
    
    earth_plot, = ax.plot([earth_pos[0]], [earth_pos[1]], [earth_pos[2]], 'o', 
                         color='blue', markersize=8, markeredgecolor='darkblue', 
                         markeredgewidth=1, label='Earth')
    
    moon_plot, = ax.plot([moon_pos[0]], [moon_pos[1]], [moon_pos[2]], 'o', 
                        color='gray', markersize=5, markeredgecolor='black', 
                        markeredgewidth=1, label='Moon')
    
    # Set view and labels
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-0.5, 0.5])
    
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    
    ax.legend()
    ax.set_title('Visibility Test: Sun-Earth-Moon')
    
    print("✅ Test plot created")
    print(f"Sun position: {sun_pos}")
    print(f"Earth position: {earth_pos}")
    print(f"Moon position: {moon_pos}")
    print("\nIf you can see all three bodies, the visibility fix is working!")
    
    plt.show()

def test_update_method():
    """Test the plot update method."""
    
    print("\n🔄 Testing plot update method...")
    
    # Create figure
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create empty plot
    earth_plot, = ax.plot([], [], [], 'o', color='blue', markersize=8, label='Earth')
    
    # Test positions over time
    positions = np.array([
        [1.0, 0.0, 0.0],
        [0.9, 0.4, 0.0],
        [0.7, 0.7, 0.0],
        [0.0, 1.0, 0.0],
        [-0.7, 0.7, 0.0],
        [-1.0, 0.0, 0.0]
    ])
    
    def update_plot(plot_obj, pos):
        """Update plot object with new position."""
        plot_obj.set_data([pos[0]], [pos[1]])
        plot_obj.set_3d_properties([pos[2]])
    
    # Test each position
    for i, pos in enumerate(positions):
        update_plot(earth_plot, pos)
        print(f"Frame {i}: Earth at ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})")
    
    # Set view
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-0.5, 0.5])
    
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.legend()
    ax.set_title('Update Method Test: Earth Orbit')
    
    print("✅ Update method test complete")
    plt.show()

if __name__ == "__main__":
    print("🌍 Testing Earth and Moon Visibility")
    print("=" * 40)
    
    # Test 1: Static visibility
    test_plot_visibility()
    
    # Test 2: Update method
    test_update_method()
    
    print("\n✅ All visibility tests complete!")
    print("If you saw the celestial bodies in both tests, the fix should work!")
