# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:51:31 2020

@author: simon
"""

class thirdBucket:
    def __init__(self, pump):
        self.pump = pump
        self.pumpedVolume = 0
    
    def start_pumping(self):
        self.pump.start_pump()
        self.pumpedVolume = 0
        
    def stop_pumping(self):
        self.pumpedVolume = self.pump.get_pumped_volume()
        self.pump.stop_pump()
    
    def total_pumped_water(self):
        self.pumpedVolume = self.pump.get_pumped_volume()
        return self.pumpedVolume

    def start_back_water(self):
        self.pump.reverse_direction()
        self.pump.start_pump()
    
    def stop_back_water(self):
        self.pump.stop_pump()
        self.pump.reverse_direction()
    
    def should_stop_back_water(self):
        return self.pump.get_pumped_volume() >= self.pumpedVolume + 3