# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:17:29 2020

@author: simon
"""
import machine as mc
class Relay:
    def __init__(self,relay_pin_no):
        self.pin = mc.Pin(relay_pin_no,mc.Pin.OUT)
        
    def set_fan_high(self):
        self.pin.value(0)
    
    def set_fan_low(self):
        self.pin.value(1)