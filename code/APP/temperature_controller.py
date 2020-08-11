# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 09:39:37 2020

@author: simon
"""

class TemperatureController:
    """Class for connecting a PID controller to a temperatur regulating system
    """
    
    def __init__(self,coolingAPI,pid):
        self.coolingAPI = coolingAPI
        self.pid = pid
        self.unreportedMeasurements = []
    
    def set_pid_threshold(self,threshold):
        self.threshold = threshold
        
    def measure_temperature(self):
        self.unreportedMeasurements.append(self.coolingAPI.get_current_temperature())
        self.pid.give_measurement(self.unreportedMeasurements[-1])
    
    def report_measurements(self):
        """returns unreported measurements, then deletes them
        """
        unreportedMeasurements = self.unreportedMeasurements
        self.unreportedMeasurements = []
        return unreportedMeasurements
    
    def get_measurements(self):
        """reports unreported measurements without deleting them
        """
        return self.unreportedMeasurements
    
    def correct_cooling_value(self):
        if self.threshold < self.pid.get_correction():
            self.coolingAPI.intense_cooling(True)
        else:
            self.coolingAPI.intense_cooling(False)
        
        self.coolingAPI.set_throughflow(0.1*self.pid.get_correction())
    
    def pump(self):
        self.coolingAPI.pump_once()