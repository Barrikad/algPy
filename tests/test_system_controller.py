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
        self.web = EmulatedWeb()
        self.pid = pd.PID()
        self.clock = EmulatedClock()
        self.tempController = EmulatedTemperatureController()
        self.tempController.set_temperature(20)
        self.systemController = sc.SystemController(self.pid,self.tempController,self.clock,self.web)
    
    def test_create_system_controller(self):
        self.assertIsNotNone(self.systemController)
    
    def test_runs_measurement_and_correction(self):
        self.clock.set_flag("temp")
        self.systemController.system_tick()
        self.assertTrue(self.tempController.measured)
        self.assertTrue(self.tempController.corrected)
    
    def test_updates_pid_values(self):
        self.web.set_incoming("P parameter",15.3)
        self.clock.set_flag("coms")
        self.systemController.system_tick()
        self.assertEqual(self.pid.P,15.3)
    
    def test_reports_temperature(self):
        self.tempController.set_temperature(15)
        self.clock.set_flag("temp")
        self.systemController.system_tick()
        self.clock.set_flag("coms")
        self.systemController.system_tick()
        self.assertTrue(self.web.pushedValues["Current Temperature"] == 15)
        

class EmulatedWeb():
    def __init__(self):
        self.values = { 'P parameter' : -9999,
                       'I parameter' : -9999,
                       'D parameter' : -9999,
                       'Ideal Temp' : -9999 }
        self.queue = []
        
        self.pushedValues = {}
    
    def connectToWifi():
        pass
    
    def connectToMQTT():
        pass
    
    def subscribe_to_keys(keys):
        pass
    
    def get_latest_value(self,key):
        return self.values[key]
    
    def set_incoming(self,key,value):
        self.queue.append((key,value))
    
    def update_values(self):
        if len(self.queue) > 0:
            xs = self.queue.pop()
            self.values[xs[0]] = xs[1]
    
    def publish(self,key, value):
        self.pushedValues[key] = value
        
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
        return [self.temp]
    
    def get_measurements(self):
        return [self.temp]
    
    def correct_cooling_value(self):
        self.corrected = True