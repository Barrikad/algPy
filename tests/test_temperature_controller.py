# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 09:12:41 2020

@author: simon
"""

import unittest as ut
import code.APP.temperature_controller as tc
import code.APP.pid as pd

class TestTemperatureController(ut.TestCase):
    
    def setUp(self):
        self.pid = pd.PID()
        self.coolingAPI = EmulatedCoolingAPI()
        self.tempCont = tc.TemperatureController(self.coolingAPI,self.pid)
    
    def tearDown(self):
        self.tempCont = None
    
    def test_create_controller(self):
        self.assertIsNotNone(self.tempCont)
    
    def test_saves_measurements(self):
        self.coolingAPI.set_current_temperature(15)
        self.tempCont.measure_temperature()
        self.coolingAPI.set_current_temperature(20)
        self.tempCont.measure_temperature()
        
        loggedTemps = self.tempCont.report_measurements()
        self.assertEqual(loggedTemps,[15,20])
    
    def test_deletes_reported_measurments(self):
        self.coolingAPI.set_current_temperature(15)
        self.tempCont.measure_temperature()
        self.tempCont.measure_temperature()
        self.coolingAPI.set_current_temperature(20)
        self.tempCont.measure_temperature()
        
        self.tempCont.report_measurements()
        self.assertEqual(self.tempCont.report_measurements(),[])
    
    def test_uses_pid_for_cooling(self):
        #initialize pid and controller
        self.pid.set_P(1)
        self.pid.set_I(1)
        self.pid.set_D(1)
        self.pid.set_goal(30)
        self.pid.set_max_errors(100)
        self.tempCont.set_pid_threshold(20)
        
        #measure too cold values
        self.coolingAPI.set_current_temperature(20)
        self.tempCont.measure_temperature()
        self.coolingAPI.set_current_temperature(21)
        self.tempCont.measure_temperature()
        self.coolingAPI.set_current_temperature(22)
        self.tempCont.measure_temperature()
        self.tempCont.correct_cooling_value()
        self.assertTrue(self.coolingAPI.get_cooling_value())
        
        #measure too warm values
        self.coolingAPI.set_current_temperature(40)
        self.tempCont.measure_temperature()
        self.tempCont.measure_temperature()
        self.tempCont.correct_cooling_value()
        self.assertFalse(self.coolingAPI.get_cooling_value())
    
class EmulatedCoolingAPI:
    
    def __init__(self):
        pass
    
    def set_current_temperature(self, temperature):
        self.current_temperature = temperature
        
    def get_current_temperature(self):
        return self.current_temperature
    
    def intense_cooling(self,on):
        self.coolingValue = on
    
    def get_cooling_value(self):
        return self.coolingValue
        