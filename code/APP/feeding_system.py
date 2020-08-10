#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:52:23 2020

@author: mathildetannebaek
"""
import time

algaeLevelToFeed = 9999 #algae (To Be decided! after experiments)


class FeedingSystem:
    def __init__(self, feedingAPI):
        self.feedingAPI = feedingAPI
        
    def feeding(self):
        self.web.publish("OD",self.feedingAPI.get_current_algea_density())
        self.web.publish("Feeding status","Feeding mussels")
        self.feedingAPI.start_feeding()
        
        while self.feedingAPI.total_fed_algea() < algaeLevelToFeed:
            self.feedingAPI.continue_feeding()
        
        self.web.publish("Feeding status","Not feeding mussels")
        time.sleep(60*15) #15 minutes before pumping back water?
        
        self.web.publish("Feeding status","Pumping back mussels water")
        self.feedingAPI.send_back_water()
        
        self.web.publish("Feeding status","Not feeding mussels")
        
    
  