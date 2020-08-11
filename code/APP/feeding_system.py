#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:52:23 2020

@author: mathildetannebaek
"""

class FeedingSystem:
    def __init__(self, feedingAPI, algaeLevelToFeed, stepsPerPump):
        self.algaeLevelToFeed = algaeLevelToFeed
        self.stepsPerPump = stepsPerPump
        self.feedingAPI = feedingAPI(self.stepsPerPump)
        
    def feedingMussels(self):
        self.web.publish("OD",self.feedingAPI.get_current_algea_density())
        self.web.publish("Feeding status","Feeding mussels")
        self.feedingAPI.start_feeding()
        
        while self.feedingAPI.total_fed_algea() < self.algaeLevelToFeed:
            self.feedingAPI.continue_feeding()
        
        self.web.publish("Feeding status","Not feeding mussels")
    
    def feedingAlgae(self):
        self.web.publish("Feeding status","Pumping back musselwater")
        self.feedingAPI.send_back_water()
        
        self.web.publish("Feeding status","Not feeding mussels")
        
    
  