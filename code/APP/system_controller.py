# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:52:40 2020

@author: simon
"""
import time
import code.API.WEBcoms as wb

temperaturePeriod = 100
defaultThreshold = 20
defaultP = 2
defaultI = 0.2
defaultD = 1
defaultGoal = 18

subscribeKeys = [b'Current Temperature',b'P parameter',b'I parameter',b'D parameter',b'Ideal Temp',b'FeedingStatus',b'OD']
wifiName = '"Mathilde - iPhone"'
wifiPassword = '"12345678"'
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'munz234'
ADAFRUIT_IO_KEY = b'aio_GzWu16y16PYJ8plYBlniKEOamHlg'

###############################QMTT_test#########################
web = wb.
#################################################################


class SystemController:
    def __init__(self,pid,temperatureController,clock):
        """pid should be the same as the one used in temp-controller
        """
        self.temperatureController = temperatureController
        self.clock = clock
        self.pid = pid
        self.temperatureController.set_pid_threshold(defaultThreshold)
        self.pid.set_P(defaultP)
        self.pid.set_I(defaultI)
        self.pid.set_D(defaultD)
        self.pid.set_goal(defaultGoal)
        self.clock.add_flag("temp", temperaturePeriod)
    
    def system_tick(self):
        if(self.clock.check_flag("temp")):
            self.temperatureController.measure_temperature()
            self.temperatureController.correct_cooling_value()