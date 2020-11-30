'''
    Stepper Motor interfacing with Raspberry Pi
    http:///www.electronicwings.com
'''
import RPi.GPIO as GPIO
from time import sleep
import sys
import blynklib

#assign GPIO pins for motor
motor_channel = (29,31,33,35)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor_channel, GPIO.OUT)
#auth_token = '4JR18qzs1AWkedrhF65mjwuASpBMpeGs'#rpiHOU
auth_token = "OXC2SHosxUj-wNyaeRMpEyd-JhHX7Vv9" #rpiDAL

# Initialize Blynk

blynk = blynklib.Blynk(auth_token)

@blynk.handle_event('write V1')
def write_handler_pin_handler(pin, value):
    Doorstep = (format(value[0]))
    if Doorstep =="1":
        print("open call")
        stepper('c')
        print("Door open")
    elif Doorstep =="2":
        print("open call")
        stepper('a')
        print("Door closed")

def stepper(direction):
    x=0
    y=1540
    while x<y:
        try:
            if(direction == 'c'):
                print('motor running clockwise\n')
                GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
                sleep(0.002)
                GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
                sleep(0.002)
                GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
                sleep(0.002)
                GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
                sleep(0.002)
                x=x+1

            elif(direction == 'a'):
                print('motor running anti-clockwise\n')
                GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
                sleep(0.002)
                GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
                sleep(0.002)
                GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
                sleep(0.002)
                GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
                sleep(0.002)
                x=x+1

                
        #press ctrl+c for keyboard interrupt
        except KeyboardInterrupt:
            #query for setting motor direction or exit
            motor_direction = input('select motor direction a=anticlockwise, c=clockwise or q=exit: ')
            #check for exit
            if(motor_direction == 'q'):
                print('motor stopped')
                sys.exit(0)
try:
    while True:
        blynk.run()

except KeyboardInterrupt:
    print("Quit")

