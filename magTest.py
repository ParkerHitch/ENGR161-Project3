import src.subsystems.sensors.IMU as IMU
import time
from lib.Vector3 import Vector3

imu = IMU.IMU()

imu.initialize()

while True:
#    if(imu.hasMagnet()):
#        print("MAGNET")
    mag = imu.mpu9250.readMagnet()
    print(mag.mag())
    if (mag.mag() == 0):
        print(0)
    else:
        print(mag.x / mag.mag())
    time.sleep(0.2)
