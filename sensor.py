import time
import board
import digitalio
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7,GPIO.IN)
door_sensor = digitalio.DigitalInOut(board.D23)
door_sensor.direction = digitalio.Direction.INPUT

while True:
    val1 = door_sensor.value
    time.sleep(0.01)
    val2 = door_sensor.value
   
    if val1 and not val2:
        print("door closed")
       
    elif not val1 and val2:
        print("door open")
