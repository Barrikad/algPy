# -*- coding: utf-8 -*-

class PID:
    """A class for general pid controllers
    
    Contains methods for calculating pid-output, as well as
    methods for breaking down the impact of the P-term, I-term and D-term
    """
    
    def __init__(self):
        pass
    
    def set_P(self, p):
        self.P = p
    
    def set_I(self, i):
        self.I = i
    
    def set_D(self, d):
        self.D = d
    
    def set_goal(self, goal):
        self.goal = goal
    
    def give_measurement(self, measurement):
        self.measurement = measurement
    
    def get_correction(self):
        return self.measurement + 1