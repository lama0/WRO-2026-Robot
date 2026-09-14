# WRO 2026 Robot

## Project Overview

This project was developed for WRO 2026 using the LEGO SPIKE Prime platform.

The robot is designed to autonomously exit the starting parking position, follow the wall using a Distance Sensor, perform controlled right turns, detect the next wall, and continue navigating the course.

The robot was developed through repeated testing and calibration to improve steering accuracy, cornering, and wall detection.

---

## Hardware Configuration

| Port | Component | Function |
|---|---|---|
| A | Steering Motor | Controls steering |
| B | Color Sensor | Detects colors and field markers |
| C | Distance Sensor | Detects walls and measures distance |
| E | Rear Drive Motor | Controls forward and reverse movement |

---

## Steering Calibration

The steering motor is connected to Port A.

Initial setting:

`STRAIGHT = 0`

The robot slightly drifted to the left.

After testing, the final calibrated value became:

`STRAIGHT = -2`

This gave the robot a more stable straight path.

---

## Distance Sensor

The Distance Sensor is connected to Port C.

It is used to:

- Detect walls
- Measure wall distance
- Maintain approximately 20–30 cm from the wall
- Detect when a wall disappears
- Detect the new wall after a corner

During calibration:

`14 cm actual distance = 140 mm sensor reading`

---

## Parking Exit

After leaving the starting parking position, the robot:

1. Recenters the steering.
2. Drives straight for approximately 13 cm.
3. Begins the right corner sequence.

---

## Right Corner Strategy

The final tested corner sequence is:

1. 55° steering + drive 8 cm
2. 55° steering + drive 8 cm
3. 55° steering + drive 8 cm
4. 80° steering + drive 8 cm

After these steps, the robot continues turning right until the Distance Sensor detects the new wall.

The robot then stops and recenters the steering.

### Important Settings

- `STRAIGHT = -2`
- `CORNER_STEP = 55`
- `LAST_CORNER_STEP = 80`
- `CORNER_STEP_DISTANCE_CM = 8`
- `CORNER_SPEED = 400`
- `STEERING_SPEED = 400`
- `RECENTER_SPEED = 600`
- `SEARCH_WALL_SPEED = 340`

---

## Color Sensor

The Color Sensor is connected to Port B.

It will be used for red and green field elements.

The final obstacle avoidance strategy is still under testing and will be added after successful physical testing.

---

## Testing Status

Verified:

- Distance Sensor calibration: 14 cm → 140 mm
- Straight steering calibration: `STRAIGHT = -2`
- Multi-step right corner configuration
- Parking exit followed by 13 cm straight movement

Still to be tested:

- Full lap
- Final wall-following performance
- Red and green obstacle avoidance
- Final competition run

---

## Documentation

The project documentation includes:

- Mechanical design
- Wiring diagram
- System architecture diagram
- Program flowchart
- Sensor calibration
- Engineering decisions
- Risk and failure analysis
- Performance verification
- Testing and iteration log

---

## Project Status

The robot is currently in the final development and testing stage.

The Distance Sensor navigation and right-turn strategy have been developed.

Full-course testing and Color Sensor obstacle avoidance are still in progress.
