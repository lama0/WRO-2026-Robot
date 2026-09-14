# WRO 2026 Robot – Testing Log

This file records the main tests, observations, modifications, and results made during robot development.

| Test | Initial Setting / Problem | Observation | Modification | Result / Status |
|---|---|---|---|---|
| Straight Steering | `STRAIGHT = 0` | Robot drifted slightly to the left | Changed steering calibration gradually | `STRAIGHT = -2` produced a more stable straight path |
| Corner Method | Single steering angle | Robot did not complete the corner consistently | Divided the corner into multiple steering steps | Improved corner control |
| Corner Final Step | `55°, 55°, 55°, 55°` | Final part of the turn was not sufficient | Increased final steering step | Final sequence: `55°, 55°, 55°, 80°` |
| Distance Between Corner Steps | `5 cm` | Movement between steering steps was too short | Increased movement distance | `8 cm` produced a smoother corner |
| Corner Speed | Lower speed | Corner execution was too slow | Increased movement and steering speeds | Faster corner while keeping the tested geometry |
| Distance Sensor Calibration | Sensor accuracy needed verification | Object placed at approximately `14 cm` | Read Port C value | Sensor returned `140 mm` – Verified |
| Parking Exit to Corner | Corner started too early | Robot needed more space before turning | Added straight movement after parking exit | `13 cm` straight movement improved the approach |
| New Wall Detection | Robot needs to recognize the next wall after turning | Physical testing performed with Distance Sensor | Continue turning right until valid wall readings are detected | Current logic uses repeated valid readings before stopping |
| Full Lap Test | Complete course | Not yet finalized | Final physical testing required | Pending |
| Red/Green Obstacle Test | Color Sensor – Port B | Final avoidance strategy not yet verified | Physical testing required | Pending |

---

## Current Tested Settings

- `STRAIGHT = -2`
- `CORNER_STEP = 55`
- `LAST_CORNER_STEP = 80`
- `CORNER_STEP_DISTANCE_CM = 8`
- `CORNER_SPEED = 400`
- `STEERING_SPEED = 400`
- `RECENTER_SPEED = 600`
- `SEARCH_WALL_SPEED = 340`
- Straight movement after parking exit = `13 cm`

---

## Remaining Tests

- Full lap completion
- Wall-following consistency
- Repeated corner reliability
- Final red obstacle avoidance
- Final green obstacle avoidance
- Final competition run
