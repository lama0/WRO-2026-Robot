from hub import port
import motor
import distance_sensor
import color_sensor
import color
import runloop
import math


# ==================================================
# HARDWARE
# ==================================================
STEER = port.A
COLOR_SENSOR = port.B
DISTANCE = port.C
DRIVE = port.E

STRAIGHT = -2
DRIVE_DIRECTION = -1

WHEEL_DIAMETER_CM = 5.6
DEG_PER_CM = 360 / (math.pi * WHEEL_DIAMETER_CM)


# ==================================================
# PARKING EXIT
# ==================================================
PARK_STEERING_SPEED = 230
PARK_SLOW_SPEED = 200
PARK_FAST_SPEED = 240

EXIT_STEER = -55
EXIT_SHORT_DEGREES = 140
EXIT_LONG_DEGREES = 380


# ==================================================
# FIRST WALL APPROACH
# ==================================================
FIRST_STRAIGHT_CM = 26
FIRST_STRAIGHT_SPEED = 400
APPROACH_DISTANCE_SCALE = 2.0

FIRST_SEARCH_ANGLES = (-5, -10, -15, -20, -24, -25)
SEARCH_STEP_CM = 3
SEARCH_STEP_SPEED = 220
FINAL_SEARCH_CM = 6

FIRST_WALL_DISTANCE = 500
FIRST_WALL_FOUND_COUNT = 3


# ==================================================
# FIRST WALL ALIGNMENT
# ==================================================
ALIGN_TEST_CM = 2
ALIGN_MOVE_CM = 3
ALIGN_TOLERANCE = 15
ALIGN_MAX_TRIES = 6
ALIGN_TOO_CLOSE = 120
ALIGN_TOO_FAR = 450
ALIGN_AWAY_STEER = 6
ALIGN_TOWARD_STEER = -10
ALIGN_SPEED = 220


# ==================================================
# FIRST WALL FOLLOWING
# ==================================================
FIRST_WALL_MIN_DISTANCE = 150
FIRST_WALL_MAX_DISTANCE = 300
FIRST_WALL_END_DISTANCE = 500
FIRST_WALL_LOCK_COUNT = 5
FIRST_WALL_LOST_COUNT = 10
FIRST_WALL_GENTLE_TOWARD = -5
FIRST_WALL_GENTLE_AWAY = 3
FIRST_WALL_GENTLE_STEER_SPEED = 300
FIRST_WALL_GENTLE_SPEED = 320


# ==================================================
# NORMAL WALL FOLLOWING
# ==================================================
MIN_DISTANCE = 150
MAX_DISTANCE = 250
WALL_LOST_DISTANCE = 450
LOST_COUNT_NEEDED = 8
WALL_LOCK_COUNT_NEEDED = 5
POST_CORNER_GUARD_CM = 12

NORMAL_SPEED = 450
CLOSE_SPEED = 320
CORRECTION_SPEED = 380
LOST_CHECK_SPEED = 340
TOWARD_WALL = -12


# ==================================================
# CORNERS
# ==================================================
CORNER_STEP = -55
LAST_CORNER_STEP = -80
CORNER_STEP_DISTANCE_CM = 8
CORNER_SPEED = 500
STEERING_SPEED = 470
RECENTER_SPEED = 670
SEARCH_WALL_SPEED = 320
WALL_FOUND_DISTANCE = 300
FOUND_COUNT_NEEDED = 2
NEW_WALL_SEARCH_MAX_CM = 30
CORNER_TOO_CLOSE = 90
CORNERS_TO_RUN = 7


# ==================================================
# COLOR AVOIDANCE
# ==================================================
COLOR_REVERSE_CM = 10
COLOR_RIGHT_STEP = 55
COLOR_RIGHT_DRIVE_CM = 5
COLOR_RIGHT_STEPS = 3
COLOR_CLEAR_CM = 10

COLOR_REVERSE_SPEED = 200
COLOR_DRIVE_SPEED = 220
COLOR_STEER_SPEED = 350
COLOR_CLEAR_SPEED = 240


# ==================================================
# RETURN TO PARKING
# ==================================================
RETURN_TURN_SPEED = 320
RETURN_STRAIGHT_SPEED = 300
RETURN_REVERSE_SPEED = 250

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

