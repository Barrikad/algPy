

class Offline :
    
    def __init__(self, file_path):
        self.path = file_path
        print("Initializing the offline version..")
    
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
        print("starting to publish to file..")
        try:
            fileWithData.write("....")
            fileWithData.write(feedname)
            fileWithData.write("\n")
            fileWithData.write(stringToPublish)
            print("writing..")
        finally:
            fileWithData.close()
            print("closed the file..")
    
    def subscribe_to_keys(self,listOfKeys):
        pass
    
    def get_latest_value(self,key):
        return -9999

    def update_values(self):
        pass
  