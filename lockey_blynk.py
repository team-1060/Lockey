from time import time

import blynklib
import RPi.GPIO as GPIO

from servo import Servo
from stepper import Stepper

BLYNK_AUTH = "OXC2SHosxUj-wNyaeRMpEyd-JhHX7Vv9"

blynk = blynklib.Blynk(BLYNK_AUTH)

# Virtual Pins
LOCK_CONTROL_VPIN = 0
DOOR_CONTROL_VPIN = 1
DOOR_UNLOCKED_FOR_VPIN = 2
DOOR_OPEN_FOR_VPIN = 3
AUTO_LOCK_ENABLE_VPIN = 4
AUTO_LOCK_TIME_VPIN = 5
DOOR_OPEN_NOTIF_TIME_VPIN = 6

# Lock
LOCK = 1
UNLOCK = 2

LOCK_ANGLE = 0
UNLOCK_ANGLE = 90

SERVO_PIN = 14
PWM_FREQ = 50

# Door
CLOSE = 1
OPEN = 2

STEPPER_PINS = (5, 6, 13, 19)
STEPPER_STEPS = 1540

# RPi
GPIO.setmode(GPIO.BCM)
servo = Servo(SERVO_PIN, PWM_FREQ)
stepper = Stepper(STEPPER_PINS)

lock_state = None
door_last_unlocked_time = time()
auto_lock_timer = time()
auto_lock_enabled = False
auto_lock_timeout = 5

door_state = None
door_last_opened_time = time()
door_open_notification_timeout = 5
sent_door_open_notification = False

# Sync app state
@blynk.handle_event("connect")
def connect_handler():
    for pin in range(7):
        blynk.virtual_sync(pin)


# SETTINGS
@blynk.handle_event(f"write V{AUTO_LOCK_ENABLE_VPIN}")
def auto_lock_enable_handler(pin, values):
    global auto_lock_enabled

    value = int(values[0])
    if value == 1:
        auto_lock_enabled = True
    else:
        auto_lock_enabled = False

    print(f"Auto-Lock Enabled: {auto_lock_enabled}")


@blynk.handle_event(f"write V{AUTO_LOCK_TIME_VPIN}")
def auto_lock_time_handler(pin, values):
    global auto_lock_timeout

    value = int(values[0])
    auto_lock_timeout = value * 60

    print(f"Auto-Lock Time: {value}")


@blynk.handle_event(f"write V{DOOR_OPEN_NOTIF_TIME_VPIN}")
def door_open_notif_time_handler(pin, values):
    global door_open_notification_timeout

    value = int(values[0])
    door_open_notification_timeout = value * 60

    print(f"Door Open Notification Time: {value}")


# STATUS DISPLAYS
@blynk.handle_event(f"read V{DOOR_UNLOCKED_FOR_VPIN}")
def door_unlocked_for_handler(pin):
    time_unlocked_sec = time() - door_last_unlocked_time
    time_unlocked = int(time_unlocked_sec) // 60

    blynk.virtual_write(pin, time_unlocked)


@blynk.handle_event(f"read V{DOOR_OPEN_FOR_VPIN}")
def door_open_for_handler(pin):
    time_opened_sec = time() - door_last_opened_time
    time_opened = int(time_opened_sec) // 60

    blynk.virtual_write(pin, time_opened)


# LOCK (SERVO)
@blynk.handle_event(f"write V{LOCK_CONTROL_VPIN}")
def lock_control_handler(pin, values):
    value = int(values[0])

    if value == LOCK:
        lock_door()
    elif value == UNLOCK:
        unlock_door()
    else:
        print("Invalid value")


def lock_door():
    if door_state == OPEN:
        blynk.notify("Cannot lock door when door is open!")
        update_blynk_switch(LOCK_CONTROL_VPIN, UNLOCK)
        return

    global lock_state

    servo.move_to_angle(LOCK_ANGLE)

    lock_state = LOCK
    update_blynk_switch(LOCK_CONTROL_VPIN, LOCK)

    print("Lock State: Locked")


def unlock_door():
    global lock_state, door_last_unlocked_time, auto_lock_timer

    servo.move_to_angle(UNLOCK_ANGLE)

    lock_state = UNLOCK
    door_last_unlocked_time = auto_lock_timer = time()
    update_blynk_switch(LOCK_CONTROL_VPIN, UNLOCK)

    print("Lock State: Unlocked")


# DOOR (STEPPER)
@blynk.handle_event(f"write V{DOOR_CONTROL_VPIN}")
def door_control_handler(pin, values):
    global door_state

    value = int(values[0])

    if value == CLOSE:
        close_door()
    elif value == OPEN:
        open_door()
    else:
        print("Invalid value")


def close_door():
    global door_state, auto_lock_timer

    stepper.move_anti_clockwise_steps(STEPPER_STEPS)

    door_state = CLOSE
    auto_lock_timer = time()
    update_blynk_switch(DOOR_CONTROL_VPIN, CLOSE)

    print("Door State: Closed")


def open_door():
    if lock_state == LOCK:
        blynk.notify("Cannot open door when door is locked!")
        update_blynk_switch(DOOR_CONTROL_VPIN, CLOSE)
        return

    global door_state, door_last_opened_time, sent_door_open_notification

    stepper.move_clockwise_steps(STEPPER_STEPS)

    door_state = OPEN
    door_last_opened_time = time()
    sent_door_open_notification = False
    update_blynk_switch(DOOR_CONTROL_VPIN, OPEN)

    print("Door State: Open")


# MISC
def update_blynk_switch(pin, state):
    blynk.virtual_write(pin, state)


def check_for_auto_lock():
    if auto_lock_enabled and lock_state == UNLOCK and door_state == CLOSE:
        diff = time() - auto_lock_timer
        if diff > auto_lock_timeout:
            lock_door()


def check_for_door_open_notification():
    global sent_door_open_notification

    if door_state == OPEN:
        diff = time() - door_last_opened_time
        if diff > door_open_notification_timeout:
            if not sent_door_open_notification:
                door_open_time = int(diff) // 60
                blynk.notify(f"Door has been open for {door_open_time} minutes!")
                sent_door_open_notification = True


if __name__ == "__main__":
    try:
        while True:
            blynk.run()
            check_for_auto_lock()
            check_for_door_open_notification()

    finally:
        servo.cleanup()
        GPIO.cleanup()
