# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:52:40 2020

@author: simon
"""

temperaturePeriod = 100
comPeriod = 600
coolingPumpPeriod = 10
mlPerPumpCooling = 0.1
defaultThreshold = 20
defaultP = 2
defaultI = 0.2
defaultD = 1
defaultGoal = 14


class SystemController:
    def __init__(self,pid,temperatureController,clock,web):
        """pid should be the same as the one used in temp-controller
        """
        self.temperatureController = temperatureController
        self.clock = clock
        self.pid = pid
        self.temperatureController.set_pid_threshold(defaultThreshold)
        self.pid.set_P(defaultP)
        self.pid.set_I(defaultI)
        self.pid.set_D(defaultD)
        self.pid.set_goal(defaultGoal)
        self.clock.add_flag("temp", temperaturePeriod)
        self.clock.add_flag("coms", comPeriod)
        self.clock.add_flag("coolPump", coolingPumpPeriod)
        
        self.web = web
        self.toBePublishedTemp = []
    
    def system_tick(self):
        if(self.clock.check_flag("temp")):
            self.temperatureController.measure_temperature()
            self.temperatureController.correct_cooling_value()
        
        if(self.clock.check_flag("coms")):
            self._update_parameters()
            
            if(len(self.toBePublishedTemp) == 0):
                self.toBePublishedTemp = self.temperatureController.report_measurements()
            
            if(len(self.toBePublishedTemp) != 0):
                self.web.publish("Current Temperature",self.toBePublishedTemp[0])
                del self.toBePublishedTemp[0]
                
        if(self.clock.check_flag("coolPump")):
            self.temperatureController.pump()
                
    def _update_parameters(self):
        self.web.update_values()
        pW = self.web.get_latest_value("P parameter")
        iW = self.web.get_latest_value("I parameter")
        dW = self.web.get_latest_value("D parameter")
        gW = self.web.get_latest_value("Ideal Temp")
        
        if pW != -9999:
            self.pid.set_P(pW)
        if iW != -9999:
            self.pid.set_I(iW)
        if dW != -9999:
            self.pid.set_D(dW)
        if gW != -9999:
            self.pid.set_goal(gW)
            