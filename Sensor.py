from time import sleep
import RPI.GPIO as GPIO

class Sensor:
    
    def _init_(self,motor_channel):
        self.motor_channel = motor_channel
        GPIO.setup(motor_channel,GPIO.in)
    
    #Status of the door (OPEN/CLOSED)    
    def status(self):
        sleep(0.002)
        if GPIO.input(self.motor_channel):
            return "door open"
           
        elif GPIO.input(self.motor_channel) == False:
            return "door closed"

