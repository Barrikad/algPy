# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 09:39:37 2020

@author: simon
"""

import code.APP.pid as pd

class TemperatureController:
    """Class for connecting a PID controller to a temperatur regulating system
    """
    
    def __init__(self,coolingAPI,pid):
        self.coolingAPI = coolingAPI
        self.pid = pid
        self.unreportedMeasurements = []
    
    def measure_temperature(self):
        self.unreportedMeasurements.append(self.coolingAPI.get_current_temperature())
        self.pid.give_measurement(self.unreportedMeasurements[-1])
    
    def report_measurements(self):
        unreportedMeasurements = self.unreportedMeasurements
        self.unreportedMeasurements = []
        return unreportedMeasurements