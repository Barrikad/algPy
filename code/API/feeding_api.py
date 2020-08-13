# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:51:31 2020

@author: simon
"""

class FeedingAPI:
    def __init__(self, algeaSensor, pump):
        self.algeaSensor = algeaSensor
        self.pump = pump
        self.pumpedVolume = 0
    
    def get_current_algea_density(self):
        """algea per ml
        """
        return self.algeaSensor.get_density() #algea/ml
    
    def start_feeding(self):
        self.pump.start_pump()
        
    def stop_feeding(self):
        self.pumpedVolume = self.pump.get_pumped_volume()
        self.pump.stop_pump()
    
    def total_fed_algea(self):
        algae_density = 3000 #self.algeaSensor.get_density() 
        return algae_density * self.pump.get_pumped_volume()

    def start_back_water(self):
        self.pump.reverse_direction()
        self.pump.start_pump()
    
    def stop_back_water(self):
        self.pump.stop_pump()
        self.pump.reverse_direction()
    
    def should_stop_back_water(self):
        return self.pump.get_pumped_volume() >= self.pumpedVolume