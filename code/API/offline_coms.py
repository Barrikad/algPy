

class Offline :
    
    def __init__(self, file_path):
        self.path = file_path
    
    def connectToWifi(self):
        pass
    
    def connectToMQTT(self):
        pass
    
    def cb(self,topic, msg):
        tp = str(topic,'utf-8')
        tp = (tp.split('/'))[-1]
        ms = float(str(msg,'utf-8'))
        self.values[tp] = ms
        
    def _subscribe(self,feedname):
        pass
        
        
    def publish(self, feedname, stringToPublish): 
        fileWithData = open(self.path,'a')
        try:
            fileWithData.write("....")
            fileWithData.write(feedname)
            fileWithData.write("\n")
            fileWithData.write(stringToPublish)
        finally:
            fileWithData.close()
    
    def subscribe_to_keys(self,listOfKeys):
        pass
    
    def get_latest_value(self,key):
        pass

    def update_values(self):
        pass
  