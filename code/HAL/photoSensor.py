#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 20:49:03 2020

@author: mathildetannebaek
"""
import machine

class PhotoSensor:
    
    def __init__(self, algeaConstant, algaeZero, lookup, odPinNo):
        self.adc_V_lookup = lookup
        self.algeaConstant = algeaConstant
        self.algaeZero = algaeZero
        
        self.odPinNo = odPinNo
        self.adc = machine.ADC(machine.Pin(self.odPinNo))
        self.adc.atten(machine.ADC.ATTN_11DB)
        self.adc.width(machine.ADC.WIDTH_10BIT)
        
    
    def get_density(self):
        return self.adc_V_lookup[self.adc.read()]*self.algeaConstant + self.algaeZero
        