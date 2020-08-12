#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 20:49:03 2020

@author: mathildetannebaek
"""
import machine

class PhotoSensor:
    
    def __init__(self, algeaConstant,odPinNo):
        self.algeaConstant = algeaConstant
        self.odPinNo = odPinNo
        self.adc = machine.ADC(machine.Pin(self.odPinNo))
        self.adc.atten(machine.ADC.ATTN_11DB)
        
    def get_OD(self):
        return self.adc.read()
    
    def get_density(self):
        return self.get_OD()*self.algeaConstant
        