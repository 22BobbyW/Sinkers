import cv2 
import numpy as np
import matplotlib.pyplot as plt
import picamera 
import time 
from datetime import datetime 
import BWSI_Sandshark
import pandas as pd
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


    def messages(self, cmd):
        
        commands = pd.DataFrame(columns=['time', 'message', 'position'])
        time = datetime.now()




