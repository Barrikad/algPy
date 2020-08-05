# -*- coding: utf-8 -*-

class PID:
    """A class for general pid controllers
    
    Contains methods for calculating pid-output, as well as
    methods for breaking down the impact of the P-term, I-term and D-term
    """
    
    def __init__(self):
        self.errors = []
    
    def set_P(self, p):
        self.P = p
    
    def set_I(self, i):
        self.I = i
    
    def set_D(self, d):
        self.D = d
    
    def set_goal(self, goal):
        self.goal = goal
    
    def give_measurement(self, measurement):
        self.errors.append(self.goal - measurement)
    
    def get_correction(self):
        if(len(self.errors) == 0):
            return 0
        
        p = self.P*(self.errors[-1])
        
        i = self.I*sum(self.errors)
        
        if(len(self.errors) > 1):
            d = self.D*(self.errors[-1] - self.errors[-2])
        else:
            d = 0
            
        return p + i + d
    
    def reset(self):
        self.P = 0 
        self.I = 0
        self.D = 0
        self.goal = 0
        self.errors = []