RETURN_FINAL_RIGHT_STEER = 5
RETURN_FINAL_FORWARD_CM = 2
RETURN_FINAL_REVERSE_CM = 15


# ==================================================
# BASIC MOVEMENT HELPERS
# ==================================================
async def set_steering(target, speed=STEERING_SPEED):
    current = motor.relative_position(STEER)
    difference = target - current

    if difference != 0:
        await motor.run_for_degrees(
            STEER,
            difference,
            speed,
            stop=motor.HOLD,
        )


async def force_straight():
    motor.stop(DRIVE)
    await runloop.sleep_ms(50)
    await set_steering(STRAIGHT, RECENTER_SPEED)
    await runloop.sleep_ms(50)


async def drive_forward_cm(cm, speed):
    degrees = int(cm * DEG_PER_CM)
    await motor.run_for_degrees(
        DRIVE,
        degrees * DRIVE_DIRECTION,
        speed,
    )


async def drive_backward_cm(cm, speed):
    degrees = int(cm * DEG_PER_CM)
    await motor.run_for_degrees(
        DRIVE,
        degrees * (-DRIVE_DIRECTION),
        speed,
    )


async def drive_approach_cm(cm, speed):
    degrees = int(cm * DEG_PER_CM * APPROACH_DISTANCE_SCALE)
    await motor.run_for_degrees(
        DRIVE,
        degrees * DRIVE_DIRECTION,
        speed,
    )


def get_distance():
    try:
        return distance_sensor.distance(DISTANCE)
    except OSError:
        return -1


async def stable_distance():
    values = []

    for _ in range(3):
        distance = get_distance()
        if distance != -1:
            values.append(distance)
        await runloop.sleep_ms(20)

    if not values:
        return -1

    return sum(values) // len(values)


# ==================================================
# COLOR SENSOR
# ==================================================
def get_target_color():
    try:
        detected = color_sensor.color(COLOR_SENSOR)

        if detected == color.RED:
            return "RED"
        if detected == color.GREEN:
            return "GREEN"

    except OSError:
        return None

    return None


async def avoid_color():
    detected = get_target_color()

    if detected is None:
        return False

    motor.stop(DRIVE)
    await force_straight()

    # Reverse away from the obstacle.
    await drive_backward_cm(COLOR_REVERSE_CM, COLOR_REVERSE_SPEED)

    # Three right steering steps with forward movement.
    for _ in range(COLOR_RIGHT_STEPS):
        await motor.run_for_degrees(
            STEER,
            COLOR_RIGHT_STEP,
            COLOR_STEER_SPEED,
            stop=motor.HOLD,
        )
        await drive_forward_cm(COLOR_RIGHT_DRIVE_CM, COLOR_DRIVE_SPEED)

    # Return the steering by the same total amount.
    for _ in range(COLOR_RIGHT_STEPS):
        await motor.run_for_degrees(
            STEER,
            -COLOR_RIGHT_STEP,
            COLOR_STEER_SPEED,
            stop=motor.HOLD,
        )

    await force_straight()
    await drive_forward_cm(COLOR_CLEAR_CM, COLOR_CLEAR_SPEED)
    motor.stop(DRIVE)
    await force_straight()

    return True


# ==================================================
# PARKING EXIT
# ==================================================
async def exit_parking():
    await force_straight()

    await motor.run_for_degrees(
        STEER,
        EXIT_STEER,
        PARK_STEERING_SPEED,
        stop=motor.HOLD,
    )
    await motor.run_for_degrees(
        DRIVE,
        EXIT_SHORT_DEGREES * DRIVE_DIRECTION,
        PARK_SLOW_SPEED,
    )

    await motor.run_for_degrees(
        STEER,
        EXIT_STEER,
        PARK_STEERING_SPEED,
        stop=motor.HOLD,
    )
    await motor.run_for_degrees(
        DRIVE,
        EXIT_LONG_DEGREES * DRIVE_DIRECTION,
        PARK_FAST_SPEED,
    )

    await motor.run_for_degrees(
        STEER,
        -EXIT_STEER,
        PARK_STEERING_SPEED,
        stop=motor.HOLD,
    )
    await motor.run_for_degrees(
        DRIVE,
        EXIT_SHORT_DEGREES * DRIVE_DIRECTION,
        PARK_SLOW_SPEED,
    )

    await motor.run_for_degrees(
        STEER,
        -EXIT_STEER,
        PARK_STEERING_SPEED,
        stop=motor.HOLD,
    )

    motor.stop(DRIVE)
    await force_straight()


