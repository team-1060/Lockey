import blynklib
import RPi.GPIO as GPIO
from time import sleep
import sys

BLYNK_AUTH = 2VQHu9rMX4eQAXW_dBQ7NWBgBvyGrVN_
blynk = blynkilb.Blynk(BLYNK_AUTH)

#assign GPIO pins for motor
motor_channel = (29,31,33,35)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor_channel, GPIO.OUT)

CLOSE = 1
OPEN = 2

x = 0
y = 1560
@blynk.handle_event("Write V0")
def write_lock_virtual_pin_handler(pin,values):
    values = int(values[0])
    if value < CLOSE or value > OPEN:
        print('Invalid input')
    else:
        open_close_door(value)
    
def open_close_door(motor_direction):
    while x < y:
        try:
        if(motor_direction == CLOSE):
            print('motor running clockwise\n')
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
            sleep(0.02)
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
            sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
            sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
            sleep(0.02)
            x+= 1
            
        elif(motor_direction == OPEN):
            print('motor running anti-clockwise\n')
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
            sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
            sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
            sleep(0.02)
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
            sleep(0.02)
            x+= 1
            
            
        #press ctrl+c for keyboard interrupt
        except KeyboardInterrupt:
        #query for setting motor direction or exit
        motor_direction = input('select motor direction a=anticlockwise, c=clockwise or q=exit: ')
        #check for exit
        if(motor_direction == 'q'):
            print('motor stopped')
            sys.exit(0)


if __name__ == "__main__":
    try:
        while True:
            blynk.run()
    finally:
        GPIO.cleanup()
