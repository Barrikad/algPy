# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:46:31 2020

@author: simon
"""

import code.API.feeding_api as fa
import unittest as ut

class TestFeedingAPI(ut.TestCase):
    def setUp(self):
        self.algeaSensor = EmulatedAlgeaSensor()
        self.pump = EmulatedPump(0.1,20,3600)
        self.feedingAPI = fa.FeedingAPI(self.algeaSensor, self.pump)
        
    def tearDown(self):
        self.feedingAPI = None
    
    def test_create_feeding_api(self):
        self.assertIsNotNone(self.feedingAPI)
        
    def test_retrieve_algea_density(self):
        self.algeaSensor.set_density(21)
        self.assertEqual(self.feedingAPI.get_current_algea_density(),21)
    
    def test_start_feeding(self):
        self.feedingAPI.start_feeding()
        self.assertEqual(self.pump.steps, 20)
    
    def test_retrieve_fed_algea(self):
        self.algeaSensor.set_density(21)
        self.feedingAPI.start_feeding()
        self.assertEqual(self.feedingAPI.total_fed_algea(),42)
    
    def test_continue_feeding(self):
        self.algeaSensor.set_density(21)
        self.feedingAPI.start_feeding()
        self.feedingAPI.continue_feeding()
        self.assertEqual(self.feedingAPI.total_fed_algea(),84)
    
    def test_send_back_water(self):
        self.feedingAPI.start_feeding()
        self.feedingAPI.continue_feeding()
        self.feedingAPI.send_back_water()
        self.assertEqual(self.pump.stepsDelta,0)
        

class EmulatedAlgeaSensor():
    
    def set_density(self, d):
        self.density = d
    
    def get_density(self):
        return self.density

class EmulatedPump():
    def __init__(self, mlPerStep, stepsPerPump, stepsPerRot):
        self.steps = 0
        self.stepsDelta = 0
        self.mlPerStep = mlPerStep
        self.stepsPerPump = stepsPerPump
        self.stepsPerRot = stepsPerRot
        self.direction = 1
        
    def get_pumped_volume(self):
        return self.stepsDelta * self.mlPerStep
    
    def clear_steps(self):
        self.stepsDelta = 0
    
    def reverse_direction(self):
        self.direction = - self.direction
        
    def pump(self, steps):
        self.stepsDelta = (self.stepsDelta + self.direction * steps) % self.stepsPerRot
        self.steps = (self.steps + self.direction * steps) % self.stepsPerRot
        
    def pump_standard_pump(self):
        self.stepsDelta = (self.stepsDelta + self.direction * self.stepsPerPump) % self.stepsPerRot
        self.steps = (self.steps + self.direction * self.stepsPerPump) % self.stepsPerRot