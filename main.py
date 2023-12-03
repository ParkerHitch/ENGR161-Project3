import math
import lib.RMath as rmath
from src.subsystems.Drivetrain import RearWheelDriveFrontWheelSteer
from src.subsystems.sensors.g_Light import GroveLightSensor
import src.subsystems.LineFollow as LineFollow
import config
import brickpi3
import time

from src.subsystems.sensors.g_LineFinder import GroveLineFinder
from src.subsystems.Dump import Dump
from src.subsystems.sensors.IMU import IMU
from src.subsystems.sensors.g_Ultrasonic import GroveUltrasonic

print("Hello Project 3!")

BP = brickpi3.BrickPi3()

# 0 = disabled
# anything else = enabled
state = 0
magnetsHit = 0
timeLastHit = 0
targetSite = 1
startAng = 0

# declaring our subsystem variables
drivetrain: RearWheelDriveFrontWheelSteer
lightLeft: GroveLineFinder
lightRight: GroveLineFinder
dump: Dump
imu: IMU
distSense: GroveUltrasonic

# stuff to do upon starting python
def robotInit():
    global drivetrain, lightLeft, lightRight, dump, imu, BP, distSense
    drivetrain = RearWheelDriveFrontWheelSteer(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR, config.FRONT_MOTOR, 0)
    dump = Dump(BP, config.DUMP_MOTOR)
    lightLeft = GroveLineFinder(config.G_LINE_LEFT)
    lightRight = GroveLineFinder(config.G_LINE_RIGHT)
    distSense = GroveUltrasonic(config.G_ULTRASONIC)
    imu = IMU()
    imu.initialize()
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
    global imu, magnetsHit, timeLastHit
    imu.zeroOrientation()
    magnetsHit = 0
    timeLastHit = 0
    print("Enabled!")

dumpStartPos = 0
dumpStartTime = 0
brightnessSum = 0

def startDump():
    global dumpStartPos, state, drivetrain
    dumpStartPos = drivetrain.getREncoder()
    drivetrain.setFrontAngle(0)
    state = 4

# 50 times per second while enabled
def enabledPeriodic():
    global drivetrain, lightLeft, lightRight, imu, dumpStartPos, state, dump, magnetsHit, timeLastHit, targetSite, startAng, dumpStartTime, brightnessSum, distSense
    imu.update()

    if imu.hasMagnet():
        print("MAGNET!!")
        if time.time() > timeLastHit + config.MAGNET_COOLDOWN:
            magnetsHit += 1
        timeLastHit = time.time()

    if distSense.hasWall():
        return

    # normal driving and wating until we hit the proper number of magnets
    if state==1:
        print("Magnets: ", magnetsHit)
        dump.idle()

        if magnetsHit == 0:
            LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
        elif magnetsHit == targetSite:
            if targetSite <= 2:
                # Exit onto branch
                LineFollow.keepRight(drivetrain, lightLeft, lightRight)
                state = 2
                startAng = imu.getYaw()
            else:
                LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
                # Start dumping
                startDump()
        else:
            LineFollow.keepLeft(drivetrain, lightLeft, lightRight)
    #turn onto branch
    elif state==2:
        LineFollow.keepRight(drivetrain, lightLeft, lightRight)
        dump.idle()
        # clockwise
        if imu.getYaw() < startAng - config.PATH_ANG:
            # follow normally until we hit a magnet
            state = 3
    #drive normally until we hit the dropoff magnet
    elif state==3:
        LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
        dump.idle()
        if magnetsHit == targetSite+1:
            # dumping time
            startDump()
    # Drive forward until we are in position to dump
    elif state==4:
        # drivetrain.setSpeeds(config.BASE_SPEED_DPS, config.BASE_SPEED_DPS)
        # drivetrain.setFrontAngle(0)
        LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
        dump.idle()

        # if we have moved DUMP_DRIVE_DIST inches since when we started dumping...
        if drivetrain.getREncoder() < dumpStartPos - 360 * (config.DUMP_DRIVE_DIST /(math.pi * config.WHEEL_RADIUS * 2)):
            state = 5
            dumpStartTime = time.time()
    # stop and dump for DUMP_TIME seconds
    elif state==5:
        drivetrain.setPowers(0,0)
        # drivetrain.setFrontAngle(0)
        dump.dump()
        if time.time() > dumpStartTime + config.DUMP_TIME:
            dumpStartPos = drivetrain.getREncoder()
            state = 6
    # at this point we have dumped
    # we drive but leave the dump down for a bit just to make sure it falls off
    elif state==6:
        LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
        # leave the dump down for a bit just to make sure it falls off
        dump.dump()
        if time.time() > dumpStartTime + config.DUMP_TIME + 5:
            state = 7
    # return the dump to idle and then drive normal until we see white for
    # a decent amount of time. Then disable.
    elif state==7:
        LineFollow.keepRight(drivetrain, lightLeft, lightRight)
        dump.idle()
        # adds 0.25 if both white, subtracts 0.75 if both black, subtracts 0.25 if different
        brightnessSum += (lightLeft.readandAverage() + lightLeft.readandAverage())/2 - 0.75
        brightnessSum = rmath.minClamp(0, brightnessSum)

        # if seeing white for 3/4 of second
        if brightnessSum >= 0.25 * (0.75 * 50):
            state = 8
    elif state == 8:
        LineFollow.keepLeft(drivetrain, lightLeft, lightRight)
        dump.idle()
        
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
    global state, targetSite
    state =int( input("Enter new state: "))
    if state == 4:
        startDump()
    else:
        targetSite = int(input("Enter target site: "))
    return


# enable/disable state logic and calling
robotInit()
onDisable()
disable()
while state!=-1:
    start = time.perf_counter_ns()
    try:
        print("State: ", state)
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
