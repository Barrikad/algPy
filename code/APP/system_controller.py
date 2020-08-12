# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:52:40 2020

@author: simon
"""
from machine import Timer
import time

#pump experiment:
#600 cycles : 400ml
#2/3ml per cycle

feedingMusselsPeriod = 100 * 60 * 45 #45 min
temperaturePeriod = 100
comPeriod = 600
coolingPumpPeriod = 100
oledPeriod = 500
defaultThreshold = -20
defaultP = 2
defaultI = 0.2
defaultD = 1
defaultGoal = 14
algaeLevelToFeed = 450 #algae (To Be decided! after experiments)


class SystemController:
    def __init__(self,pid,temperatureController,clock,web,oled,feedingAPI):
        """pid should be the same as the one used in temp-controller
        """
        self.temperatureController = temperatureController
        self.clock = clock
        self.pid = pid
        self.oled = oled
        self.feedingAPI = feedingAPI
        #self.feedingSystem = feedingSystem(algaeLevelToFeed,stepsPerPump)
        self.temperatureController.set_pid_threshold(defaultThreshold)
        self.pid.set_P(defaultP)
        self.pid.set_I(defaultI)
        self.pid.set_D(defaultD)
        self.pid.set_goal(defaultGoal)
        self.clock.add_flag("temp", temperaturePeriod)
        self.clock.add_flag("coms", comPeriod)
        self.clock.add_flag("pumpCool",coolingPumpPeriod)
        self.clock.add_flag("oled",oledPeriod)
        self.clock.add_flag("feedMussels", feedingMusselsPeriod)
        self.offset_done = False
        self.feedingMussels = False
        self.web = web
        self.toBePublishedTemp = []
        self.previousAlgaeLevel = 0
        
        self.start_algae_offset()
    
    def system_tick(self):
        if(self.clock.check_flag("temp")):
            self.temperatureController.measure_temperature()
            self.temperatureController.correct_cooling_value()
        
        if(self.clock.check_flag("coms")):
            self._update_parameters()
            
            if(len(self.toBePublishedTemp) == 0):
                self.toBePublishedTemp = self.temperatureController.report_measurements()
            
            if(len(self.toBePublishedTemp) != 0):
                self.web.publish("Current Temperature",str(self.toBePublishedTemp[0]))
                del self.toBePublishedTemp[0]
            
            tempAlgaeLevel = self.feedingAPI.get_current_algea_density()
            if tempAlgaeLevel != self.previousAlgaeLevel:
                self.previousAlgaeLevel = tempAlgaeLevel
                self.web.publish("OD",str(self.previousAlgaeLevel))
            
            if self.feedingMussels:
                self.web.publish("Feeding status","Feeding mussels")
        
        if(self.clock.check_flag("feedMussels")):
            self.feedingAPI.start_feeding()
            self.feedingMussels = True
        
        if self.feedingMussels:
            if(self.feedingAPI.total_fed_algea() < algaeLevelToFeed):
                self.feedingAPI.continue_feeding()
            else:
                self.feedingMussels = False
        
        if(self.offset_done and self.clock.check_flag("feedAlgae")):
            self.feedingAPI.send_back_water()
            
        if(self.clock.check_flag("pumpCool")):
            self.temperatureController.pump()
        
        if(self.clock.check_flag("oled")):
            line1 = "p{}:t{}".format(int(10*self.pid._p) / 10,int(self.temperatureController.get_latest_temperature()*10)/10)
            line2 = "i{}".format(int(10*self.pid._error_sum*self.pid.I) / 10)
            line3 = "d{}".format(int(10*self.pid._d) / 10)
            self.oled.write_to_oled(line1,line2,line3)
        
                
    def _update_parameters(self):
        self.web.update_values()
        pW = self.web.get_latest_value("P parameter")
        iW = self.web.get_latest_value("I parameter")
        dW = self.web.get_latest_value("D parameter")
        gW = self.web.get_latest_value("Ideal Temp")
        th = self.web.get_latest_value("Threshold")
        
        if pW != -9999:
            self.pid.set_P(pW)
        if iW != -9999:
            self.pid.set_I(iW)
        if dW != -9999:
            self.pid.set_D(dW)
        if gW != -9999:
            self.pid.set_goal(gW)
        if th != -9999:
            self.temperatureController.set_pid_threshold(th)
    
    def start_algae_offset(self):
        def start_algae_timer(timer):
            self.clock.add_flag("feedAlgae", feedingMusselsPeriod)
            self.offset_done = True
        t1 = Timer(2)
        t1.init(period=10*feedingMusselsPeriod/2,mode=Timer.ONE_SHOT,callback=start_algae_timer)