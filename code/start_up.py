# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:51:29 2020

@author: simon
"""

import machine as mc
import time
import code.API.clock as clk
import code.APP.temperature_controller as tc
import code.APP.system_controller as sc

def start():
    sc.web_test()