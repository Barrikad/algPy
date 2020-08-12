# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:23:27 2020

@author: simon
"""
import code.HAL.temperature_sensor as ts
import time

sensor = ts.TemperatureSensor(32)

for i in range(1000):
    print(sensor.get_temperature())
    time.sleep(1)