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
class web 
    def get_value(key):
        
    def send_value(key,value)
