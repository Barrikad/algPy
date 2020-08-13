# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:52:40 2020

@author: simon
"""
from machine import Timer

#pump experiment:
#600 cycles : 400ml
#2/3ml per cycle

feedingMusselsPeriod = 3000 #tbd
temperaturePeriod = 500
comPeriod = 800
oledPeriod = 500
defaultGoal = 14

persFile = open("persistenceFile.txt","r") 
values = persFile.readlines() #values = [P,I,D,threshold,maxerrors,errorgap]
defaultP = float(values[0][:-1])
defaultI = float(values[1][:-1])
defaultD = float(values[2][:-1])
defaultThreshold = float(values[3][:-1])
persFile.close()

class SystemController:
    def __init__(self,pid,temperatureController,clock,web,oled,feedingAPI,algaeLevelToFeed):
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
        self.clock.add_flag("oled",oledPeriod)
        self.clock.add_flag("feedMussels", feedingMusselsPeriod)
        self.clock.add_flag("feedAlgae", feedingMusselsPeriod,int(feedingMusselsPeriod/2))
        self.feedingMussels = False
        self.sendingBackWater = False
        self.web = web        
        self.previousAlgaeLevel = 0
        self.previousTempLevel = 0
        self.algaeLevelToFeed = algaeLevelToFeed
        
    
    def system_tick(self):
        #print("yo")
        if(self.clock.check_flag("temp") and not (self.feedingMussels or self.sendingBackWater)):
            print("Checking the temp")
            self.temperatureController.measure_temperature()
            self.temperatureController.correct_cooling_value()
        
        
        if(self.clock.check_flag("coms")):
            self._update_parameters()
            print("sending data to web")
            tempTempLevel = self.temperatureController.get_latest_temperature()
            if tempTempLevel != self.previousTempLevel:
                print("sending od")
                self.previousTempLevel = tempTempLevel
                self.web.publish("Current Temperature",str(self.previousTempLevel))
            
            tempAlgaeLevel = self.feedingAPI.get_current_algea_density()
            if tempAlgaeLevel != self.previousAlgaeLevel:
                print("sending temp")
                self.previousAlgaeLevel = tempAlgaeLevel
                self.web.publish("OD",str(self.previousAlgaeLevel))            
            
        
        if(self.clock.check_flag("feedMussels")):
            print("time to feed")
            self.feedingAPI.pump.set_rps(1)
            self.feedingAPI.start_feeding()
            self.feedingMussels = True
            self.web.publish("Feeding status", "Feeding mussels")
        
        if self.feedingMussels:
            print("feeding")
            if(self.feedingAPI.total_fed_algea() >= self.algaeLevelToFeed):
                print("done feeding")
                self.web.publish("Feeding status", "Stop feeding mussels")
                self.feedingAPI.stop_feeding()
                self.feedingMussels = False
        
        if(self.clock.check_flag("feedAlgae")):
            print("time to feed algae")
            self.feedingAPI.pump.set_rps(1)
            self.feedingAPI.start_back_water()
            self.sendingBackWater = True
            self.web.publish("Feeding status", "Feeding algae")
        
        if(self.sendingBackWater):
            print("sending back water")
            if self.feedingAPI.should_stop_back_water():
                print("stop sending back water")
                self.sendingBackWater = False
                self.feedingAPI.stop_back_water()
                self.web.publish("Feeding status", "Stop feeding algae")
        
        if(self.clock.check_flag("oled")):
            print("print to oled")
            line1 = "p{:.4}:t{:.4}".format(self.pid.get_p_correction(), int(self.temperatureController.get_latest_temperature()*10)/10)
            line2 = "i{:.4}".format(self.pid.get_i_correction())
            line3 = "d{:.4}".format(self.pid.get_d_correction())
            self.oled.write_to_oled(line1,line2,line3)
        
                
    def _update_parameters(self):
        pWprev = self.web.get_latest_value("P parameter")
        iWprev = self.web.get_latest_value("I parameter")
        dWprev = self.web.get_latest_value("D parameter")
        imprev = self.web.get_latest_value("Integral memory")
        dgprev = self.web.get_latest_value("Derivative gap")
        thprev = self.web.get_latest_value("Threshold")
        flprev = self.web.get_latest_value("Feeding Level")
        self.web.update_values()
        pW = self.web.get_latest_value("P parameter")
        iW = self.web.get_latest_value("I parameter")
        dW = self.web.get_latest_value("D parameter")
        im = self.web.get_latest_value("Integral memory")
        dg = self.web.get_latest_value("Derivative gap")
        th = self.web.get_latest_value("Threshold")
        fl = self.web.get_latest_value("Feeding Level")
        
        valuesPrev = values 
        persFile = open("persistenceFile.txt","w") 
        if pW != -9999 & pW != pWprev:
            self.pid.set_P(pW)
            values[0] = str(pW)+'\n'
        if iW != -9999 & iW != iWprev:
            self.pid.set_I(iW)
            values[1] = str(iW)+'\n'
        if dW != -9999 & dW != dWprev:
            self.pid.set_D(dW)
            values[2] = str(iW)+'\n'
        if im != -9999 & im != imprev:
            self.pid.set_max_errors(int(im))
            values[4] = str(im)+'\n'
        if dg != -9999 & dg != dgprev:
            self.pid.set_derivative_error_gap(int(dg))
            values[5] = str(dg)+'\n'
        if th != -9999 & th != thprev:
            self.temperatureController.set_pid_threshold(th)
            values[3] = str(th)+'\n'
        if fl != -9999 & fl != flprev:
            self.algaeLevelToFeed = fl
        
        if valuesPrev != values:
            persFile.write(''.join(values))
        
        persFile.close()
    
    def start_algae_offset(self):
        def start_algae_timer(timer):
            self.clock.add_flag("feedAlgae", feedingMusselsPeriod)
            self.offset_done = True
        t1 = Timer(2)
        t1.init(period=int(10*feedingMusselsPeriod/2),mode=Timer.ONE_SHOT,callback=start_algae_timer)
