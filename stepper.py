import time
import board
import digitalio
 
enable_pin = digitalio.DigitalInOut(board.D18)
coil_A_1_pin = digitalio.DigitalInOut(board.D4)
coil_A_2_pin = digitalio.DigitalInOut(board.D17)
coil_B_1_pin = digitalio.DigitalInOut(board.D23)
coil_B_2_pin = digitalio.DigitalInOut(board.D24)
 
enable_pin.direction = digitalio.Direction.OUTPUT
coil_A_1_pin.direction = digitalio.Direction.OUTPUT
coil_A_2_pin.direction = digitalio.Direction.OUTPUT
coil_B_1_pin.direction = digitalio.Direction.OUTPUT
coil_B_2_pin.direction = digitalio.Direction.OUTPUT

enable_pin.value = True

def forward(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        i += 1
def backwards(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        i += 1
 
def setStep(w1, w2, w3, w4):
    coil_A_1_pin.value = w1
    coil_A_2_pin.value = w2
    coil_B_1_pin.value = w3
    coil_B_2_pin.value = w4
 
auth_token = '4JR18qzs1AWkedrhF65mjwuASpBMpeGs'

# Initialize Blynk

blynk = blynklib.Blynk(auth_token)

@blynk.handle_event('write V1')
def write_handler_pin_handler(pin, value):
    Doorstep = (format(value[0]))
    if Doorstep =="0":
        forward(int(2) / 1000.0, int(1500))
        print("Door open")
    elif Doorstep =="1":
        backwards(int(2) / 1000.0, int(1500))
        print("Door closed")
try:
    while True:
        blynk.run()

except KeyboardInterrupt:
    print("Quit")

# Reset GPIO settings
GPIO.cleanup()