# ==================================================
# FIRST WALL
# ==================================================
async def approach_first_wall():
    await force_straight()
    await drive_approach_cm(FIRST_STRAIGHT_CM, FIRST_STRAIGHT_SPEED)

    found_count = 0

    for angle in FIRST_SEARCH_ANGLES:
        await set_steering(angle, STEERING_SPEED)
        await drive_approach_cm(SEARCH_STEP_CM, SEARCH_STEP_SPEED)

        distance = get_distance()

        if distance != -1 and distance <= FIRST_WALL_DISTANCE:
            found_count += 1
        else:
            found_count = 0

        if found_count >= FIRST_WALL_FOUND_COUNT:
            motor.stop(DRIVE)
            return True

    await set_steering(FIRST_SEARCH_ANGLES[-1], STEERING_SPEED)
    await drive_approach_cm(FINAL_SEARCH_CM, SEARCH_STEP_SPEED)

    distance = get_distance()
    if distance != -1 and distance <= FIRST_WALL_DISTANCE:
        return True

    await force_straight()
    found_count = 0
    motor.run(DRIVE, 220 * DRIVE_DIRECTION)

    while True:
        distance = get_distance()

        if distance != -1 and distance <= FIRST_WALL_DISTANCE:
            found_count += 1
        else:
            found_count = 0

        if found_count >= FIRST_WALL_FOUND_COUNT:
            motor.stop(DRIVE)
            return True

        await runloop.sleep_ms(20)


async def align_robot_parallel_to_first_wall():
    for _ in range(ALIGN_MAX_TRIES):
        await force_straight()
        d1 = await stable_distance()

        if d1 == -1 or d1 > ALIGN_TOO_FAR:
            await set_steering(ALIGN_TOWARD_STEER, STEERING_SPEED)
            await drive_forward_cm(ALIGN_MOVE_CM, ALIGN_SPEED)
            continue

        if d1 < ALIGN_TOO_CLOSE:
            await set_steering(ALIGN_AWAY_STEER, STEERING_SPEED)
            await drive_forward_cm(ALIGN_MOVE_CM, ALIGN_SPEED)
            continue

        await force_straight()
        await drive_forward_cm(ALIGN_TEST_CM, ALIGN_SPEED)
        d2 = await stable_distance()

        if d2 == -1:
            continue

        delta = d2 - d1

        if abs(delta) <= ALIGN_TOLERANCE:
            await force_straight()
            return True

        if delta < 0:
            await set_steering(ALIGN_AWAY_STEER, STEERING_SPEED)
        else:
            await set_steering(ALIGN_TOWARD_STEER, STEERING_SPEED)

        await drive_forward_cm(ALIGN_MOVE_CM, ALIGN_SPEED)

    await force_straight()
    return False


async def first_wall_motion(distance):
    if distance != -1 and distance < FIRST_WALL_MIN_DISTANCE:
        await set_steering(
            FIRST_WALL_GENTLE_AWAY,
            FIRST_WALL_GENTLE_STEER_SPEED,
        )
        motor.run(DRIVE, FIRST_WALL_GENTLE_SPEED * DRIVE_DIRECTION)

    elif distance != -1 and distance <= FIRST_WALL_MAX_DISTANCE:
        await set_steering(
            STRAIGHT,
            FIRST_WALL_GENTLE_STEER_SPEED,
        )
        motor.run(DRIVE, NORMAL_SPEED * DRIVE_DIRECTION)

    else:
        await set_steering(
            FIRST_WALL_GENTLE_TOWARD,
            FIRST_WALL_GENTLE_STEER_SPEED,
        )
        motor.run(DRIVE, FIRST_WALL_GENTLE_SPEED * DRIVE_DIRECTION)


