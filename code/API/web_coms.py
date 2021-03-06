import network
import time
from umqtt.robust import MQTTClient
import code.API.offline_coms as Offline
import os

###############################QMTT_test#########################
def web_test(wifiName,wifiPassword,ADAFRUIT_IO_URL,ADAFRUIT_USERNAME,ADAFRUIT_IO_KEY,subscribeKeys):
    web = Web(wifiName,wifiPassword,ADAFRUIT_IO_URL,ADAFRUIT_USERNAME,ADAFRUIT_IO_KEY)
    web.connectToWifi()
    web.connectToMQTT()
    web.subscribe_to_keys(subscribeKeys)
    for i in range(1000):
        web.publish('Current Temperature', str(i))
        web.update_values()
        for s in subscribeKeys:
            print("{} : {}".format(s,web.get_latest_value(s)))
        time.sleep(5)
#################################################################

class Web :
    
    def __init__(self,wifiName,wifiPassword,ADAFRUIT_IO_URL,ADAFRUIT_USERNAME,ADAFRUIT_IO_KEY):
        self.wifiName = wifiName
        self.wifiPassword = wifiPassword
        self.ADAFRUIT_IO_URL = ADAFRUIT_IO_URL
        self.ADAFRUIT_USERNAME = ADAFRUIT_USERNAME
        self.ADAFRUIT_IO_KEY = ADAFRUIT_IO_KEY
        self.Connected = "F"
        # create a random MQTT clientID 
        random_num = int.from_bytes(os.urandom(3), 'little')
        self.mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
        
        # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
        # 
        # To use a secure connection (encrypted) with TLS: 
        #   set MQTTClient initializer parameter to "ssl=True"
        #   Caveat: a secure connection uses about 9k bytes of the heap
        #         (about 1/4 of the micropython heap on the ESP8266 platform)
        self.client = MQTTClient(client_id=self.mqtt_client_id, 
                                 server=ADAFRUIT_IO_URL, 
                                 user=ADAFRUIT_USERNAME, 
                                 password=ADAFRUIT_IO_KEY,
                                 ssl=False)
        
        self.values = {}
    
    def getConnected(self):
        return self.Connected
    
    def connectToWifi(self):
        # WiFi connection information
        WIFI_SSID = self.wifiName
        WIFI_PASSWORD = self.wifiPassword
        
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
            self.Connected = "F"
            wifi.active(False)
            return Offline.Offline("Offline_Data.txt")
        
        self.Connected = "T"
        return self
    
    
    def connectToMQTT(self):
        try:      
            self.client.connect()
            return 0
        except Exception:
            return -1
    
    def cb(self,topic, msg):
        tp = str(topic,'utf-8')
        tp = (tp.split('/'))[-1]
        ms = float(str(msg,'utf-8'))
        self.values[tp] = ms
        
    def _subscribe(self,feedname):
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.ADAFRUIT_USERNAME, feedname), 'utf-8')    
        self.client.set_callback(self.cb)                    
        self.client.subscribe(mqtt_feedname)  
        
        mqtt_feedname_get = bytes('{:s}/feeds/{:s}/get'.format(self.ADAFRUIT_USERNAME,feedname), 'utf-8')    
        self.client.publish(mqtt_feedname_get, '\0')  
        
        self.client.wait_msg()
        
        
    def publish(self, feedname, stringToPublish): 
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.ADAFRUIT_USERNAME, feedname), 'utf-8')   
        
        self.client.publish(mqtt_feedname,    
                            bytes(stringToPublish, 'utf-8'), 
                            qos=0)
    
    def subscribe_to_keys(self,listOfKeys):
        for s in listOfKeys:
            bs = str(s,'utf-8')
            self.values[s] = -9999
            self._subscribe(bs)
    
    def get_latest_value(self,key):
        return self.values[key]

    def update_values(self):
        self.client.check_msg()
  