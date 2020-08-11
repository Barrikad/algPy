# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:38:05 2020

@author: simon
"""
import code.HAL.pump_API as pa
import time

pump = pa.Stepper(33, 20)

for i in range(100):
    pump.pump(3000)
    time.sleep(4)
    print("{} steps",3000*i)