async def follow_first_wall_until_corner():
    await force_straight()

    wall_lock = 0

    while wall_lock < FIRST_WALL_LOCK_COUNT:
        if await avoid_color():
            wall_lock = 0
            await align_robot_parallel_to_first_wall()
            continue

        distance = get_distance()

        if distance != -1 and distance <= FIRST_WALL_END_DISTANCE:
            wall_lock += 1
        else:
            wall_lock = 0

        await first_wall_motion(distance)
        await runloop.sleep_ms(20)

    lost_count = 0

    while True:
        if await avoid_color():
            lost_count = 0
            await align_robot_parallel_to_first_wall()
            continue

        distance = get_distance()

        if distance == -1 or distance > FIRST_WALL_END_DISTANCE:
            lost_count += 1

            await set_steering(
                FIRST_WALL_GENTLE_TOWARD,
                FIRST_WALL_GENTLE_STEER_SPEED,
            )
            motor.run(DRIVE, FIRST_WALL_GENTLE_SPEED * DRIVE_DIRECTION)

            if lost_count >= FIRST_WALL_LOST_COUNT:
                motor.stop(DRIVE)
                await force_straight()
                return True

        else:
            lost_count = 0
            await first_wall_motion(distance)

        await runloop.sleep_ms(20)


# ==================================================
# NORMAL WALL FOLLOWING
# ==================================================
async def follow_wall_motion(distance):
    if distance == -1:
        await set_steering(STRAIGHT, STEERING_SPEED)
        motor.run(DRIVE, LOST_CHECK_SPEED * DRIVE_DIRECTION)

    elif distance < MIN_DISTANCE:
        await set_steering(STRAIGHT, STEERING_SPEED)
        motor.run(DRIVE, CLOSE_SPEED * DRIVE_DIRECTION)

    elif distance <= MAX_DISTANCE:
        await set_steering(STRAIGHT, STEERING_SPEED)
        motor.run(DRIVE, NORMAL_SPEED * DRIVE_DIRECTION)

    else:
        await set_steering(TOWARD_WALL, STEERING_SPEED)
        motor.run(DRIVE, CORRECTION_SPEED * DRIVE_DIRECTION)


async def follow_until_wall_lost():
    wall_lock = 0

    while wall_lock < WALL_LOCK_COUNT_NEEDED:
        if await avoid_color():
            wall_lock = 0
            continue

        distance = get_distance()

        if distance != -1 and distance < WALL_LOST_DISTANCE:
            wall_lock += 1
        else:
            wall_lock = 0

        await follow_wall_motion(distance)
        await runloop.sleep_ms(20)

    motor.stop(DRIVE)
    await force_straight()
    await drive_forward_cm(POST_CORNER_GUARD_CM, NORMAL_SPEED)

    lost_count = 0

    while True:
        if await avoid_color():
            lost_count = 0
            continue

        distance = get_distance()

        if distance == -1 or distance >= WALL_LOST_DISTANCE:
            lost_count += 1
        else:
            lost_count = 0

        if lost_count >= LOST_COUNT_NEEDED:
            motor.stop(DRIVE)
            await force_straight()
            return True

        await follow_wall_motion(distance)
        await runloop.sleep_ms(20)


# ==================================================
# CORNERS
# ==================================================
async def safe_corner_drive(cm):
    target_degrees = int(cm * DEG_PER_CM)
    motor.reset_relative_position(DRIVE, 0)
    motor.run(DRIVE, CORNER_SPEED * DRIVE_DIRECTION)

    while abs(motor.relative_position(DRIVE)) < target_degrees:
        distance = get_distance()

        if distance != -1 and distance <= CORNER_TOO_CLOSE:
            motor.stop(DRIVE)
            return False

        await runloop.sleep_ms(10)

    motor.stop(DRIVE)
    return True


async def turn_left_until_wall():
    await force_straight()

    for step in (CORNER_STEP, CORNER_STEP, CORNER_STEP, LAST_CORNER_STEP):
        await motor.run_for_degrees(
            STEER,
            step,
            STEERING_SPEED,
            stop=motor.HOLD,
        )

        if not await safe_corner_drive(CORNER_STEP_DISTANCE_CM):
            await force_straight()
            return False

    max_degrees = int(NEW_WALL_SEARCH_MAX_CM * DEG_PER_CM)
    motor.reset_relative_position(DRIVE, 0)

    found_count = 0
    motor.run(DRIVE, SEARCH_WALL_SPEED * DRIVE_DIRECTION)

    while abs(motor.relative_position(DRIVE)) < max_degrees:
        if await avoid_color():
            found_count = 0
            continue

        distance = get_distance()

        if distance != -1 and distance <= CORNER_TOO_CLOSE:
            motor.stop(DRIVE)
            await force_straight()
            return False

        if distance != -1 and distance <= WALL_FOUND_DISTANCE:
            found_count += 1
        else:
            found_count = 0

        if found_count >= FOUND_COUNT_NEEDED:
            motor.stop(DRIVE)
            await force_straight()
            return True

        await runloop.sleep_ms(20)

    motor.stop(DRIVE)
    await force_straight()
    return False


