import machine
import time

adcPin = 26

adc = machine.ADC(machine.Pin(adcPin))
adc.atten(machine.ADC.ATTN_11DB)

print("Initial testing")
for i in range(10):
    print(adc.read())
    

while True:
    print("...")
    for i in range(10):
        print(adc.read())
    time.sleep(15)
