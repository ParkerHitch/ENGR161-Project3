import math
from lib.MPU9250 import MPU9250
from src.subsystems.Drivetrain import RearWheelDriveFrontWheelSteer
from src.subsystems.sensors.g_Light import GroveLightSensor
import src.subsystems.LineFollow as LineFollow
import config
import brickpi3
import time

from src.subsystems.sensors.g_LineFinder import GroveLineFinder
from src.subsystems.Dump import Dump

class IMU:
    def __init__(self):
        self.mpu9250 = MPU9250()
    
    def hasMagnet(self):
        mag = self.mpu9250.readMagnet()
        return 250 < math.sqrt(math.pow(mag['x'],2) + math.pow(mag['y'],2) + math.pow(mag['z'],2))

print("Hello Project 3!")

BP = brickpi3.BrickPi3()

# 0 = disabled
# 1 = following a basic line
state = 0

# declaring our subsystem variables
drivetrain: RearWheelDriveFrontWheelSteer
lightLeft: GroveLineFinder
lightRight: GroveLineFinder
dump: Dump
imu:IMU

# stuff to do upon starting python
def robotInit():
    global drivetrain, lightLeft, lightRight, dump, imu, BP
    drivetrain = RearWheelDriveFrontWheelSteer(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR, config.FRONT_MOTOR, 0)
    dump = Dump(BP, config.DUMP_MOTOR)
    lightLeft = GroveLineFinder(config.G_LINE_LEFT)
    lightRight = GroveLineFinder(config.G_LINE_RIGHT)
    imu = IMU()
    LineFollow.initLineFollow()

def enable():
    global state
    state = 1
    onEnable()
def disable():
    global state
    state = 0
    onDisable()
def stop():
    global state, BP
    state = -1
    BP.reset_all()

# when robot switches to enable
def onEnable():
    print("Enabled!")

startPos = 0

# 50 times per second while enabled
def enabledPeriodic():
    global drivetrain, lightLeft, lightRight, imu, startPos, state, dump
    if state==1:
        LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
        dump.idle()
    elif state==2:
        drivetrain.setPowers(0.6,0.6)
        drivetrain.setFrontAngle(0)
        dump.idle()
    elif state==3:
        drivetrain.setPowers(0.2,0.2)
        drivetrain.setFrontAngle(0)
        dump.idle()
        if imu.hasMagnet():
            startPos = drivetrain.getREncoder()
            state = 4
    if state == 4:
        print(startPos)
        print(startPos - 360 * (12 /(math.pi * config.WHEEL_RADIUS * 2)))
        print(drivetrain.getREncoder())
        drivetrain.setPowers(0.2,0.2)
        drivetrain.setFrontAngle(0)
        dump.idle()
        if drivetrain.getREncoder() < startPos - 360 * (12 /(math.pi * config.WHEEL_RADIUS * 2)):
            state = 5
            startPos = time.time()
    if state == 5:
        dump.dump()
        drivetrain.setPowers(0,0)
        drivetrain.setFrontAngle(0)
        if(time.time() > startPos+2):
            state = 2

        



    return

# runs once when robot becomes disabled (including when powered on)
def onDisable():
    global drivetrain, dump
    print("Disabled.")
    drivetrain.setPowers(0,0)
    drivetrain.setFrontAngle(0)
    dump.idle()
    

# runs 50 times per second while disabled
def disabledPeriodic():
    global state
    state =int( input("Enter new state: "))
    return


# enable/disable state logic and calling
robotInit()
onDisable()
disable()
while state!=-1:
    start = time.perf_counter_ns()
    try:
        print(state)
        if(state >= 1):
            enabledPeriodic()
        else:
            disabledPeriodic()
        # limiting the speed of our loop
        diff = time.perf_counter_ns() - start
        if(diff > config.NS_PER_TICK):
            print(f"LOOP OVERRUN. TOOK {diff}ns")
        else:
            time.sleep((config.NS_PER_TICK - diff) / 1e9)
    except KeyboardInterrupt:
        if(state >= 1):
            disable()
        else:
            stop()