# ==================================================
# RETURN TO PARKING
# ==================================================
async def return_right_45():
    await force_straight()
    await set_steering(RETURN_RIGHT_STEER, STEERING_SPEED)
    await drive_forward_cm(RETURN_RIGHT_DRIVE_CM, RETURN_TURN_SPEED)
    motor.stop(DRIVE)
    await force_straight()


async def return_straight_10():
    await force_straight()
    await drive_forward_cm(
        RETURN_STRAIGHT_AFTER_RIGHT_CM,
        RETURN_STRAIGHT_SPEED,
    )
    motor.stop(DRIVE)
    await force_straight()


async def return_left_three_times():
    await force_straight()

    for _ in range(3):
        await motor.run_for_degrees(
            STEER,
            RETURN_LEFT_STEP,
            STEERING_SPEED,
            stop=motor.HOLD,
        )
        await drive_forward_cm(
            RETURN_LEFT_STEP_DRIVE_CM,
            RETURN_TURN_SPEED,
        )

    motor.stop(DRIVE)
    await force_straight()


async def return_straight_15():
    await force_straight()
    await drive_forward_cm(
        RETURN_STRAIGHT_AFTER_LEFT_CM,
        RETURN_STRAIGHT_SPEED,
    )
    motor.stop(DRIVE)
    await force_straight()


async def return_reverse_three_turns():
    await force_straight()

    await set_steering(RETURN_REVERSE_RIGHT_1_STEER, STEERING_SPEED)
    await drive_backward_cm(
        RETURN_REVERSE_RIGHT_1_CM,
        RETURN_REVERSE_SPEED,
    )

    await set_steering(RETURN_REVERSE_RIGHT_2_STEER, STEERING_SPEED)
    await drive_backward_cm(
        RETURN_REVERSE_RIGHT_2_CM,
        RETURN_REVERSE_SPEED,
    )

    await set_steering(RETURN_REVERSE_RIGHT_3_STEER, STEERING_SPEED)
    await drive_backward_cm(
        RETURN_REVERSE_RIGHT_3_CM,
        RETURN_REVERSE_SPEED,
    )

    motor.stop(DRIVE)


async def return_final():
    await set_steering(RETURN_FINAL_RIGHT_STEER, STEERING_SPEED)
    await runloop.sleep_ms(100)

    await force_straight()
    await drive_forward_cm(RETURN_FINAL_FORWARD_CM, RETURN_STRAIGHT_SPEED)

    motor.stop(DRIVE)
    await force_straight()

    await drive_backward_cm(RETURN_FINAL_REVERSE_CM, RETURN_REVERSE_SPEED)

    motor.stop(DRIVE)
    await force_straight()


async def return_to_parking():
    await return_right_45()
    await return_straight_10()
    await return_left_three_times()
    await return_straight_15()
    await return_reverse_three_turns()
    await return_final()


# ==================================================
# MAIN RACE
# ==================================================
async def main():
    # Steering wheels must be physically straight before starting.
    motor.reset_relative_position(STEER, 0)
    await force_straight()

    # Start from the parking area.
    await exit_parking()

    # Find and align with the first wall.
    await approach_first_wall()
    await align_robot_parallel_to_first_wall()
    await follow_first_wall_until_corner()

    # Corner 1.
    if not await turn_left_until_wall():
        motor.stop(DRIVE)
        return

    # Corners 2 to 7.
    for _ in range(2, CORNERS_TO_RUN + 1):
        await follow_until_wall_lost()

        if not await turn_left_until_wall():
            motor.stop(DRIVE)
            return

    # Return to the parking area after corner 7.
    motor.stop(DRIVE)
    await force_straight()
    await return_to_parking()

    motor.stop(DRIVE)
    await force_straight()


runloop.run(main())
