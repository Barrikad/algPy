import code.HAL.temperature_sensor as temp
import code.HAL.oled as oled
import time

tempData = []
display = oled.Oled()

tempreader = temp.TemperatureSensor(32)

for i in range(200):
    value = tempreader.get_temperature()
    tempData.append(value)
    print(value)
    display.write_to_oled("temperature: ",str(value),"...")
    time.sleep(5)

print("-----------------")
print(tempData)


    
