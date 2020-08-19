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
        self.algaeSum = 0
    
    def get_current_algea_density(self):
        """algea per ml
        """
        return self.algeaSensor.get_density() #algea/ml
    
    def start_feeding(self):
        self.pump.start_pump()
        self.algaeSum = 0
        self.pumpedVolume = 0
        
        
    def stop_feeding(self):
        self.pumpedVolume = self.pump.get_pumped_volume()
        self.pump.stop_pump()
    
    def total_fed_algea(self):
        algae_density = self.algeaSensor.get_density()
        pVolume = self.pump.get_pumped_volume()
        self.algaeSum += (pVolume - self.pumpedVolume) * algae_density
        self.pumpedVolume = pVolume
        return self.algaeSum

    def start_back_water(self):
        self.pump.reverse_direction()
        self.pump.start_pump()
    
    def stop_back_water(self):
        self.pump.stop_pump()
        self.pump.reverse_direction()
    
    def should_stop_back_water(self):
        return self.pump.get_pumped_volume() >= self.pumpedVolume + 3