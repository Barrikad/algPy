# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:28:12 2020

@author: -
"""

import machine as mc

stp = mc.Pin(14)
pwm = mc.PWM(stp)
pwm.freq(1600)
pwm.duty(512)
