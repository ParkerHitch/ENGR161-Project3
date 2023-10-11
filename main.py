from src.subsystems.Drivetrain import TwoWheel
from src.subsystems.sensors.g_Light import groveLightSensor
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
lightLeft: groveLightSensor
lightRight: groveLightSensor

# stuff to do upon starting python
def robotInit():
    print("Power on.")
    drivetrain = TwoWheel(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR)
    lightLeft = groveLightSensor(config.G_LIGHT_LEFT)
    lightRight = groveLightSensor(config.G_LIGHT_RIGHT)

def enable():
    state = 1
    onEnable()
def disable():
    state = 0
    onDisable()
def stop():
    state = -1

# when robot switches to enable
def onEnable():
    print("Enabled!")

# 50 times per second while enabled
def enabledPeriodic():
    return

# runs once when robot becomes disabled (including when powered on)
def onDisable():
    drivetrain.setPowers(0,0)
    print("Disabled!")

# runs 50 times per second while disabled
def disabledPeriodic():
    return


# enable/disable state logic and calling
robotInit()
onDisable()
while state!=-1:
    start = time.perf_counter_ns()
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
    