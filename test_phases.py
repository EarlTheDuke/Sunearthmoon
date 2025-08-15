#!/usr/bin/env python3
"""
Test script to verify animation phase timing
"""

def test_phase_timing(duration_days=30, time_step_hours=1):
    """Test the phase timing calculation."""
    
    total_hours = duration_days * 24
    num_frames = int(total_hours / time_step_hours)
    
    # New phase calculation (fixed)
    phase1_frames = max(50, num_frames // 6)  # Sun only (shorter)
    phase2_frames = max(100, num_frames // 2)  # Sun + Earth (longer)
    phase3_frames = num_frames  # Sun + Earth + Moon
    
    print(f"🧪 Testing phase timing for {duration_days} days with {time_step_hours}h steps")
    print(f"Total frames: {num_frames}")
    print(f"Total hours: {total_hours}")
    print()
    
    print("Phase timing:")
    print(f"Phase 1 (Sun only): frames 0 to {phase1_frames} ({phase1_frames/24:.1f} days)")
    print(f"Phase 2 (Sun+Earth): frames {phase1_frames} to {phase2_frames} ({(phase2_frames-phase1_frames)/24:.1f} days)")
    print(f"Phase 3 (All bodies): frames {phase2_frames} to {phase3_frames} ({(phase3_frames-phase2_frames)/24:.1f} days)")
    print()
    
    # Calculate percentages
    phase1_percent = (phase1_frames / num_frames) * 100
    phase2_percent = ((phase2_frames - phase1_frames) / num_frames) * 100
    phase3_percent = ((phase3_frames - phase2_frames) / num_frames) * 100
    
    print("Phase distribution:")
    print(f"Phase 1: {phase1_percent:.1f}% of animation")
    print(f"Phase 2: {phase2_percent:.1f}% of animation")
    print(f"Phase 3: {phase3_percent:.1f}% of animation")
    print()
    
    # Time to see each phase at 20 FPS
    fps = 20
    phase1_seconds = phase1_frames / fps
    phase2_seconds = (phase2_frames - phase1_frames) / fps
    phase3_seconds = (phase3_frames - phase2_frames) / fps
    
    print("Viewing time at 20 FPS:")
    print(f"Phase 1 duration: {phase1_seconds:.1f} seconds ({phase1_seconds/60:.1f} minutes)")
    print(f"Phase 2 duration: {phase2_seconds:.1f} seconds ({phase2_seconds/60:.1f} minutes)")
    print(f"Phase 3 duration: {phase3_seconds:.1f} seconds ({phase3_seconds/60:.1f} minutes)")
    print(f"Total animation: {(phase1_seconds + phase2_seconds + phase3_seconds)/60:.1f} minutes")

if __name__ == "__main__":
    print("Testing different durations:\n")
    
    test_cases = [
        (30, 1),   # 30 days, 1 hour steps
        (40, 1),   # 40 days, 1 hour steps  
        (10, 1),   # 10 days, 1 hour steps
        (7, 0.5),  # 7 days, 30 minute steps
    ]
    
    for days, hours in test_cases:
        test_phase_timing(days, hours)
        print("-" * 60)
        print()
