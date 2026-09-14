# WRO 2026 Robot – Engineering Project

## Project Overview

This project was developed for WRO 2026 using the LEGO SPIKE Prime platform.

The goal of the robot is to autonomously leave the starting parking position, move along the competition field, detect and follow walls using a Distance Sensor, perform controlled right turns, detect the next wall, and continue navigating the course.

The robot was developed through an iterative engineering process based on testing, observation, adjustment, and retesting. Instead of relying on one fixed movement sequence, several steering angles, driving distances, and speed values were tested and modified until the robot became more stable and predictable.

The current system includes:

- Steering control
- Rear-wheel drive
- Distance-based wall detection
- Wall-following logic
- Multi-step right corner execution
- Parking exit sequence
- Distance sensor calibration
- Color sensing hardware for future red and green obstacle detection

The obstacle avoidance strategy using the Color Sensor is still under physical testing and is not considered finalized.

---

## Robot Platform

The robot is built using the LEGO SPIKE Prime system.

The design separates the steering system from the driving system. This allows the rear motor to control forward and reverse movement while a separate motor controls the steering angle.

### Port Configuration

| Port | Component | Function |
|---|---|---|
| Port A | Steering Motor | Controls steering direction and steering angles |
| Port B | Color Sensor | Detects field colors and markers |
| Port C | Distance Sensor | Measures distance from walls and detects wall transitions |
| Port E | Rear Drive Motor | Controls forward and reverse movement |

The SPIKE Prime Hub acts as the main controller and power source for the robot.

---

## Mechanical Design

The robot uses a dedicated steering mechanism controlled by the motor connected to Port A.

During testing, the steering position initially used:

`STRAIGHT = 0`

However, the robot showed a small drift toward the left.

The steering value was gradually adjusted until the robot achieved a more stable straight path.

The final tested straight steering value is:

`STRAIGHT = -2`

The rear drive motor is connected to Port E and provides the main driving force for the robot.

The mechanical design was developed to allow steering adjustments independently from forward movement.

Additional photographs and measurements of the final robot chassis, steering mechanism, drive mechanism, and sensor positions will be added after the final physical inspection of the robot.

---

## Distance Sensor

The Distance Sensor is connected to Port C.

It is one of the main sensors used in the navigation strategy.

The sensor is used to:

- Detect the wall
- Measure the distance between the robot and the wall
- Maintain an approximate target wall distance
- Detect when a wall disappears
- Detect the next wall after a right turn

The target wall-following range is approximately:

`20–30 cm`

### Distance Sensor Calibration

The sensor was tested independently by placing an object approximately 14 cm away from the sensor.

The sensor returned:

`140 mm`

This confirmed that the readings used by the program are expressed in millimeters.

Example values:

| Actual Distance | Sensor Reading |
|---|---|
| 14 cm | 140 mm |
| 20 cm | approximately 200 mm |
| 30 cm | approximately 300 mm |

A sensor reading of `-1` may occur when the Distance Sensor does not detect a valid surface.

The program must therefore handle missing or invalid wall readings instead of assuming every reading represents a real wall.

---

## Color Sensor

The Color Sensor is connected to Port B.

Its intended purpose is to detect colored field elements or markers, including red and green elements.

The final obstacle avoidance behavior for the Color Sensor is still being tested.

For this reason, the current engineering documentation does not claim that red and green obstacle avoidance is fully verified.

The final strategy will be added only after successful physical testing.

---

## Software Architecture

The robot software is divided into separate functions so that each major movement or navigation task can be tested independently.

Important functions include:

### `set_straight()`

Moves the steering mechanism back to the calibrated straight position.

The current calibrated value is:

`STRAIGHT = -2`

### `drive_cm()`

Converts a requested travel distance in centimeters into motor rotation for the rear drive motor.

This allows movement commands to be described using physical distances rather than only motor degrees.

### `exit_parking()`

Executes the parking exit sequence.

The parking maneuver was developed separately before being integrated into the complete navigation program.

After leaving the parking area, the steering is returned to the straight position and the robot drives approximately:

`13 cm`

before beginning the next turning sequence.

### `turn_right_until_wall()`

Executes the tested multi-step right corner.

The robot performs several controlled steering movements instead of one large immediate turn.

After the turning sequence, the robot continues turning right until the Distance Sensor detects the new wall.

The drive motor is then stopped and the steering is recentered.

---

## Final Right Corner Calibration

The right corner was one of the main areas of iterative development.

An early approach using a single steering movement did not provide enough control.

The turn was therefore divided into multiple steering steps.

The final tested sequence is:

1. Steering step: `55°` → drive `8 cm`
2. Steering step: `55°` → drive `8 cm`
3. Steering step: `55°` → drive `8 cm`
4. Steering step: `80°` → drive `8 cm`

After the fourth step, the robot continues turning right while searching for the new wall.

Once the Distance Sensor detects the new wall, the robot stops the drive motor and recenters the steering.

### Current Corner Parameters

```python
STRAIGHT = -2

CORNER_STEP = 55
LAST_CORNER_STEP = 80
CORNER_STEP_DISTANCE_CM = 8

CORNER_SPEED = 400
STEERING_SPEED = 400
RECENTER_SPEED = 600
SEARCH_WALL_SPEED = 340
