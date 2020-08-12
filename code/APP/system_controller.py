# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:52:40 2020

@author: simon
"""

#pump experiment:
#600 cycles : 400ml
#2/3ml per cycle

feedingMusselsPeriod = 100 * 60 * 45 #45 min
feedingAlgaePeriod = 100 * 60 * 15 #15 min
temperaturePeriod = 100
comPeriod = 600
coolingPumpPeriod = 100
oledPeriod = 500
defaultThreshold = -20
defaultP = 2
defaultI = 0.2
defaultD = 1
defaultGoal = 14
algaeLevelToFeed = 9999 #algae (To Be decided! after experiments)


class SystemController:
    def __init__(self,pid,temperatureController,clock,web,oled):
        """pid should be the same as the one used in temp-controller
        """
        self.temperatureController = temperatureController
        self.clock = clock
        self.pid = pid
        self.oled = oled
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
        #feeding stuff added after temp-test
        #self.clock.add_flag("feedMussels", feedingMusselsPeriod)
        #self.clock.add_flag("feedAlgae", feedingAlgaePeriod)
        self.web = web
        self.toBePublishedTemp = []
    
    def system_tick(self):
        if(self.clock.check_flag("temp")):
            #self.write_to_oled("measuring","temperature","")
            self.temperatureController.measure_temperature()
            #self.write_to_oled("Correct","cooling","value")
            self.temperatureController.correct_cooling_value()
        
        if(self.clock.check_flag("coms")):
            #self.write_to_oled("Updating","PID","Parameters")
            self._update_parameters()
            
            if(len(self.toBePublishedTemp) == 0):
                #self.write_to_oled("Reporting","temp to be","published")
                self.toBePublishedTemp = self.temperatureController.report_measurements()
            
            if(len(self.toBePublishedTemp) != 0):
                #self.write_to_oled("Publishing","current","temperature")
                self.web.publish("Current Temperature",str(self.toBePublishedTemp[0]))
                del self.toBePublishedTemp[0]
        """
        if(self.clock.check_flag("feedMussels")):
            self.write_to_oled("Feeding","mussels","")
            self.feedingSystem.feedingMussels()
        
        if(self.clock.check_flag("feedAlgae")):
            self.write_to_oled("Feeding","algae","")
            self.feedingSystem.feedingAlgae()"""
            
        if(self.clock.check_flag("pumpCool")):
            #self.write_to_oled("Cool","pump","")
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
            