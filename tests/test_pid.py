# -*- coding: utf-8 -*-

import unittest as ut
import code.pid as pd

class Testpid(ut.TestCase):
    def setUp(self):
        self.pid = pd.PID()
    
    def tearDown(self):
        self.pid = None
        
    def test_can_create_pid(self):
        self.assertIsNotNone(self.pid)
        
    def test_corrects_negative_error(self):
        self.pid.set_P(1)
        self.pid.set_I(1)
        self.pid.set_D(1)
        self.pid.set_goal(30)
        
        self.pid.give_measurement(15)
        
        self.assertGreater(self.pid.get_correction(),15)
        
        self.pid.give_measurement(20)
        
        self.assertGreater(self.pid.get_correction(),20)
