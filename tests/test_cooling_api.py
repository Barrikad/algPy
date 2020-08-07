# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:35:49 2020

@author: simon
"""
import unittest as ut
import code.API.cooling_api as ca

class TestCoolingAPI(ut.TestCase):
    
    def setUp(self):
        self.coolingAPI = ca.CoolingAPI()
        self.temperatureSensor = EmulatedTemperatureSensor()
        self.relay = EmulatedRelay()
    
    def tearDown(self):
        self.coolingAPI = None
    
    def test_create_cooling_api(self):
        self.assertIsNotNone(self.coolingAPI)
    
    def test_turn_on_intense_cooling(self):
        self.coolingAPI.turn_on
    

class EmulatedTemperatureSensor:
    def __init__(self):
        pass
    
class EmulatedRelay:
    def __init__(self):
        pass