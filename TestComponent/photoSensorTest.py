#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:11:07 2020

@author: mathildetannebaek
"""

#We should get different readings from the photosensor when 
#exposing it against different light. 10 readings per sec are made

#Note: i'm not sure if it prints the reading, else we need to insert that

#insert adc pin here:
adcPin = 33


import machine
import time

adc = machine.ADC(machine.Pin(adcPin))
adc.atten(machine.ADC.ATTN_11DB)

while True:
    for i in range(1024):
        time.sleep(0.1)
        adc.read()