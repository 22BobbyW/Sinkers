import time 
from datetime import datetime

from numpy.lib.utils import info 
import BWSI_Sandshark
import csv 

# pictures what the AUV sees vs actual camera
# AUV's location
# commands being sent
# plotting AUV path
# buoys passed/what buoy we are at
# time count

class Mission_Reconstruction():
        
    def __init__(self):
        self.missionstart = datetime.now()
        self.vehicle = BWSI_Sandshark.Sandshark()
        self.__index = 0
        self.__time = None
        self.__data = []


            
    # this function is called before store_autonomy_decide 
    # so that they use the same index 
    def messages(self, status):
        m = status.split(",")
        timeStamp = m[1] # change to store time - first time; time elapsed
        heading = m[9]

        self.__data.append(timeStamp)
        self.__data.append(heading)

      
    def auv_command(self, cmd):
        self.__data.append(cmd)
        
    def store_autonomy_decide(self, information):
        
        if len(information) == 0:
            self.__data.append("no data")
            self.add_to_csv()
           
        else:
            desired_heading = information[0]
            
            self.__data.append(desired_heading)
            self.add_to_csv()
           
            
    def save_pos(self, pos):
         auv_posX = []
         auv_posY = []
         auv_posX.append(pos[0])
         auv_posY.append(pos[1])
         
         with open('position.csv', 'a') as csvfile:
            auvData = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            auvData.writerow(['X', 'Y'])
            
            auvData.writerow([auv_posX, auv_posY])

        
    def add_to_csv(self):
        with open('auvData.csv', 'a') as csvfile:
            auvData = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #auvData.writerow(['Time', 'Heading', 'Desired Heading'])
            
            auvData.writerow(self.__data)
        self.__data = []

        
    

 