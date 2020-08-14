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
ADAFRUIT_IO_KEY = 'aio_utLL84g8XHwfI6tqjryLw3si4172'

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
lookup = [0.02470588, 0.02058824, 0.04117647, 0.06176471, 0.06588235, 0.07, 0.07411765, 0.07720589, 0.08029412, 0.08338236, 0.08647059, 0.09058825, 0.09470588, 0.09882354, 0.1012941, 0.1037647, 0.1062353, 0.1087059, 0.1111765, 0.117353, 0.1235294, 0.126, 0.1284706, 0.1309412, 0.1334118, 0.1358824, 0.14, 0.1441177, 0.1482353, 0.1513235, 0.1544118, 0.1575, 0.1605882, 0.1636765, 0.1667647, 0.1698529, 0.1729412, 0.1770588, 0.1811765, 0.1852941, 0.1883824, 0.1914706, 0.1945588, 0.1976471, 0.2017647, 0.2058824, 0.21, 0.2130883, 0.2161765, 0.2192647, 0.222353, 0.2264706, 0.2305882, 0.2347059, 0.2377941, 0.2408824, 0.2439706, 0.2470588, 0.2501471, 0.2532353, 0.2563236, 0.2594118, 0.2625, 0.2655883, 0.2686765, 0.2717647, 0.2758824, 0.28, 0.2841177, 0.2872059, 0.2902942, 0.2933824, 0.2964706, 0.2995588, 0.3026471, 0.3057353, 0.3088235, 0.3119118, 0.315, 0.3180882, 0.3211765, 0.3252941, 0.3294118, 0.3335294, 0.3366177, 0.3397059, 0.3427941, 0.3458824, 0.3489706, 0.3520588, 0.3551471, 0.3582353, 0.362353, 0.3664706, 0.3705883, 0.3747059, 0.3788235, 0.3829412, 0.3860294, 0.3891177, 0.3922059, 0.3952941, 0.3983824, 0.4014706, 0.4045588, 0.4076471, 0.4107353, 0.4138236, 0.4169118, 0.42, 0.4241177, 0.4282353, 0.432353, 0.4364706, 0.4405883, 0.4447059, 0.4477942, 0.4508824, 0.4539706, 0.4570589, 0.4601471, 0.4632353, 0.4663236, 0.4694118, 0.4735294, 0.4776471, 0.4817647, 0.4838236, 0.4858823, 0.4879412, 0.4900001, 0.4920588, 0.4941177, 0.4982353, 0.502353, 0.5064706, 0.5095589, 0.5126471, 0.5157353, 0.5188236, 0.5229412, 0.5270588, 0.5311765, 0.5342648, 0.537353, 0.5404412, 0.5435295, 0.547647, 0.5517647, 0.5558824, 0.5589706, 0.5620589, 0.5651471, 0.5682353, 0.5723529, 0.5764706, 0.5805883, 0.5836765, 0.5867648, 0.589853, 0.5929412, 0.5960294, 0.5991177, 0.6022058, 0.6052941, 0.6083823, 0.6114706, 0.6145588, 0.6176471, 0.6207353, 0.6238235, 0.6269117, 0.63, 0.6341177, 0.6382353, 0.642353, 0.6454412, 0.6485294, 0.6516176, 0.6547059, 0.6588235, 0.6629412, 0.6670588, 0.670147, 0.6732353, 0.6763235, 0.6794118, 0.6835294, 0.6876471, 0.6917647, 0.6948529, 0.6979412, 0.7010294, 0.7041177, 0.7072059, 0.7102942, 0.7133823, 0.7164706, 0.7195588, 0.7226471, 0.7257353, 0.7288236, 0.7329412, 0.7370589, 0.7411765, 0.7442647, 0.747353, 0.7504412, 0.7535295, 0.7566176, 0.7597059, 0.7627941, 0.7658824, 0.7689706, 0.7720589, 0.7751471, 0.7782353, 0.7823529, 0.7864707, 0.7905883, 0.7936765, 0.7967648, 0.7998529, 0.8029412, 0.8070589, 0.8111765, 0.8152942, 0.8183824, 0.8214706, 0.8245588, 0.8276471, 0.8307353, 0.8338236, 0.8369118, 0.8400001, 0.8441177, 0.8482353, 0.852353, 0.8554412, 0.8585295, 0.8616177, 0.8647059, 0.8677941, 0.8708824, 0.8739706, 0.8770589, 0.8801471, 0.8832354, 0.8863235, 0.8894118, 0.8935295, 0.8976471, 0.9017648, 0.9042353, 0.906706, 0.9091764, 0.9116471, 0.9141177, 0.9172059, 0.9202942, 0.9233824, 0.9264707, 0.9295588, 0.9326471, 0.9357353, 0.9388236, 0.9429413, 0.9470588, 0.9511765, 0.9542647, 0.957353, 0.9604412, 0.9635295, 0.9666177, 0.969706, 0.9727942, 0.9758824, 0.9789706, 0.9820589, 0.9851471, 0.9882354, 0.9913236, 0.9944118, 0.9975, 1.000588, 1.004706, 1.008824, 1.012941, 1.016029, 1.019118, 1.022206, 1.025294, 1.029412, 1.033529, 1.037647, 1.040735, 1.043824, 1.046912, 1.05, 1.053088, 1.056177, 1.059265, 1.062353, 1.065441, 1.068529, 1.071618, 1.074706, 1.078824, 1.082941, 1.087059, 1.090147, 1.093235, 1.096324, 1.099412, 1.1025, 1.105588, 1.108677, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.128235, 1.132353, 1.136471, 1.139559, 1.142647, 1.145735, 1.148824, 1.151912, 1.155, 1.158088, 1.161177, 1.165294, 1.169412, 1.17353, 1.176618, 1.179706, 1.182794, 1.185882, 1.188971, 1.192059, 1.195147, 1.198235, 1.201324, 1.204412, 1.2075, 1.210588, 1.214706, 1.218824, 1.222941, 1.226029, 1.229118, 1.232206, 1.235294, 1.239412, 1.243529, 1.247647, 1.250735, 1.253824, 1.256912, 1.26, 1.263088, 1.266176, 1.269265, 1.272353, 1.276471, 1.280588, 1.284706, 1.287794, 1.290882, 1.293971, 1.297059, 1.300147, 1.303235, 1.306324, 1.309412, 1.311882, 1.314353, 1.316824, 1.319294, 1.321765, 1.327941, 1.334118, 1.336588, 1.339059, 1.341529, 1.344, 1.346471, 1.349559, 1.352647, 1.355735, 1.358824, 1.361912, 1.365, 1.368088, 1.371176, 1.374265, 1.377353, 1.380441, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882, 1.4, 1.404118, 1.408235, 1.412353, 1.416471, 1.420588, 1.423676, 1.426765, 1.429853, 1.432941, 1.436029, 1.439118, 1.442206, 1.445294, 1.449412, 1.453529, 1.457647, 1.460735, 1.463824, 1.466912, 1.47, 1.473088, 1.476177, 1.479265, 1.482353, 1.486471, 1.490588, 1.494706, 1.497794, 1.500882, 1.503971, 1.507059, 1.510147, 1.513235, 1.516324, 1.519412, 1.5225, 1.525588, 1.528677, 1.531765, 1.535882, 1.54, 1.544118, 1.547206, 1.550294, 1.553382, 1.556471, 1.559559, 1.562647, 1.565735, 1.568824, 1.572941, 1.577059, 1.581177, 1.584265, 1.587353, 1.590441, 1.593529, 1.597647, 1.601765, 1.605882, 1.608971, 1.612059, 1.615147, 1.618235, 1.621324, 1.624412, 1.6275, 1.630588, 1.634706, 1.638824, 1.642941, 1.646029, 1.649118, 1.652206, 1.655294, 1.658382, 1.661471, 1.664559, 1.667647, 1.670735, 1.673824, 1.676912, 1.68, 1.683088, 1.686177, 1.689265, 1.692353, 1.696471, 1.700588, 1.704706, 1.707794, 1.710882, 1.713971, 1.717059, 1.721177, 1.725294, 1.729412, 1.7325, 1.735588, 1.738677, 1.741765, 1.745882, 1.75, 1.754118, 1.756177, 1.758235, 1.760294, 1.762353, 1.764412, 1.766471, 1.772647, 1.778824, 1.781294, 1.783765, 1.786235, 1.788706, 1.791177, 1.794265, 1.797353, 1.800441, 1.80353, 1.807647, 1.811765, 1.815882, 1.82, 1.824118, 1.828235, 1.831324, 1.834412, 1.8375, 1.840588, 1.843677, 1.846765, 1.849853, 1.852941, 1.85603, 1.859118, 1.862206, 1.865294, 1.869412, 1.87353, 1.877647, 1.881765, 1.885882, 1.89, 1.892471, 1.894941, 1.897412, 1.899882, 1.902353, 1.90647, 1.910588, 1.914706, 1.917794, 1.920882, 1.923971, 1.927059, 1.931176, 1.935294, 1.939412, 1.9425, 1.945588, 1.948677, 1.951765, 1.954853, 1.957941, 1.96103, 1.964118, 1.968235, 1.972353, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.991912, 1.995, 1.998088, 2.001177, 2.005294, 2.009412, 2.01353, 2.016618, 2.019706, 2.022794, 2.025882, 2.03, 2.034118, 2.038235, 2.041324, 2.044412, 2.0475, 2.050588, 2.053677, 2.056765, 2.059853, 2.062941, 2.06603, 2.069118, 2.072206, 2.075294, 2.078382, 2.081471, 2.084559, 2.087647, 2.091765, 2.095882, 2.1, 2.103088, 2.106177, 2.109265, 2.112353, 2.116471, 2.120588, 2.124706, 2.127794, 2.130883, 2.133971, 2.137059, 2.140147, 2.143235, 2.146324, 2.149412, 2.1525, 2.155588, 2.158677, 2.161765, 2.164853, 2.167941, 2.17103, 2.174118, 2.178235, 2.182353, 2.186471, 2.188941, 2.191412, 2.193882, 2.196353, 2.198824, 2.201912, 2.205, 2.208088, 2.211177, 2.214265, 2.217353, 2.220441, 2.22353, 2.227647, 2.231765, 2.235883, 2.238971, 2.242059, 2.245147, 2.248235, 2.251324, 2.254412, 2.2575, 2.260588, 2.264706, 2.268824, 2.272941, 2.27603, 2.279118, 2.282206, 2.285294, 2.287765, 2.290235, 2.292706, 2.295177, 2.297647, 2.301765, 2.305882, 2.31, 2.313088, 2.316177, 2.319265, 2.322353, 2.325441, 2.32853, 2.331618, 2.334706, 2.338824, 2.342941, 2.347059, 2.350147, 2.353235, 2.356324, 2.359412, 2.3625, 2.365588, 2.368677, 2.371765, 2.374853, 2.377941, 2.381029, 2.384118, 2.387206, 2.390294, 2.393382, 2.396471, 2.399559, 2.402647, 2.405735, 2.408823, 2.412941, 2.417059, 2.421176, 2.424265, 2.427353, 2.430441, 2.433529, 2.436, 2.438471, 2.440941, 2.443412, 2.445882, 2.448971, 2.452059, 2.455147, 2.458235, 2.462353, 2.466471, 2.470588, 2.473059, 2.475529, 2.478, 2.480471, 2.482941, 2.487059, 2.491177, 2.495294, 2.497765, 2.500235, 2.502706, 2.505177, 2.507647, 2.510735, 2.513824, 2.516912, 2.52, 2.523088, 2.526176, 2.529265, 2.532353, 2.534824, 2.537294, 2.539765, 2.542235, 2.544706, 2.548824, 2.552941, 2.557059, 2.55953, 2.562, 2.564471, 2.566941, 2.569412, 2.5725, 2.575588, 2.578676, 2.581765, 2.583824, 2.585882, 2.587941, 2.59, 2.592059, 2.594118, 2.597206, 2.600294, 2.603382, 2.606471, 2.609559, 2.612647, 2.615735, 2.618824, 2.620883, 2.622941, 2.625, 2.627059, 2.629118, 2.631176, 2.634265, 2.637353, 2.640441, 2.643529, 2.646, 2.648471, 2.650941, 2.653412, 2.655882, 2.658353, 2.660824, 2.663294, 2.665765, 2.668235, 2.670706, 2.673177, 2.675647, 2.678118, 2.680588, 2.683059, 2.685529, 2.688, 2.690471, 2.692941, 2.696029, 2.699118, 2.702206, 2.705294, 2.707765, 2.710235, 2.712706, 2.715177, 2.717647, 2.720118, 2.722588, 2.725059, 2.72753, 2.73, 2.732471, 2.734941, 2.737412, 2.739882, 2.742353, 2.744412, 2.746471, 2.748529, 2.750588, 2.752647, 2.754706, 2.757176, 2.759647, 2.762118, 2.764588, 2.767059, 2.769118, 2.771177, 2.773235, 2.775294, 2.777353, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.794235, 2.796706, 2.799177, 2.801647, 2.804118, 2.806588, 2.809059, 2.81153, 2.814, 2.816471, 2.81853, 2.820588, 2.822647, 2.824706, 2.826765, 2.828824, 2.830883, 2.832941, 2.835, 2.837059, 2.839118, 2.841177, 2.843235, 2.845294, 2.847353, 2.849412, 2.851471, 2.853529, 2.856, 2.858471, 2.860941, 2.863412, 2.865882, 2.867647, 2.869412, 2.871177, 2.872941, 2.874706, 2.876471, 2.878235, 2.88, 2.881765, 2.883529, 2.885294, 2.887059, 2.888824, 2.890588, 2.892353, 2.894118, 2.895882, 2.897647, 2.899412, 2.901177, 2.902941, 2.905412, 2.907882, 2.910353, 2.912824, 2.915294, 2.917353, 2.919412, 2.921471, 2.92353, 2.925588, 2.927647, 2.929412, 2.931177, 2.932941, 2.934706, 2.936471, 2.938235, 2.94, 2.942471, 2.944941, 2.947412, 2.949883, 2.952353, 2.954118, 2.955883, 2.957647, 2.959412, 2.961176, 2.962941, 2.964706, 2.966471, 2.968235, 2.97, 2.971765, 2.973529, 2.975294, 2.977059, 2.979118, 2.981177, 2.983235, 2.985294, 2.987353, 2.989412, 2.990956, 2.9925, 2.994044, 2.995588, 2.997132, 2.998676, 3.000221, 3.001765, 3.003824, 3.005883, 3.007941, 3.01, 3.012059, 3.014118, 3.015882, 3.017647, 3.019412, 3.021177, 3.022941, 3.024706, 3.026471, 3.028235, 3.03, 3.031765, 3.03353, 3.035294, 3.037059, 3.038824, 3.040883, 3.042941, 3.045, 3.047059, 3.049118, 3.051177, 3.052721, 3.054265, 3.055809, 3.057353, 3.058897, 3.060441, 3.061985, 3.063529, 3.065588, 3.067647, 3.069706, 3.071765, 3.073823, 3.075882, 3.077255, 3.078628, 3.08, 3.081373, 3.082745, 3.084118, 3.08549, 3.086863, 3.088235, 3.090294, 3.092353, 3.094412, 3.096471, 3.098529, 3.100588, 3.102353, 3.104118, 3.105882, 3.107647, 3.109412, 3.111177, 3.112941, 3.115412, 3.117882, 3.120353, 3.122824, 3.137647]


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
    tempSensor = ts.TemperatureSensor(lookup,tempPin)
    relay = rl.Relay(relayPin)
    algaeSensor = ps.PhotoSensor(algaeConstant, algaeZero, lookup, odPin)
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