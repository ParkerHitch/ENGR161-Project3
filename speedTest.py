from src.subsystems.Drivetrain import RearWheelDriveFrontWheelSteer
import time
import math
import config
import brickpi3
import src.subsystems.LineFollow as LineFollow
from src.subsystems.sensors.g_LineFinder import GroveLineFinder
from src.subsystems.Dump import Dump
from src.subsystems.sensors.IMU import IMU
from src.subsystems.sensors.g_Ultrasonic import GroveUltrasonic
import matplotlib.pyplot as plt

BP = brickpi3.BrickPi3()

drivetrain = RearWheelDriveFrontWheelSteer(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR, config.FRONT_MOTOR, 0)
dump = Dump(BP, config.DUMP_MOTOR)
lightLeft = GroveLineFinder(config.G_LINE_LEFT)
lightRight = GroveLineFinder(config.G_LINE_RIGHT)
distSense = GroveUltrasonic(config.G_ULTRASONIC)
imu = IMU()
imu.initialize()
LineFollow.initLineFollow()

deltaT = 0
lastT = time.time()

desiredCmpS = int(input("Enter desired cm/s: "))
desiredRadPS = desiredCmpS / (config.WHEEL_RADIUS_CM)
desiredDPS = math.degrees(desiredRadPS)
mult = desiredDPS / config.BASE_SPEED_DPS

go = True

lastDist = distSense.getRawVal()

lastL = drivetrain.getLEncoder()
lastR = drivetrain.getREncoder()

times = []
imuVels = []
distVels = []
encVels = []


startT = time.time()
while go:
    try:
        LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight, mult)
        deltaT = time.time() - lastT
        lastT += deltaT
        times.append(lastT - startT)
        
        imu.update()
        imuVels.append(imu.velocity.z)

        deltaDist = distSense.getRawVal() - lastDist
        lastDist += deltaDist
        distVels.append(deltaDist / deltaT)

        deltaL = drivetrain.getLEncoder() - lastL
        deltaR = drivetrain.getREncoder() - lastR
        lastL += deltaL
        lastR += deltaR
        encVels.append(math.radians((deltaL+deltaR)/(2*deltaT)) * config.WHEEL_RADIUS_CM)
        time.sleep(0.1)

    except KeyboardInterrupt:
        go = False

BP.reset_all()

filt = list(filter(lambda x: x!= 0,distVels[10:]))
print("DIST AVG: ", sum(filt)/len(filt))

plt.title("CMPs " + str(desiredCmpS))

plt.plot(times, imuVels, label="imuVels")
plt.plot(times, distVels, label="distVels")
plt.plot(times, encVels, label="encVels")
plt.legend()
plt.show()

    
