#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 12:05:08 2021

@author: BWSI AUV Challenge Instructional Staff
"""
import sys
import numpy as np
import math

from MissionReconstruction import Mission_Reconstruction

class AUVController():
    def __init__(self):
        
        # initialize state information
        self.__heading = None
        # self.__speed = None
        # self.__rudder = None
        # self.__position = None
        
        # assume we want to be going the direction we're going for now
        self.__desired_heading = None
        
    def initialize(self, auv_state):
        self.__heading = auv_state['heading']
        # self.__speed = auv_state['speed']
        # self.__rudder = auv_state['rudder']
        # self.__position = auv_state['position']
        
        # assume we want to be going the direction we're going for now
        self.__desired_heading = auv_state['heading']

    ### Public member functions
    # also add something to change speeds and whatnot
    def decide(self, auv_state, green_buoys, red_buoys, sensor_type='POSITION'):
        if auv_state['heading'] is None:
            return None, []

        # update state information
        self.__heading = auv_state['heading']
        print("the heading is ", self.__heading)
        # self.__speed = auv_state['speed']
        # self.__rudder = auv_state['rudder']
        # self.__position = auv_state['position']
                
        # determine what heading we want to go
        if sensor_type.upper() == 'POSITION': # known positions of buoys
            self.__desired_heading = self.__heading_to_position(green_buoys, red_buoys)
        elif sensor_type.upper() == 'ANGLE': # camera sensor
            self.__desired_heading = self.__heading_to_angle(green_buoys, red_buoys)
        
        # determine whether and what command to issue to desired heading               
        cmd = self.__select_command()

        #want to call the messages command from mission reconstruction here
        #because its currently not getting the data
        reconstruction = Mission_Reconstruction()
        reconstruction.store_autonomy_decide([self.__desired_heading])
        reconstruction.auv_command(cmd)
        
        #
        # ADDED STATUS HERE; INFORMATION FROM STUFF
        #

        return cmd, []
        
    # return the desired heading to a public requestor
    def get_desired_heading(self):
        return self.__desired_heading
    

    ### Private member functions
        
    # calculate the heading we want to go to reach the gate center
    def __heading_to_position(self, gnext, rnext):
        # center of the next buoy pair
        gate_center = ((gnext[0]+rnext[0])/2.0, (gnext[1]+rnext[1])/2.0)
        
        # heading to gate_center
        tgt_hdg = np.mod(np.degrees(np.arctan2(gate_center[0]-self.__position[0],
                                               gate_center[1]-self.__position[1]))+360,360)
        
        return tgt_hdg
    
    def __heading_to_angle(self, gnext, rnext):
        # relative angle to the center of the next buoy pair
        if len(gnext) == 0 and len(rnext) == 0:
            return self.__heading
        elif len(gnext) == 0:
            return max(rnext, key=abs) + self.__heading + (15 * max(rnext)/abs(max(rnext)))
        elif len(rnext) == 0:
            return max(gnext, key=abs) + self.__heading + (15 * max(gnext)/abs(max(gnext)))

        #
        # TODO PAIR UP THE BUOYS???
        # DON'T KNOW HOW THIS WILL BE DONE THOUGH
        # SINCE WE DON'T KNOW THEIR DISTANCES, ONLY ANGLES
        # DEFINITELY RED ANGLE > GREEN ANGLE
        #

        #
        # because of method of image processing, it might not be necessary to have to deal
        # with the "multiple buoy" test case
        #

        relative_angle = 0
        angle_difference = 0
        for i in range(0, min(len(gnext), len(rnext))):
            if angle_difference < abs(gnext[i] - rnext[i]):
                relative_angle = (gnext[i] + rnext[i]) / 2.0
                angle_difference = abs(gnext[i] - rnext[i])

        # heading to center of the next buoy pair        
        tgt_hdg = self.__heading + relative_angle
        
        return tgt_hdg

    # choose a command to send to the front seat
    def __select_command(self):
        # Unless we need to issue a command, we will return None
        cmd = None
        
        # determine the angle between current and desired heading
        delta_angle = max(self.__desired_heading, self.__heading) - min(self.__desired_heading, self.__heading)

        # if delta_angle > 15:
        #     delta_angle *= 1.5

        if delta_angle < 15 and delta_angle > 5:
            delta_angle -= 5

        if delta_angle > 25:
            delta_angle = 25
        if delta_angle < 0:
            delta_angle = 0
        
        # how much do we want to turn the rudder
        ## Note: using STANDARD RUDDER only for now! A calculation here
        ## will improve performance!
        turn_command = str(round(delta_angle)) + " DEGREES RUDDER"

        '''thresh = 10
        if(np.abs(delta_angle) < thresh ):
            turn_command = f"{str(math.ceil(delta_angle))} DEGREES RUDDER"
        elif(np.abs(delta_angle) == thresh):
            turn_command = "20 DEGREES RUDDER"
        else:
            if self.__heading > self.__desired_heading:
                cmd = f"LEFT 25 DEGREES RUDDER"
            elif self.__heading < self.__desired_heading:
                cmd = f"RIGHT 25 DEGREES RUDDER"
            return cmd'''
        
        if delta_angle > 0:
            if self.__heading > self.__desired_heading:
                cmd = f"LEFT {turn_command}"
            elif self.__heading < self.__desired_heading:
                cmd = f"RIGHT {turn_command}"
        else:
            cmd = "RUDDER AMIDSHIPS"
        
        return cmd
        