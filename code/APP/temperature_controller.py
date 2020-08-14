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
        self.temp = self.coolingAPI.get_current_temperature()
    
    def set_pid_threshold(self,threshold):
        self.threshold = threshold
        
    def measure_temperature(self):
        tSum = 0
        for i in range(5):
            tSum += self.coolingAPI.get_current_temperature()
        tSum /= 5
        self.pid.give_measurement(tSum)
        self.temp = tSum
    
    def get_latest_temperature(self):
        return self.temp
    
    def correct_cooling_value(self):
        if self.threshold > self.pid.get_correction():
            self.coolingAPI.intense_cooling(True)
        else:
            self.coolingAPI.intense_cooling(False)
        
        self.coolingAPI.set_rps(min(10,max(-0.1*self.pid.get_correction(),0)))
    