# -*- coding: utf-8 -*-

import unittest as ut
import code.pid as pd

class Testpid(ut.TestCase):
    def setUp(self):
        self.pid = pd.PID()
        self.pid.set_P(1)
        self.pid.set_I(1)
        self.pid.set_D(1)
        self.pid.set_goal(30)
    
    def tearDown(self):
        self.pid = None
        
    def test_can_create_pid(self):
        self.assertIsNotNone(self.pid)
    
    def test_can_give_correction(self):
        self.pid.give_measurement(5)
        
        self.assertIsNotNone(self.pid.get_correction())
    
    def test_can_reset(self):
        self.pid.give_measurement(5)
        self.pid.reset()
        
        self.assertEqual(self.pid.get_correction(), 0)
        
    def test_corrects_by_proportional_on_error(self):
        self.pid.give_measurement(20)
        smallProportionalCorrection = self.pid.get_correction()
        self.setUp()
        self.pid.give_measurement(5)
        largeProportionalCorrection = self.pid.get_correction()
    
        self.assertGreater(largeProportionalCorrection, smallProportionalCorrection)

    def test_corrects_by_proportinal_on_p(self):
        self.pid.give_measurement(5)
        smallProportionalCorrection = self.pid.get_correction()
        self.setUp()
        self.pid.set_P(10)
        self.pid.give_measurement(5)
        largeProportionalCorrection = self.pid.get_correction()
        
        self.assertGreater(largeProportionalCorrection, smallProportionalCorrection)
    
    def test_corrects_by_integral_on_i(self):
        self.pid.give_measurement(5)
        self.pid.give_measurement(5)
        smallIntegralCorrection = self.pid.get_correction()
        self.setUp()
        
        self.pid.set_I(10)
        self.pid.give_measurement(5)
        self.pid.give_measurement(5)
        largeIntegralCorrection = self.pid.get_correction()
        
        self.assertGreater(largeIntegralCorrection, smallIntegralCorrection)
    
    def test_corrects_by_integral_over_time(self):
        self.pid.give_measurement(5)
        smallIntegralCorrection = self.pid.get_correction()
        self.setUp()
        
        self.pid.give_measurement(5)
        self.pid.give_measurement(5)
        self.pid.give_measurement(5)
        largeIntegralCorrection = self.pid.get_correction()
        
        self.assertGreater(largeIntegralCorrection, smallIntegralCorrection)
    
    def test_corrects_by_derivative_on_d(self):
        self.pid.give_measurement(5)
        self.pid.give_measurement(25)
        largeDerivativeCorrection = self.pid.get_correction()
        self.setUp()
        
        self.pid.set_D(10)
        self.pid.give_measurement(5)
        self.pid.give_measurement(25)
        smallDerivativeCorrection = self.pid.get_correction()
        
        self.assertGreater(largeDerivativeCorrection,smallDerivativeCorrection)
    
    def test_corrects_by_derivative_over_time(self):
        self.pid.give_measurement(10)
        self.pid.give_measurement(5)
        self.pid.give_measurement(25)
        smallDerivativeCorrection = self.pid.get_correction()
        self.setUp()
        
        self.pid.give_measurement(5)
        self.pid.give_measurement(10)
        self.pid.give_measurement(25)
        largeDerivativeCorrection = self.pid.get_correction()
        
        self.assertGreater(largeDerivativeCorrection,smallDerivativeCorrection)

