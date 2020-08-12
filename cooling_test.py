from code.HAL.temperature_sensor import get_temperature
import oled
import time

tempData = []
display = Oled()

for i in range (200)
    value = get_temperature()
    tempData.append(value)
    print(value)
    display.write_to_oled("temperature: ",value," ")
    time.sleep(15)

print("-----------------")
print(tempData)


    
