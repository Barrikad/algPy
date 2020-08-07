import network

internetName = "Mathilde - iPhone"
internetCode = "12345678"

# connect the device to the WiFi network 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(internetName,internetCode)


#If you wish to turn off the WiFi Access Point

#ap_if = network.WLAN(network-AP_IF)
#ap_if.active(False)



#Here is the test for wether you are connected to the wifi
#If you are connected, the first 1000 characters received 
#from the www.dtu.dk web-page are printed

import socket

request = b"GET / HTTP/1.1\nHost: www.dtu.dk\n\n" 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.dtu.dk", 80))
s.settimeout(2) 
s.send(request) 
result = s.recv(10000) 
print(result) 
s.close()


import network
import time
from umqtt.robust import MQTTClient
import os
import sys


wifiName = '"Mathilde - iPhone"'
wifiPassword = '"12345678"'
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'munz234'
ADAFRUIT_IO_KEY = b'aio_GzWu16y16PYJ8plYBlniKEOamHlg'
ADAFRUIT_IO_FEEDNAME = "tbd"

class web :
    
    
    def connectToWifi():
        # WiFi connection information
        WIFI_SSID = wifiName
        WIFI_PASSWORD = wifiPassword
        
        # turn off the WiFi Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        
        # connect the device to the WiFi network
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # wait until the device is connected to the WiFi network
        MAX_ATTEMPTS = 20
        attempt_count = 0
        while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            time.sleep(1)

        if attempt_count == MAX_ATTEMPTS:
            print('could not connect to the WiFi network')
            sys.exit()
    
    def connectToFeed(feedname):
        # create a random MQTT clientID 
        random_num = int.from_bytes(os.urandom(3), 'little')
        mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

        # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
        # 
        # To use a secure connection (encrypted) with TLS: 
        #   set MQTTClient initializer parameter to "ssl=True"
        #   Caveat: a secure connection uses about 9k bytes of the heap
        #         (about 1/4 of the micropython heap on the ESP8266 platform)
        
        client = MQTTClient(client_id=mqtt_client_id, 
                            server=ADAFRUIT_IO_URL, 
                            user=ADAFRUIT_USERNAME, 
                            password=ADAFRUIT_IO_KEY,
                            ssl=False)
            
        try:      
            client.connect()
            print("Connected!")
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
            sys.exit()
        
    def cb(topic, msg):
        print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
        free_heap = int(str(msg,'utf-8'))
        print('free heap size = {} bytes'.format(free_heap))
        
    def subscribe(feedname):
        
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')    
        client.set_callback(cb)                    
        client.subscribe(mqtt_feedname)  
        
        # following two lines is an Adafruit-specific implementation of the Publish "retain" feature 
        # which allows a Subscription to immediately receive the last Published value for a feed,
        # even if that value was Published two hours ago.
        # Described in the Adafruit IO blog, April 22, 2018:  https://io.adafruit.com/blog/  
        mqtt_feedname_get = bytes('{:s}/get'.format(mqtt_feedname), 'utf-8')    
        client.publish(mqtt_feedname_get, '\0')  
        
        # wait until data has been Published to the Adafruit IO feed
        while True:
            try:
                client.wait_msg()
                print("Client subscribed!")
            except KeyboardInterrupt:
                print('Ctrl-C pressed...exiting')
                client.disconnect()
                sys.exit()
        
    def publish(feedname, stringToPublish):
        PUBLISH_PERIOD_IN_SEC = 10 
        while True:
            try:
                client.publish(mqtt_feedname,    
                           bytes(stringToPublish, 'utf-8'), 
                           qos=0)  
                print("Client published!")
                time.sleep(PUBLISH_PERIOD_IN_SEC)
            except KeyboardInterrupt:
                print('Ctrl-C pressed...exiting')
                client.disconnect()
                sys.exit()
    
    
    def subscribeCurrentTemp():
        ADAFRUIT_IO_FEEDNAME = b'Current Temperature'
        return subscribe(ADAFRUIT_IO_FEEDNAME)
    
    def publishCurrentTemp():
        return publish(b'Current Temperature',"67")
    
 
        
    
