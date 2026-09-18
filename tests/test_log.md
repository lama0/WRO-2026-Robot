# WRO 2026 Robot – Testing Log

This file records the main physical tests, observations, modifications, and results made during the development of the WRO 2026 robot.

The robot was developed through repeated testing of steering, wall detection, cornering, sensor behavior, obstacle avoidance, parking exit, and return-to-parking movement.

---

## Development and Testing Log

| Test | Initial Setting / Problem | Observation | Modification | Result / Status |
|---|---|---|---|---|
| Straight Steering | `STRAIGHT = 0` | Robot drifted slightly instead of travelling straight | Steering calibration adjusted gradually | `STRAIGHT = -2` produced a more stable straight path |
| Parking Exit | Initial parking exit required tuning | Robot needed a controlled path to leave the parking area without contacting the boundary | Developed a multi-step left steering exit using `-55` steering steps | Parking exit sequence calibrated and integrated |
| First Forward Approach | Initial approach distance required adjustment | Robot needed additional movement before beginning the first-wall search | Final value set to `FIRST_STRAIGHT_CM = 26` with calibrated approach scaling | Improved first-wall approach |
| First Wall Search | Single large steering change was not reliable | Robot could approach the first wall at an incorrect body angle | Added gradual search angles: `-5, -10, -15, -20, -24, -25` | More controlled first-wall search |
| First Wall Detection | Detecting the wall was initially treated too quickly as a corner | First detected wall is actually the beginning of the wall | Changed logic so the robot first confirms and aligns with the wall | First wall is now treated separately from corner detection |
| Robot-to-Wall Alignment | Straight wheels did not always mean the robot body was parallel to the wall | Robot could continue straight while physically pointing toward the wall | Added two-distance comparison and small steering corrections | Alignment routine successfully added |
| Alignment Tolerance | Alignment required a stable acceptance range | Small sensor differences occurred even when the robot was nearly parallel | Set `ALIGN_TOLERANCE = 15` | Stable alignment threshold |
| First Wall Following | Robot needed to maintain its position beside the wall | Distance changed while travelling along the wall | Added gentle toward/away steering corrections | First-wall following behavior improved |
| Wall End Detection | A single missing reading could falsely trigger a corner | Distance Sensor occasionally returned a lost reading while still beside the wall | Required multiple consecutive lost readings | Reduced false wall-end detection |
| Normal Wall Following | Robot needed a stable operating distance | Too-close and too-far conditions caused different path errors | Added distance ranges and correction speeds | Normal wall following integrated |
| Corner Direction | Earlier documentation described right corners | Current course navigation uses left corners | Updated corner direction and steering signs | Current corner logic uses negative steering values |
| Corner Method | Single steering movement did not produce reliable corners | Robot did not consistently complete the corner | Divided the corner into multiple steering and driving steps | Improved corner control |
| Corner Final Step | Equal steering steps were not enough | Final part of the corner required more steering | Increased the final steering movement | Final sequence: `-55, -55, -55, -80` |
| Distance Between Corner Steps | Smaller movement distance was insufficient | Robot needed more travel while steering | Increased movement between steering steps | `8 cm` used for each corner movement |
| Corner Speed | Lower speeds made the turn unnecessarily slow | Corner geometry remained usable at a higher speed | Increased corner speed | `CORNER_SPEED = 500` |
| Steering Speed | Steering response needed to be faster | Previous values slowed corner execution | Increased steering motor speed | `STEERING_SPEED = 470` |
| Recenter Speed | Steering recentering needed to be quicker | Slow recentering delayed transitions | Increased recenter speed | `RECENTER_SPEED = 670` |
| Distance Sensor Calibration | Sensor reading needed verification | Object was positioned approximately `14 cm` away | Compared physical distance with Port C reading | Approximately `140 mm` reading confirmed |
| New Wall Detection | Robot needed to identify the wall after each corner | One reading could be unreliable | Required repeated valid Distance Sensor readings | New-wall confirmation integrated |
| Corner Safety | Robot could become too close to a wall during a corner | Continuing forward could cause a collision | Added minimum corner distance check | `CORNER_TOO_CLOSE = 90` |
| Color Sensor Port | Color Sensor connection was corrected during testing | Sensor was physically connected to Port B | Program updated to use Port B | Correct port confirmed |
| Red/Green Detection | Robot needs to respond to both competition colors | Red and green require the same avoidance behavior | Added detection for both colors | Logic integrated into program |
| Color Avoidance | Robot needed to move away from a colored obstacle before passing it | Small reverse distance was not sufficient during testing | Reverse distance increased and multi-step right avoidance added | Current avoidance routine integrated; final field validation still required |
| Seven-Corner Sequence | Robot must complete the required navigation sequence | Individual wall-following and corner routines were developed separately | Main program configured for `7` corners | Integrated in main program |
| Return to Parking | Robot originally stopped after Corner 7 | A separate route was required to return to the starting parking area | Developed and calibrated a multi-stage return routine | Return routine integrated |
| Final Parking Reverse | Final position required additional backward movement | Robot needed to move farther into the parking area | Added final straight reverse movement | Final reverse set to `15 cm` |
| Full Integrated Run | Complete start-to-finish competition sequence | All major functions are now combined | Final competition-field testing required | Final validation pending |

---

# Current Tested and Calibrated Settings

