
#The LED will be blinking if plugged in correct

#Insert LED-pin here:
ledPin = 27

import machine
import time
led = machine.Pin(ledPin, machine.Pin.OUT)
while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)

