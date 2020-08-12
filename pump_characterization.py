# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:38:05 2020

@author: simon
"""
#import code.HAL.pump_API as pa
import time
from machine import I2C
from machine import Pin
from code.HAL.ssd1306 import SSD1306_I2C
import code.HAL.pump_API as pa


pump = pa.Stepper(33, 20)
i2c = I2C(scl= Pin(22), sda=Pin(23), freq=100000)
oled = SSD1306_I2C(128,32,i2c)

for i in range(1000):
    pump.pump(3600)
    oled.fill(0)
    oled.text("{}".format(i), 0, 8)
    oled.show()