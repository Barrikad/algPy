# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:23:38 2020

@author: simon
"""

from machine import Timer

class Clock:
    """control the periodic setting of flags
    """
    def __init__(self):
        self.count = 0
        self.flagPeriods = {}
        self.flags = {}
        self.timer = Timer(-1)
        self.timer.init(period=10,mode=Timer.PERIODIC,callback=self.tick)
    
    def tick(self):
        self.count = (self.count + 1) % 1440000
        for i in self.flagPeriods.keys():
            if self.count % self.flagPeriods[i] == 0:
                self.flags[i] = True
    
    def add_flag(self,flagName,flagPeriod):
        """add a flag with the given name
        the flagPeriod is how many 10ms should pass between the flag being set
        """
        self.flags[flagName] = False
        self.flagPeriods[flagName] = flagPeriod
    
    def check_flag(self,flagName):
        return self.flags[flagName]