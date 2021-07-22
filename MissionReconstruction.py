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
        self.__index = 0
        self.__time = None
        self.__commands = [][4] # time, heading, desired heading, speed

    # this function is called before store_autonomy_decide 
    # so that they use the same index 
    def messages(self, status):
        m = status.split(",")
        time = m[1] # change to store time - first time; time elapsed
        heading = m[9]

        self.__commands[self.__index][0] = time
        self.__commands[self.__index][1] = heading 
        return

    def store_autonomy_decide(self, information):
        desired_heading = information[0]
        speed = information[1]

        self.__commands[self.__index][2] = desired_heading
        self.__commands[self.__index][3] = speed

        self.__index += 1
        return
