#!/usr/bin/env /home/bet/.virtualenvs/cv/bin/python
import enum
import os
import sys
import rclpy
from rclpy.node import Node
from math import *
import numpy as np
import serial
import time
from mbse.srv import Mani , Navi , Detect
class State(enum.Enum):
    softwarecheck = 0
    waitfeedbacksoftware = 1
    hardwarecheck = 5
    waitfeedbackhardware = 6
    idle = 10
    sendtomani = 20
    waitfeedbackmani = 21
    resultmani = 22
    sendtonavi = 30
    waitfeedbacknavi = 31
    resultnavi = 32
    sendtodetect = 40
    waitfeedbackdetect = 41
    resultdetect = 42
    collisiondetect = 99
    Emergencybutton = 100

class Response(enum.Enum):
    success = 1
    failure = 0
    inprogress = 2

class Order(enum.Enum):
    waitforcommand = 0
    doingtask1 = 1
    doingtask2 = 2
class Core(Node):
    def __init__(self):
        super().__init__('Core')
        self.Navi = self.create_service(Navi, '/mbse/Navi', self.Navi_callback)
        self.Mani = self.create_service(Mani, '/mbse/Mani', self.Mani_callback)
        self.Detect = self.create_service(Detect, '/mbse/Detect', self.Detect_callback)
        self.state = State.softwarecheck
        self.order = 0
        self.goalpose
        self.currentpose
        self.findingstate = 0
        self.findingarea = [[],[],[]] # add object finding area ex: [Umbrella,10,10]
        self.detectionresponse
        self.naviresponse
        self.task = Response.inprogress
        self.graspstate = 0
        self.grasprange = 0
        self.objectpose = []
        self.graspresponse
    def Initialize(self):
        # run softwarecheck
        self.state = State.waitfeedbacksoftware
        while self.state != State.hardwarecheck:
            # get feedback
            self.state = State.hardwarecheck
        # run hardwarecheck
        self.state = State.waitfeedbackhardware
        while self.state != State.idle:
            # get feedback
            self.state = State.idle

    def Idle(self):
        self.Detectingcommand()

    def Detectingcommand(self):
        if self.order == Order.waitforcommand:
            pass
            #call service to Detection node to detect Input/Output state
    def Movetotarget(self,goalpose):
        # call service to NAV2 node
        self.currentpose = []
        # self.naviresponse = Response.success or failure

    def Findingobject(self,findingstate,objectclass):
        # call service to Detection node =
        # self.detectionresponse = Response.success or failure
        pass

    def Ingraspingrange(self,objectpose,currentpose):
        #call service to Detection to check if object pose and current pose can grasp
        return Response.success # return can or cant
    def Findingobjectandmoving(self,objectclass):
        if self.findingstate == 0:
            self.Movetotarget(self.findingarea[objectclass][1:])             #call service to NAV2 = go to find area
            if self.currentpose[0:1] == self.findingarea[objectclass][1:]:
                self.findingstate = 1
        if self.findingstate == 1:
            #call service to NAV2 node = spin
            self.Findingobject(self.findingstate,objectclass)                   #call service to Detection node = detect objectclass
            if self.detectionresponse == Response.success:
                self.findingstate = 0
                self.task = Response.success
            # if spin completely
                self.task = Response.failure

    def Pickingupobject(self,objectclass):
        if self.graspstate == 0:
            self.Findingobject(1,objectclass)                    #call service to Detection node = to return object pose
            self.grasprange = self.Ingraspingrange(self.objectpose,self.currentpose)
            if self.grasprange == Response.failure:
                self.Movetotarget(self.objectpose)
            else:
                #call service to stop moving
                #call service to grasp object return with response
                pass
            if self.graspresponse == Response.success:
                self.graspstate = 1

if __name__ == '__main__':
    while 1:
        print("1")
