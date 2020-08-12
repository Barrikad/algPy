#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 21:22:59 2020

@author: mathildetannebaek
"""
import code.HAL.ssd1306 as ssd1306
from machine import I2C, Pin

class Oled:
    def write_to_oled(self,line1,line2,line3):
        i2c = I2C(scl= Pin(22), sda=Pin(23), freq=100000)
        oled = ssd1306.SSD1306_I2C(128,32,i2c)
        
        oled.fill(0)
        oled.text(line1, 0, 8)
        oled.text(line2, 0, 16)
        oled.text(line3, 0, 24)
        oled.show()