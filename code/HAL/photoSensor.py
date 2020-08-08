#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 20:49:03 2020

@author: mathildetannebaek
"""
import machine

class PhotoSensor:
    def get_OD(self):
        #insert adc pin here:
        adcPin = 33
        
        adc = machine.ADC(machine.Pin(adcPin))
        adc.atten(machine.ADC.ATTN_11DB)
        
        return adc.read()
        