import machine
import time

adcPin = 33
pumpPin = 27

pPin = machine.Pin(pumpPin,machine.Pin.OUT)

def pump(timer):
    pPin.value(1)
    time.sleep_us(100)
    pPin.value(0)
    time.sleep_us(100) 


adc = machine.ADC(machine.Pin(adcPin))
adc.atten(machine.ADC.ATTN_11DB)

clock = machine.Timer(0)
clock.init(period = 1, mode = machine.Timer.PERIODIC, callback = pump)

print("Initial testing")
for i in range(10):
    print(adc.read())
    

for j in range(10):
    for i in range(10):
        print(adc.read())
        time.sleep(1)

