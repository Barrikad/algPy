# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:35:56 2020

@author: simon
"""

class CoolingAPI:
    """API for interacting with the thermometer and cooling
    """
    
    def __init__(self,temperatureSensor,relay,pump):
        self.temperatureSensor = temperatureSensor
        self.relay = relay
        self.stepsPerPump = 1
        self.pump = pump
        pump.start_pump()
    
    def intense_cooling(self,on):
        if on:
            self.relay.set_fan_high()
        else:
            self.relay.set_fan_low()
            
    def set_rps(self,rps):
        """set how much water the pump is putting through the cooler
        max is ??? and min is ???
        """
        self.pump.set_rps(rps)
    
    def get_current_temperature(self):
        return self.temperatureSensor.get_temperature()