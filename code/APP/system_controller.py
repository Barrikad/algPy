# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:52:40 2020

@author: simon
"""
from machine import Timer

#pump experiment:
#600 cycles : 400ml
#2/3ml per cycle

feedingMusselsPeriod = 360000 #tbd
temperaturePeriod = 500
comPeriod = 800
oledPeriod = 500
defaultGoal = 17




class SystemController:
    def __init__(self,pid,temperatureController,clock,web,oled,feedingAPI):
        """pid should be the same as the one used in temp-controller
        """
        persFile = open("persistenceFile.txt","r") 
        persFile.seek(0,0)
        self.values = persFile.readlines() #values = [P,I,D,threshold,maxerrors,errorgap,leveltoFeed]
        defaultP = float(self.values[0][:-2])
        defaultI = float(self.values[1][:-2])
        defaultD = float(self.values[2][:-2])
        defaultThreshold = float(self.values[3][:-2])
        defaultMaxErrors = int(self.values[4][:-2])
        defaultErrorGap = int(self.values[5][:-2])
        algaeLevelToFeed = int(self.values[6][:-2])
        persFile.close()
        
        self.temperatureController = temperatureController
        self.clock = clock
        self.pid = pid
        self.oled = oled
        self.feedingAPI = feedingAPI
        self.temperatureController.set_pid_threshold(defaultThreshold)
        self.pid.set_P(defaultP)
        self.pid.set_I(defaultI)
        self.pid.set_D(defaultD)
        self.pid.set_goal(defaultGoal)
        self.pid.set_max_errors(defaultMaxErrors)
        self.pid.set_derivative_error_gap(defaultErrorGap)
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
            #try:
            self._update_parameters()
            print("sending data to web")
            tempTempLevel = self.temperatureController.get_latest_temperature()
            if tempTempLevel != self.previousTempLevel:
                print("sending temp")
                self.previousTempLevel = tempTempLevel
                self.web.publish("Current Temperature",str(self.previousTempLevel))
                        
            tempAlgaeLevel = self.feedingAPI.get_current_algea_density()
            if tempAlgaeLevel != self.previousAlgaeLevel:
                print("sending od")
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
        
        valuesPrev = self.values.copy()
        persFile = open("persistenceFile.txt","w") 
        persFile.seek(0,0)
        if pW != -9999:
            self.values[0] = str(pW)+'\r\n'
            if pW != pWprev:
                self.pid.set_P(pW)
        else:
            self.values[0] = valuesPrev[0]
        
        if iW != -9999:
            self.values[1] = str(iW)+'\r\n'
            if iW != iWprev:
                self.pid.set_I(iW)
        else:
            self.values[1] = valuesPrev[1]
                
        if dW != -9999:
            self.values[2] = str(dW)+'\r\n'
            if dW != dWprev:
                self.pid.set_D(dW)
        else:
            self.values[2] = valuesPrev[2]
       
        if im != -9999:
            self.values[4] = str(int(im))+'\r\n'
            if im != imprev:
                self.pid.set_max_errors(int(im))
        else:
            self.values[4] = valuesPrev[4]
        
        if dg != -9999:
            self.values[5] = str(int(dg))+'\r\n'
            if dg != dgprev:
                self.pid.set_derivative_error_gap(int(dg))
        else:
            self.values[5] = valuesPrev[5]
        
        if th != -9999:
            self.values[3] = str(th)+'\r\n'
            if th != thprev:
                self.temperatureController.set_pid_threshold(th)
        else:
            self.values[3] = valuesPrev[3]
        
        if fl != -9999:
            self.values[6] = str(int(fl)) + '\r\n'
            if fl != flprev:
                self.algaeLevelToFeed = int(fl)
        else:
            self.values[6] = valuesPrev[6]
        
        print("P ",self.pid.P)
        print("I ",self.pid.I)
        print("D ",self.pid.D)
        print("Tr ",self.temperatureController.threshold)
        
        persFile.write(''.join(self.values))
        
        persFile.close()
    