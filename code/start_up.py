# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:51:29 2020

@author: simon
"""

import machine as mc
import time
import os
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

subscribeKeys = ['P parameter','I parameter','D parameter','Integral memory','Derivative gap','Threshold','Feeding Level']
wifiName = "Simons_network"
wifiPassword = "85858585"
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'munz234'
ADAFRUIT_IO_KEY = 'here'

tempPin = 32
relayPin = 25
stepPinCool = 27
odPin = 33
feedPumpPin = 14
feedDirPin = 15
algaeLevelToFeed = 18000000 #algae (To Be decided! after experiments)

mlPerRev = 2/3
stepsPerRev = 1800
rps = 2

algaeConstant = -308487#tbd
algaeZero = 498933

def start():
    errorLog = open("errorLog.txt","r") 
    if os.stat("errorLog.txt").st_size != 0:
        errors = errorLog.readlines()
        for i in errors: 
            wc.publish("Feeding status", i)
    errorLog.close()
    
    clock = clk.Clock()
    tempSensor = ts.TemperatureSensor(tempPin)
    relay = rl.Relay(relayPin)
    algaeSensor = ps.PhotoSensor(algaeConstant, algaeZero, odPin)
    feedPump = pa.Stepper(feedPumpPin, stepsPerRev, rps, mlPerRev,feedDirPin)
    feedingAPI = fa.FeedingAPI(algaeSensor, feedPump)
    coolPump = pa.Stepper(stepPinCool,stepsPerRev, rps, mlPerRev)
    coolingAPI = ca.CoolingAPI(tempSensor,relay,coolPump)
    pid = pd.PID()
    oled = ol.Oled()
    tempCont = tc.TemperatureController(coolingAPI, pid)
    web = wc.Web(wifiName,wifiPassword,ADAFRUIT_IO_URL,ADAFRUIT_USERNAME,ADAFRUIT_IO_KEY)
    web.connectToWifi()
    web.connectToMQTT()
    web.subscribe_to_keys(subscribeKeys)
    sysCont = sc.SystemController(pid,tempCont,clock,web,oled,feedingAPI,algaeLevelToFeed)
    
    while(True):
        sysCont.system_tick()