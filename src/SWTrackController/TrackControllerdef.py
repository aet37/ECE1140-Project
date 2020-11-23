

class TrackController:

    def __init__(self, controller_id, mystery_argument):
       # self.PLC_Program = 

        self.id = controller_id
        self.suggestedspeed=0
        self.blocklist = []
        self.occupancy = []
        self.prevoccupancy = []
        self.position = 0
        self.positionQueue=[]

    def getSwitchPos(self):
        return self.position

    def changeSwitchPos(self):
        if self.position==0:
            self.position==1
        elif self.position==1:
            self.position = 0

    def occupancyToString(self):
        for i in self.occupancy:
            outputString= outputString +str(self.occupancy[i])
        return outputString

    def setupOccupancy(self, blocks):
        for i in range(0,blocks):
            self.occupancy.append(0)

    def setOccupied(self,blockIndex):
        self.occupancy[blockIndex] = 1
    
    def setUnoccupied(self,blockIndex):
        self.occupancy[blockIndex]=0

    def getSuggestedSpeed(self):
        return self.suggestedspeed
    
    def setSuggestedSpeed(self,speed):
        self.suggestedspeed = speed
    
    def addToQueue(self,next):
        self.positionQueue.append(next)

    def popNext(self):
        self.positionQueue.pop


if __name__ == "__main__": 
    raise Exception("Not to be run as a module")



    


    

    

    


       
