# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:51:31 2020

@author: simon
"""

class FeedingAPI:
    def __init__(self, algeaSensor, pump):
        self.algeaSensor = algeaSensor
        self.pump = pump
    
    def get_current_algea_density(self):
        """algea per ml
        """
        return self.algeaSensor.get_density()
    
    def start_feeding(self):
        self.pump.clear_steps()
        self.pump.pump_standard_pump()
        
    def continue_feeding(self):
        self.pump.pump_standard_pump()
    
    def total_fed_algea(self):
        return self.algeaSensor.get_density() * self.pump.get_pumped_volume()

    def send_back_water(self):
        self.pump.reverse_direction()
        self.pump.pump(self.pump.stepsDelta)
        self.pump.reverse_direction()