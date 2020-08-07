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
    
    def test_controller_saves_measurements(self):
        self.coolingAPI.set_current_temperature(15)
        self.tempCont.measure_temperature()
        self.coolingAPI.set_current_temperature(20)
        self.tempCont.measure_temperature()
        
        loggedTemps = self.tempCont.report_measurements()
        self.assertEqual(loggedTemps,[15,20])
    
    def test_controller_deletes_reported_measurments(self):
        self.coolingAPI.set_current_temperature(15)
        self.tempCont.measure_temperature()
        self.tempCont.measure_temperature()
        self.coolingAPI.set_current_temperature(20)
        self.tempCont.measure_temperature()
        
        self.tempCont.report_measurements()
        self.assertEqual(self.tempCont.report_measurements(),[])
    
class EmulatedCoolingAPI:
    
    def __init__(self):
        pass
    
    def set_current_temperature(self, temperature):
        self.current_temperature = temperature
        
    def get_current_temperature(self):
        return self.current_temperature