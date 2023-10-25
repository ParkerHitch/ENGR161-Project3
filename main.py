from src.subsystems.Drivetrain import RearWheelDriveFrontWheelSteer
from src.subsystems.sensors.g_Light import GroveLightSensor
import src.subsystems.LineFollow as LineFollow
import config
import brickpi3
import time

from src.subsystems.sensors.g_LineFinder import GroveLineFinder


print("Hello Project 3!")

BP = brickpi3.BrickPi3()

# 0 = disabled
# 1 = following a basic line
state = 0

# declaring our subsystem variables
drivetrain: RearWheelDriveFrontWheelSteer
lightLeft: GroveLineFinder
lightRight: GroveLineFinder

# stuff to do upon starting python
def robotInit():
    global drivetrain, lightLeft, lightRight, BP
    drivetrain = RearWheelDriveFrontWheelSteer(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR, config.FRONT_MOTOR, 0)
    lightLeft = GroveLineFinder(config.G_LINE_LEFT)
    lightRight = GroveLineFinder(config.G_LINE_RIGHT)

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

# 50 times per second while enabled
def enabledPeriodic():
    global drivetrain, lightLeft, lightRight
    LineFollow.followBasicLineDigital(drivetrain, lightLeft, lightRight)
    return

# runs once when robot becomes disabled (including when powered on)
def onDisable():
    global drivetrain
    print("Disabled.")
    drivetrain.setPowers(0,0)
    

# runs 50 times per second while disabled
def disabledPeriodic():
    return


# enable/disable state logic and calling
robotInit()
onDisable()
enable()
while state!=-1:
    start = time.perf_counter_ns()
    try:
        if(state == 1):
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
        stop()
