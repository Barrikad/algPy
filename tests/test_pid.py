# -*- coding: utf-8 -*-

import unittest as ut
import code.APP.pid as pd

class Testpid(ut.TestCase):
    """class containing the pid-tests
    
    By default the pid runs with p=1, i=1, d=1, and goal=30
    """
    def setUp(self):
        self.pid = pd.PID()
        self.pid.set_P(1)
        self.pid.set_I(1)
        self.pid.set_D(1)
        self.pid.set_goal(30)
    
    def tearDown(self):
        self.pid = None
        
    def test_create_pid(self):
        self.assertIsNotNone(self.pid)
    
    def test_gives_correction(self):
        self.pid.give_measurement(5)
        
        self.assertIsNotNone(self.pid.get_correction())
    
    def test_reset(self):
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
    
    def test_gives_correction_terms(self):
        self.pid.give_measurement(1)
        self.pid.give_measurement(2)
        self.pid.give_measurement(3)
        
        self.assertEqual(self.pid.get_p_correction(),27)
        self.assertEqual(self.pid.get_i_correction(),84)
        self.assertEqual(self.pid.get_d_correction(),-1)
    
    def test_set_max_errors(self):
        self.pid.set_max_errors(50)
        for i in range(50):
            self.pid.give_measurement(0)
        largeIntegralCorrection = self.pid.get_i_correction()
        
        self.pid.give_measurement(10)
        self.pid.give_measurement(10)
        smallIntegralCorrection = self.pid.get_i_correction()
        
        self.assertGreater(largeIntegralCorrection, smallIntegralCorrection)
        
    def test_deletes_errors_when_decreasing_max(self):
        for i in range(100):
            self.pid.give_measurement(20)
        self.pid.set_max_errors(50)
        self.assertEqual(self.pid.get_i_correction(), 500)
    
    def test_saves_errors_when_increasing_max(self):
        self.pid.set_max_errors(100)
        for i in range(100):
            self.pid.give_measurement(20)
        self.pid.set_max_errors(150)
        self.assertEqual(self.pid.get_i_correction(),1000)
        