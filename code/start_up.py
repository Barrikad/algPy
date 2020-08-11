# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:51:29 2020

@author: simon
"""

import machine as mc
import time
import code.HAL.pump_API as pa
import code.HAL.temperature_sensor as ts
import code.HAL.relay as rl
import code.API.cooling_api as ca
import code.API.clock as clk
import code.API.web_coms as wc
import code.APP.pid as pd
import code.APP.temperature_controller as tc
import code.APP.system_controller as sc

subscribeKeys = ['P parameter','I parameter','D parameter','Ideal Temp']
wifiName = "Simons_network"
wifiPassword = "85858585"
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'munz234'
ADAFRUIT_IO_KEY = b'CENSORED'

tempPin = 14
relayPin = 25
stepPinCool = 33


def start():
    clock = clk.Clock()
    tempSensor = ts.TemperatureSensor(tempPin)
    relay = rl.Relay(relayPin)
    pump = pa.Stepper(stepPinCool)
    coolingAPI = ca.CoolingAPI(tempSensor,relay,pump)
    pid = pd.PID()
    tempCont = tc.TemperatureController(coolingAPI, pid)
    web = wc.Web(wifiName,wifiPassword,ADAFRUIT_IO_URL,ADAFRUIT_USERNAME,ADAFRUIT_IO_KEY)
    web.connectToWifi()
    web.connectToMQTT()
    web.subscribe_to_keys(subscribeKeys)
    sysCont = sc.SystemController(pid,tempCont,clock,web)
    
    while(True):
        sysCont.system_tick()