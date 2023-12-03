from lib.MPU9250 import MPU9250
from lib.Vector3 import Vector3
import numpy as np
import time
import math
import config

class IMU:
    def __init__(self):
        self.mpu9250 = MPU9250()
        self.accel = Vector3(0,0,0)
        self.gyro = Vector3(0,0,0)
        self.orientation = Vector3(0,0,0)
        self.mag = Vector3(0,0,0)
        self.biases = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.state = [[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],[0,0,0,0,0,0,0,0,0]]
        self.lastUpdated = time.time_ns()


    # sets self.biases and self.std
    def initialize(self):
        print("Initializing IMU...")
        print("    Calibrating IMU...")
        depth = 25
        self.biases=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        for x in range(depth):
            accel = self.mpu9250.readAccel()
            gyro = self.mpu9250.readGyro()
            mag = self.mpu9250.readMagnet()
            self.biases[0] += accel.x/depth
            self.biases[1] += accel.y/depth
            self.biases[2] += accel.z/depth
            self.biases[3] += gyro.x/depth
            self.biases[4] += gyro.y/depth
            self.biases[5] += gyro.z/depth
            self.biases[6] += mag.x/depth
            self.biases[7] += mag.y/depth
            self.biases[8] += mag.z/depth
            time.sleep(0.02)
        print("    Calibration Complete")
        print("\n    Initializing Filters...")
        #Setting up initial variables
        depth=99
        data=[[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        self.std=[0,0,0,0,0,0,0,0,0]
        #Gathering data to analyze
        for x in range(depth):
            accel = self.mpu9250.readAccel()
            gyro = self.mpu9250.readGyro()
            mag = self.mpu9250.readMagnet()
            data[0].append(accel.x -self.biases[0])
            data[1].append(accel.y -self.biases[1])
            data[2].append(accel.z -self.biases[2])
            data[3].append(gyro.x - self.biases[3])
            data[4].append(gyro.y - self.biases[4])
            data[5].append(gyro.z - self.biases[5])
            data[6].append(mag.x - self.biases[6])
            data[7].append(mag.y - self.biases[7])
            data[8].append(mag.z - self.biases[8])
        #Breaking out data
        accelx=np.array(data[0],dtype=np.float)
        accely=np.array(data[1],dtype=np.float)
        accelz=np.array(data[2],dtype=np.float)
        gyrox=np.array(data[3],dtype=np.float)
        gyroy=np.array(data[4],dtype=np.float)
        gyroz=np.array(data[5],dtype=np.float)
        magx=np.array(data[6],dtype=np.float)
        magy=np.array(data[7],dtype=np.float)
        magz=np.array(data[8],dtype=np.float)
        #Setting up for output
        self.std[0]=np.std(accelx)
        self.std[1]=np.std(accely)
        self.std[2]=np.std(accelz)
        self.std[3]=np.std(gyrox)
        self.std[4]=np.std(gyroy)
        self.std[5]=np.std(gyroz)
        self.std[6]=np.std(magx)
        self.std[7]=np.std(magy)
        self.std[8]=np.std(magz)
        print("    Filters Initialized")
        print("IMU Initialized")
        self.lastUpdated = time.time_ns()


    def InvGaussFilter(self, value, bias, std):
        if value < config.STDEV_COUNT*std-bias and value > -config.STDEV_COUNT*std-bias:
            value = bias
        return value

    def update(self):
        accel = self.mpu9250.readAccel()
        gyro = self.mpu9250.readGyro()
        self.rawMag = self.mpu9250.readMagnet()
        mag = Vector3(self.rawMag.x, self.rawMag.y, self.rawMag.z)
        temp=[accel.x,accel.y,accel.z,gyro.x,gyro.y,gyro.z,mag.x,mag.y,mag.z]
        for x in range(9):
            #Setting up initial variables
            r=config.FILTER[x][0]
            q=config.FILTER[x][1]
            #Setting up state
            ex=self.state[1][x]
            p=self.state[0][x]+q
            #Applying filter criteria
            k=p/(p+r)
            ex=ex+k*(temp[x]-ex)
            p=(1-k)*p
            #Put values into state
            self.state[1][x]=ex
            self.state[0][x]=p

        self.accel.x =self.InvGaussFilter(self.state[1][0], self.biases[0],self.std[0]) - self.biases[0]
        self.accel.y =self.InvGaussFilter(self.state[1][1], self.biases[1],self.std[1]) - self.biases[1]
        self.accel.z =self.InvGaussFilter(self.state[1][2], self.biases[2],self.std[2]) - self.biases[2]
        self.gyro.x =self.InvGaussFilter(self.state[1][3], self.biases[3],self.std[3]) - self.biases[3]
        self.gyro.y =self.InvGaussFilter(self.state[1][4], self.biases[4],self.std[4]) - self.biases[4]
        self.gyro.z =self.InvGaussFilter(self.state[1][5], self.biases[5],self.std[5]) - self.biases[5]
        self.mag.x =self.InvGaussFilter(self.state[1][6], self.biases[6],self.std[6]) - self.biases[6]
        self.mag.y =self.InvGaussFilter(self.state[1][7], self.biases[7],self.std[7]) - self.biases[7]
        self.mag.z =self.InvGaussFilter(self.state[1][8], self.biases[8],self.std[8]) - self.biases[8]

        now = time.time_ns()
        deltaT = (now - self.lastUpdated) / 1e9
        self.lastUpdated = now

        self.orientation.x += self.gyro.x * deltaT
        self.orientation.y += self.gyro.y * deltaT
        self.orientation.z += self.gyro.z * deltaT


    def hasMagnet(self):
        mag = self.rawMag
        #print(mag.mag())
        return (mag.mag() > config.MAG_THRESH and mag.x/mag.mag() > config.MAG_ANG)
    
    # + is CCW
    def getYaw(self):
        return math.radians(self.orientation.y)
    # + is nose up
    def getPitch(self):
        return math.radians(self.orientation.x)
    # + is CCW from behind
    def getRoll(self):
        return math.radians(self.orientation.z)
    
    def zeroOrientation(self):
        self.orientation = Vector3()
