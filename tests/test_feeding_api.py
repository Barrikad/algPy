# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:46:31 2020

@author: simon
"""

import code.API.feeding_api as fa
import unittest as ut

class TestFeedingAPI(ut.TestCase):
    def setUp(self):
        self.feedingAPI = fa.FeedingAPI()
        
    def tearDown(self):
        self.feedingAPI = None
    
    def test_create_feeding_api(self):
        self.assertIsNotNone(self.feedingAPI)
        
    def test_retrieve_algea_density(self):
        self.feedingAPI.measure_algea_density()
        