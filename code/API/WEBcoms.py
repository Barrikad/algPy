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
