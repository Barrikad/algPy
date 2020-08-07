import ssd1306
from machine import I2C, Pin

i2c = I2C(scl= Pin(22), sda=Pin(23), freq=100000)
oled = ssd1306.SSD1306_12C(128,32,i2c)
oled.fill(0)
oled.text("I", 0, 8)
oled.text("wrote", 8, 16)
oled.text("this!", 16, 24)
oled.show()