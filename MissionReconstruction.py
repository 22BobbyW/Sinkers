import cv2 
import numpy as np
import matplotlib.pyplot as plt
import time 
from datetime import datetime 
import BWSI_Sandshark
import pandas as pd
import BWSI_BackSeat
import csv 

# pictures what the AUV sees vs actual camera
# AUV's location
# commands being sent
# plotting AUV path
# buoys passed/what buoy we are at
# time count

class MissionReconstruction():
    def __init__(self):
        self.missionstart = datetime.now()
        self.vehicle = BWSI_Sandshark.Sandshark()
    
    def messages(self, status):
        commands = [][2]
        n = 0
        while(True):
            m = status.split(",")
            time = m[1]
            commands[n][0] = time
            heading = m[9]
            commands[n][1] = heading 
            n += 1 

            
