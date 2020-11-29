from time import sleep

import RPi.GPIO as GPIO


class Stepper:
    def __init__(self, motor_channel):
        self.motor_channel = motor_channel
        GPIO.setup(motor_channel, GPIO.OUT)

    def move_clockwise_steps(self, steps):
        for _ in range(steps):
            self.step_clockwise()

    def step_clockwise(self):
        GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
        sleep(0.002)
        GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
        sleep(0.002)
        GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
        sleep(0.002)
        GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
        sleep(0.002)

    def move_anti_clockwise_steps(self, steps):
        for _ in range(steps):
            self.step_anti_clockwise()

    def step_anti_clockwise(self):
        GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
        sleep(0.002)
        GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
        sleep(0.002)
        GPIO.output(self.motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
        sleep(0.002)
        GPIO.output(self.motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
        sleep(0.002)
