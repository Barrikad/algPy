# -*- coding: utf-8 -*-

class PID:
    """A class for general pid controllers
    
    Contains methods for calculating pid-output, as well as
    methods for breaking down the impact of the P-term, I-term and D-term
    """
    
    def __init__(self):
        self.errors = []
        self.P = 0 
        self.I = 0
        self.D = 0
        self.goal = 0
        self._p = 0
        self._i = 0
        self._d = 0
    
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
        
        #update correction
        if(len(self.errors) > 0):
            self._p = self.P*(self.errors[-1])
            self._i = self.I*sum(self.errors)
        
        if(len(self.errors) > 1):
            self._d = self.D*(self.errors[-1] - self.errors[-2])
    
    def get_correction(self):
        return self._p + self._i + self._d
    
    def get_p_correction(self):
        return self._p 
    
    def get_i_correction(self):
        return self._i 
    
    def get_d_correction(self):
        return self._d
    
    def reset(self):
        self.P = 0 
        self.I = 0
        self.D = 0
        self.goal = 0
        self.errors = []
        self._p = 0
        self._i = 0
        self._d = 0