# -*- coding: utf-8 -*-

class PID:
    """A class for general pid controllers
    
    Contains methods for calculating pid-output, as well as
    methods for breaking down the impact of the P-term, I-term and D-term
    """
    
    def __init__(self):
        self.maxErrors = 100
        self.errors = [0]*self.maxErrors
        self.errorCursor = 0
        self.P = 0 
        self.I = 0
        self.D = 0
        self.goal = 0
        self._p = 0
        self._errorSum = 0
        self._d = 0
    
    def set_P(self, p):
        self.P = p
    
    def set_I(self, i):
        self.I = i
    
    def set_D(self, d):
        self.D = d
    
    def set_goal(self, goal):
        self.goal = goal
    
    def set_max_errors(self,newMaxErrors):
        """Change the number of errors rembered by the pid
        
        Affects the integral term
        Saves all the previous values for which the new list has space
        """
        errorsTemp = [0]*newMaxErrors
        tempCursor = 0
        #while we have not reached the capacity of the new list, 
        #and have not exhausted the previous datapoints
        #while tempCursor < newMaxErrors && self.errorCursor > self.maxErrors:
            
    
    def give_measurement(self, measurement):
        overwrittenError = self.errors[self.errorCursor]
        self.errors[self.errorCursor] = (self.goal - measurement)
        
        if(len(self.errors) > 0):
            self._p = self.P*(self.errors[self.errorCursor])
            self._errorSum = self._errorSum + self.errors[self.errorCursor] - overwrittenError
        
        if(len(self.errors) > 1):
            self._d = self.D*(self.errors[self.errorCursor] - self.errors[self.errorCursor - 1])
            
        self.errorCursor = (self.errorCursor + 1) % self.maxErrors
    
    def get_correction(self):
        return self._p + self._errorSum*self.I + self._d
    
    def get_p_correction(self):
        return self._p 
    
    def get_i_correction(self):
        return self._errorSum*self.I
    
    def get_d_correction(self):
        return self._d
    
    def reset(self):
        self.P = 0 
        self.I = 0
        self.D = 0
        self.goal = 0
        self.errors = []
        self._p = 0
        self._errorSum = 0
        self._d = 0