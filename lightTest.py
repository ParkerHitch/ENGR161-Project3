from src.subsystems.Drivetrain import TwoWheel
from src.subsystems.sensors.g_Light import GroveLightSensor
import src.subsystems.LineFollow as LineFollow
import config
import brickpi3
import time


print("Hello Project 3!")

BP = brickpi3.BrickPi3()

# 0 = disabled
# 1 = following a basic line
state = 0

# declaring our subsystem variables
drivetrain: TwoWheel
lightLeft: GroveLightSensor
lightRight: GroveLightSensor

# stuff to do upon starting python
def robotInit():
    global drivetrain, lightLeft, lightRight, BP
    drivetrain = TwoWheel(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR)
    print(drivetrain)
    lightLeft = GroveLightSensor(config.G_LIGHT_LEFT, 70)
    lightRight = GroveLightSensor(config.G_LIGHT_RIGHT)

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
    print(lightRight.getRawVal() - lightLeft.getRawVal())
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
    except:
        stop()
