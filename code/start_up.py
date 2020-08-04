# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:51:29 2020

@author: simon
"""

import machine as mc
import time

def start():
    led = mc.Pin(14,mc.Pin.OUT)
    
    for i in range(60):
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.2)
    