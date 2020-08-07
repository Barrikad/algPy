# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:35:49 2020

@author: simon
"""
import unittest as ut
import code.API.cooling_api as ca

class TestCoolingAPI(ut.TestCase):
    
    def setUp(self):
        self.temperatureSensor = EmulatedTemperatureSensor()
        self.relay = EmulatedRelay()
        self.coolingAPI = ca.CoolingAPI(self.temperatureSensor, self.relay)
    
    def tearDown(self):
        self.coolingAPI = None
    
    def test_create_cooling_api(self):
        self.assertIsNotNone(self.coolingAPI)
    
    def test_turn_on_intense_cooling(self):
        self.coolingAPI.intense_cooling(True)
        self.assertTrue(self.relay.fan_value)
    
    def test_turn_off_intense_cooling(self):
        self.coolingAPI.intense_cooling(True)
        self.coolingAPI.intense_cooling(False)
        self.assertFalse(self.relay.fan_value)
    
    def test_get_current_temperature(self):
        self.temperatureSensor.temperature = 15
        self.assertEqual(self.coolingAPI.get_current_temperature(),15)
    

class EmulatedTemperatureSensor:
    def __init__(self):
        self.temperature = 20
    
    def get_temperature(self):
        return self.temperature
    
class EmulatedRelay:
    def __init__(self):
        self.fan_value = False
    
    def set_fan_high(self):
        self.fan_value = True
    
    def set_fan_low(self):
        self.fan_value = False