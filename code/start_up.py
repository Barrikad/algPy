# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:51:29 2020

@author: simon
"""

import machine as mc
import time
import code.HAL.photoSensor as ps
import code.HAL.pump_API as pa
import code.HAL.temperature_sensor as ts
import code.HAL.relay as rl
import code.HAL.oled as ol
import code.API.feeding_api as fa
import code.API.cooling_api as ca
import code.API.clock as clk
import code.API.web_coms as wc
import code.APP.pid as pd
import code.APP.temperature_controller as tc
import code.APP.system_controller as sc

subscribeKeys = ['P parameter','I parameter','D parameter','Integral memory','Derivative gap','Threshold']
wifiName = "Simons_network"
wifiPassword = "85858585"
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'munz234'
ADAFRUIT_IO_KEY = b'aio_lyvx0984GHTIxPxJtLuHCrZxkXA9'

tempPin = 32
relayPin = 25
stepPinCool = 33
odPin = 34#A0
feedPumpPin = 14
feedDirPin = 15

stepsPerPump = 3600 
mlPerPump = 2/3
stepsPerRev = 3600

algaeConstant = 3#tbd

def start():
    
    clock = clk.Clock()
    tempSensor = ts.TemperatureSensor(tempPin)
    relay = rl.Relay(relayPin)
    algaeSensor = ps.PhotoSensor(algaeConstant, odPin)
    feedPump = pa.Stepper(feedPumpPin, stepsPerPump, stepsPerRev, mlPerPump/stepsPerPump,feedDirPin)
    feedingAPI = fa.FeedingAPI(algaeSensor, feedPump)
    coolPump = pa.Stepper(stepPinCool,stepsPerPump,stepsPerRev,mlPerPump/stepsPerPump)
    coolingAPI = ca.CoolingAPI(tempSensor,relay,coolPump)
    pid = pd.PID()
    oled = ol.Oled()
    tempCont = tc.TemperatureController(coolingAPI, pid)
    web = wc.Web(wifiName,wifiPassword,ADAFRUIT_IO_URL,ADAFRUIT_USERNAME,ADAFRUIT_IO_KEY)
    web.connectToWifi()
    web.connectToMQTT()
    web.subscribe_to_keys(subscribeKeys)
    sysCont = sc.SystemController(pid,tempCont,clock,web,oled,feedingAPI)
    
    while(True):
        sysCont.system_tick()