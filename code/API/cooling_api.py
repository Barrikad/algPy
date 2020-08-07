# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:35:56 2020

@author: simon
"""

class CoolingAPI:
    """API for interacting with the thermometer and cooling
    """
    
    def __init__(self,temperatureSensor,relay):
        self.temperatureSensor = temperatureSensor
        self.relay = relay
    
    def intense_cooling(self,on):
        if on:
            self.relay.set_fan_high()
        else:
            self.relay.set_fan_low()
    
    def get_current_temperature(self):
        return self.temperatureSensor.get_temperature()