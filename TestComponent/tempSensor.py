#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:29:46 2020

@author: mathildetannebaek
"""
#Inspiration:
#https://learn.adafruit.com/thermistor/circuitpython

#We should get 10 analog readings per sec

import board
import analogio
import time

#Make sure the analog pin is A1 (else change the code)
thermistor = analogio.AnalogIn(board.A1)

while True:
    for i in range(1024):
        time.sleep(0.1)
        thermistor.value



