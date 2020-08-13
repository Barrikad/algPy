# -*- coding: utf-8 -*-
import gc
class PID:
    """A class for general use pid controllers
    
    Contains methods for calculating pid-output, as well as
    methods for breaking down the impact of the P-term, I-term and D-term
    """
    
    def __init__(self):
        persFile = open("persistenceFile.txt","r") 
        values = persFile.readlines()
        
        self.maxErrors = float(values[4][:-1]) 
        self.errors = [0]*self.maxErrors
        self.errorGap = float(values[5][:-1]) 
        persFile.close()
        
        self._errorCursor = 0
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
        previousErrors = self.errors[max(0, self._errorCursor - newMaxErrors) : self._errorCursor]
        #Too complicated fuck me
        wrappingErrors = self.errors[self._errorCursor + max(0,  self.maxErrors - newMaxErrors) : self.maxErrors]
        del self.errors
        freeSpace = [0] * (newMaxErrors - len(previousErrors) - len(wrappingErrors))
        self._errorCursor = (len(wrappingErrors) + len(previousErrors)) % newMaxErrors
        self.errors = wrappingErrors + previousErrors + freeSpace
        self.maxErrors = newMaxErrors
        self._errorSum = sum(self.errors)
        del previousErrors
        del wrappingErrors
        del freeSpace
        gc.collect()
        
    def set_derivative_error_gap(self,gap_value):
        if gap_value >= self.maxErrors:
            raise IndexError("Can't increase error gap beyond size of saved errors")
        self.errorGap = gap_value
    
    def give_measurement(self, measurement):
        overwrittenError = self.errors[self._errorCursor]
        self.errors[self._errorCursor] = (self.goal - measurement)
        
        if(len(self.errors) > 0):
            self._p = self.P*(self.errors[self._errorCursor])
            self._errorSum = self._errorSum + self.errors[self._errorCursor] - overwrittenError
        
        if(len(self.errors) > 1):
            self._d = self.D*(self.errors[self._errorCursor] - self.errors[self._errorCursor - self.errorGap])
            
        self._errorCursor = (self._errorCursor + 1) % self.maxErrors
    
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