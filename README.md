# Sun-Earth-Moon System Simulation

A realistic 3D animation of the Sun-Earth-Moon system using precise ephemeris data from astropy.

## Features

- **Astronomically accurate**: Uses astropy's ephemeris data for precise celestial positions
- **Sequential animation**: Shows Sun → Sun+Earth → Sun+Earth+Moon in three phases
- **Real-time dating**: Simulates any user-specified date with accurate orbital mechanics
- **3D visualization**: Interactive matplotlib 3D plots with orbital trails
- **MP4 export**: Saves animations as video files
- **Automatic scaling**: Switches between wide and close views for optimal visualization

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. For MP4 export, install ffmpeg:
   - Windows: Download from https://ffmpeg.org/
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## Usage

Run the simulation:
```bash
python sun_earth_moon_simulation.py
```

The program will prompt you for:
- Start date (YYYY-MM-DD format)
- Whether to save as MP4

## Simulation Phases

1. **Phase 1 (Days 1-10)**: Sun only, establishing the reference frame
2. **Phase 2 (Days 11-20)**: Sun + Earth orbit, showing Earth's yearly motion
3. **Phase 3 (Days 21-30)**: Earth-Moon system with zoomed view showing lunar orbit

## Technical Details

- **Duration**: 30 days simulation time
- **Time step**: 1 hour per frame
- **Ephemeris**: Uses astropy's built-in ephemeris (DE405/DE421)
- **Coordinate system**: Heliocentric (Sun-centered)
- **Accuracy**: Sub-kilometer precision for planetary positions

## Requirements

- Python 3.7+
- astropy (ephemeris calculations)
- matplotlib (3D plotting and animation)
- numpy (numerical calculations)
- ffmpeg (optional, for MP4 export)
