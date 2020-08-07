# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:03:53 2020

@author: simon
"""
import unittest as ut
import code.APP.system_controller as sc
import code.APP.pid as pd

class TestSystemController(ut.TestCase):
    
    def setUp(self):
        self.pid = pd.PID()
        self.clock = EmulatedClock()
        self.tempController = EmulatedTemperatureController()
        self.tempController.set_temperature(20)
        self.systemController = sc.SystemController(self.pid,self.tempController,self.clock)
    
    def test_create_system_controller(self):
        self.assertIsNotNone(self.systemController)
    
    def test_runs_measurement_and_correction(self):
        self.clock.set_flag("temp")
        self.systemController.system_tick()
        self.assertTrue(self.tempController.measured)
        self.assertTrue(self.tempController.corrected)
        
        
        
class EmulatedClock:
    def __init__(self):
        self.flags = {}
    
    def set_flag(self,flagName):
        self.flags[flagName] = True
    
    def add_flag(self,flagName,flagPeriod):
        self.flags[flagName] = False
    
    def check_flag(self,flagName):
        flagValue = self.flags[flagName]
        self.flags[flagName] = False
        return flagValue

class EmulatedTemperatureController:
    def __init__(self):
        self.measured = False
        self.corrected = False
    
    def set_pid_threshold(self,threshold):
        pass
    
    def set_temperature(self,temp):
        self.temp = temp
        
    def measure_temperature(self):
        self.measured = True
    
    def report_measurements(self):
        pass
    
    def get_measurements(self):
        return self.temp
    
    def correct_cooling_value(self):
        self.corrected = True