"""

Segmented switch that we are using (one option will be highlighted at a time)

LOCK sends a value of 1
UNLOCK sends a value of 2

+-----------------+
|  LOCK  | UNLOCK |
+-----------------+

"""

import blynklib
import RPi.GPIO as GPIO
from time import sleep

BLYNK_AUTH = "OXC2SHosxUj-wNyaeRMpEyd-JhHX7Vv9"

blynk = blynklib.Blynk(BLYNK_AUTH)

LOCK = 1
UNLOCK = 2

LOCK_ANGLE = 0
UNLOCK_ANGLE = 90

SERVO_PIN = 14
PWM_FREQ = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, PWM_FREQ)


@blynk.handle_event("write V0")
def write_lock_virtual_pin_handler(pin, values):
    value = int(values[0])

    if value == LOCK:
        lock_door()
    elif value == UNLOCK:
        unlock_door()
    else:
        print("Invalid value")


def lock_door():
    move_servo_to_angle(LOCK_ANGLE)

    global lock_state
    lock_state = LOCK

    print("Door has been locked")


def unlock_door():
    move_servo_to_angle(UNLOCK_ANGLE)

    global lock_state
    lock_state = UNLOCK

    print("Door has been unlocked")


def move_servo_to_angle(angle):
    servo.ChangeDutyCycle(get_duty_cycle(angle))
    sleep(0.5)
    servo.ChangeDutyCycle(0)


def get_duty_cycle(angle):
    return angle / 18 + 2


if __name__ == "__main__":
    # Initial state is locked
    servo.start(get_duty_cycle(LOCK_ANGLE))
    lock_state = LOCK

    try:
        while True:
            blynk.run()
    finally:
        servo.stop()
        GPIO.cleanup()
