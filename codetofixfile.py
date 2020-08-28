# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 09:40:15 2020

@author: Bruger
"""
from machine import Timer

count = 0
def tick(timer):
    print(count)
    
t1 = Timer(2)
t1.init(period = 1000, mode=Timer.PERIODIC, callback = tick)

file = open("Offline_Data.txt","r")
foundData = False
s2 = " "
s1 = " "
while not foundData:
    count += 1
    s1Prev = s1
    s2Prev = s2
    s1=file.readline()
    file.readline()
    s2= file.readline()
    file.readline()
    bbb = False
    for s in ["Current Temperature","Feeding status","OD"]:
        bbb = bbb or (s in s2)
    foundData = not bbb
print("FOUND!!!!!!!!!!!!!!!!!!!!!!!!!")
file2 = open("ExpData.txt","w")
file2.write(s1Prev)
file2.write(s2Prev)
file2.write(s1)
while not((s2)==""):
    count += 1
    file2.write(s2)
    s2=file.readline()
    file.readline()
file.close()
file2.close()
