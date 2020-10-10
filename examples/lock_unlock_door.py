"""

Segmented switch that we are using (one option will be highlighted at a time)

UNLOCK sends a value of 1
LOCK sends a value of 2

+-----------------+
| UNLOCK |  LOCK  |
+-----------------+

"""

import blynklib
import RPi.GPIO as GPIO
from time import sleep

# insert your Auth Token here
BLYNK_AUTH = "OXC2SHosxUj-wNyaeRMpEyd-JhHX7Vv9"

blynk = blynklib.Blynk(BLYNK_AUTH)

UNLOCK = 1
LOCK = 2

UNLOCK_ANGLE = 180
LOCK_ANGLE = 0

SERVO_PIN = 11
PWM_FREQ = 50

# Initial state is locked
lock_state = LOCK

GPIO.setmode(GPIO.BOARD)

GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, PWM_FREQ)


# register handler for Virtual Pin V0 writing by Blynk App
@blynk.handle_event("write V0")
def write_virtual_pin_handler(pin, values):
    # values is a list that contains a single string (the write value)
    value = int(values[0])

    if value == UNLOCK:
        unlock_door()
    elif value == LOCK:
        lock_door()
    else:
        print("Invalid value")


def unlock_door():
    move_servo_to_angle(180)

    global lock_state
    lock_state = UNLOCK

    blynk.notify("Door has been unlocked")


def lock_door():
    move_servo_to_angle(0)

    global lock_state
    lock_state = LOCK

    blynk.notify("Door has been locked")


def move_servo_to_angle(angle):
    print(f"Changed angle to {angle}")
    duty_cycle = angle / 18 + 2
    servo.ChangeDutyCycle(duty_cycle)
    sleep(1)
    servo.ChangeDutyCycle(0)


if __name__ == "__main__":
    while True:
        blynk.run()
