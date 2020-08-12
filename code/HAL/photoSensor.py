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
        
    def get_OD(self):
        
        adc = machine.ADC(machine.Pin(self.odPinNo))
        adc.atten(machine.ADC.ATTN_11DB)
        
        return adc.read()
    
    def get_density(self):
        return self.get_od*self.algeaConstant
        