## Steering

```python
STRAIGHT = -2

STEERING_SPEED = 470
RECENTER_SPEED = 670
```

---

## Parking Exit

```python
EXIT_STEER = -55

EXIT_SHORT_DEGREES = 140
EXIT_LONG_DEGREES = 380

PARK_STEERING_SPEED = 230
PARK_SLOW_SPEED = 200
PARK_FAST_SPEED = 240
```

---

## First Wall Approach

```python
FIRST_STRAIGHT_CM = 26
FIRST_STRAIGHT_SPEED = 400

APPROACH_DISTANCE_SCALE = 2.0

FIRST_SEARCH_ANGLES = (
    -5,
    -10,
    -15,
    -20,
    -24,
    -25
)

SEARCH_STEP_CM = 3
FINAL_SEARCH_CM = 6
```

---

## First Wall Alignment

```python
ALIGN_TEST_CM = 2
ALIGN_MOVE_CM = 3

ALIGN_TOLERANCE = 15
ALIGN_MAX_TRIES = 6

ALIGN_TOO_CLOSE = 120
ALIGN_TOO_FAR = 450

ALIGN_AWAY_STEER = 6
ALIGN_TOWARD_STEER = -10
```

---

## First Wall Following

```python
FIRST_WALL_MIN_DISTANCE = 150
FIRST_WALL_MAX_DISTANCE = 300

FIRST_WALL_END_DISTANCE = 500

FIRST_WALL_LOCK_COUNT = 5
FIRST_WALL_LOST_COUNT = 10
```

---

## Normal Wall Following

```python
MIN_DISTANCE = 150
MAX_DISTANCE = 250

WALL_LOST_DISTANCE = 450

LOST_COUNT_NEEDED = 8
WALL_LOCK_COUNT_NEEDED = 5

NORMAL_SPEED = 450
CLOSE_SPEED = 320
CORRECTION_SPEED = 380
```

---

## Corner Settings

```python
CORNER_STEP = -55
LAST_CORNER_STEP = -80

CORNER_STEP_DISTANCE_CM = 8

CORNER_SPEED = 500
STEERING_SPEED = 470
RECENTER_SPEED = 670

SEARCH_WALL_SPEED = 320

CORNER_TOO_CLOSE = 90

CORNERS_TO_RUN = 7
```

---

## Color Avoidance

```python
COLOR_REVERSE_CM = 10

COLOR_RIGHT_STEP = 55
COLOR_RIGHT_DRIVE_CM = 5
COLOR_RIGHT_STEPS = 3

COLOR_CLEAR_CM = 10
```

The Color Sensor is connected to:

```text
Port B
```

The Distance Sensor is connected to:

```text
Port C
```

---

# Return-to-Parking Calibration

The return-to-parking routine was developed separately before being added to the full competition program.

Current sequence:

1. Right steering and forward movement – approximately `45 cm`
2. Straight movement – approximately `10 cm`
3. Three left steering movements
4. Straight movement – approximately `15 cm`
5. Reverse with right steering `35` – approximately `10 cm`
6. Reverse with right steering `40` – approximately `10 cm`
7. Reverse with right steering `50` – approximately `20 cm`
8. Final positioning movement
9. Final straight reverse – approximately `15 cm`

Current values:

```python
RETURN_RIGHT_STEER = 35
RETURN_RIGHT_DRIVE_CM = 45

RETURN_STRAIGHT_AFTER_RIGHT_CM = 10

RETURN_LEFT_STEP = -55
RETURN_LEFT_STEP_DRIVE_CM = 8

RETURN_STRAIGHT_AFTER_LEFT_CM = 15

RETURN_REVERSE_RIGHT_1_STEER = 35
RETURN_REVERSE_RIGHT_1_CM = 10

RETURN_REVERSE_RIGHT_2_STEER = 40
RETURN_REVERSE_RIGHT_2_CM = 10

RETURN_REVERSE_RIGHT_3_STEER = 50
RETURN_REVERSE_RIGHT_3_CM = 20

RETURN_FINAL_FORWARD_CM = 2
RETURN_FINAL_REVERSE_CM = 15
```

---

# Confirmed Development Results

The following have been physically tested or calibrated during development:

- Straight steering calibration to `STRAIGHT = -2`
- Distance Sensor measurement behavior
- Parking exit movement
- Gradual first-wall approach
- First-wall body alignment method
- Multi-step corner geometry
- Steering and recentering speeds
- Distance-based wall-following logic
- Wall-loss confirmation logic
- Color Sensor connection on Port B
- Return-to-parking path developed through repeated physical adjustment

---

# Final Validation

The following should still be confirmed during the final competition-field test:

- Complete start-to-finish run without manual intervention
- Consistency of all seven corners in one run
- Wall-following consistency across the complete field
- Red obstacle avoidance under final field placement
- Green obstacle avoidance under final field placement
- Return-to-parking accuracy after the complete seven-corner run
- Repeatability across multiple consecutive competition runs

---

## Final Test Goal

The final validation goal is for the robot to complete the entire sequence autonomously:

```text
Parking Exit
     ↓
First Wall Approach
     ↓
Wall Alignment
     ↓
Wall Following
     ↓
Seven Corners
     ↓
Color Avoidance When Required
     ↓
Return to Parking
     ↓
Stop
```
