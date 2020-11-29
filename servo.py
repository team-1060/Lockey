from time import sleep

import RPi.GPIO as GPIO


class Servo:
    def __init__(self, servo_pin, pwm_freq):
        GPIO.setup(servo_pin, GPIO.OUT)
        self.servo = GPIO.PWM(servo_pin, pwm_freq)
        self.servo.start(0)

    def move_to_angle(self, angle):
        self.servo.ChangeDutyCycle(self.get_duty_cycle(angle))
        sleep(0.5)
        self.servo.ChangeDutyCycle(0)

    def get_duty_cycle(self, angle):
        return angle / 18 + 2.5

    def cleanup(self):
        self.servo.stop()
