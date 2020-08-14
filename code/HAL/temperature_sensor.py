# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:17:30 2020

@author: simon
"""
import machine as mc
import math

class TemperatureSensor:
    
    def __init__(self,lookup,TENP_SENS_ADC_PIN_NO):
        self.adc_V_lookup = lookup
        self.NOM_RES = 10000
        self.SER_RES = 9820
        self.TEMP_NOM = 25
        self.NUM_SAMPLES = 25
        self.THERM_B_COEFF = 3950
        self.ADC_MAX = 1023
        self.ADC_Vmax = 3.15
    
        adc = mc.ADC(mc.Pin(TENP_SENS_ADC_PIN_NO))
        adc.atten(mc.ADC.ATTN_11DB)
        adc.width(mc.ADC.WIDTH_10BIT)
        self.temp_sens = adc
    
    def get_temperature(self):
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, self.NUM_SAMPLES+1):
            raw_read.append(self.temp_sens.read())
    
        # Average of the NUM_SAMPLES and look it up in the table
        raw_average = sum(raw_read)/self.NUM_SAMPLES
        
        # Convert to resistance
        raw_average = self.ADC_MAX * self.adc_V_lookup[round(raw_average)]/self.ADC_Vmax
        resistance = (self.SER_RES * raw_average) / (self.ADC_MAX - raw_average)
        
        # Convert to temperature
        steinhart  = math.log(resistance / self.NOM_RES) / self.THERM_B_COEFF
        steinhart += 1.0 / (self.TEMP_NOM + 273.15)
        steinhart  = (1.0 / steinhart) - 273.15
        return steinhart