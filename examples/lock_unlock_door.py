"""

Segmented switch that we are using (one option will be highlighted at a time)

UNLOCK sends a value of 1
LOCK sends a value of 2

+-----------------+
| UNLOCK |  LOCK  |
+-----------------+

"""

import blynklib

# insert your Auth Token here
BLYNK_AUTH = "OXC2SHosxUj-wNyaeRMpEyd-JhHX7Vv9"

blynk = blynklib.Blynk(BLYNK_AUTH)

UNLOCK = 1
LOCK = 2

# register handler for Virtual Pin V0 writing by Blynk App
@blynk.handle_event("write V0")
def write_virtual_pin_handler(pin, values):
    # values is a list that contains a single string (the write value)
    value = int(values[0])

    if value == UNLOCK:
        print("Door has been unlocked") 
    elif value == LOCK:
        print("Door has been locked")
    else:
        print("Invalid value")

if __name__ == "__main__":
    # main loop that starts program and handles registered events
    while True:
        blynk.run()
