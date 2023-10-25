from src.subsystems.Drivetrain import TwoWheel
from src.subsystems.sensors.g_Light import GroveLightSensor
import src.subsystems.LineFollow as LineFollow
import config
import brickpi3
import time
import matplotlib.pyplot as plt


print("Hello Project 3!")

BP = brickpi3.BrickPi3()

# 0 = disabled
# 1 = following a basic line
state = 0

# declaring our subsystem variables
drivetrain: TwoWheel
lightLeft: GroveLightSensor
lightRight: GroveLightSensor

times = []
valLeft = []
valRight = []
quotient = []
difference = []

# stuff to do upon starting python
def robotInit():
    global drivetrain, lightLeft, lightRight, BP
    drivetrain = TwoWheel(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR)
    lightLeft = GroveLightSensor(config.G_LIGHT_LEFT)
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
    times.append(0.0)
    valLeft.append(lightLeft.getRawVal())
    valRight.append(lightRight.getRawVal())
    difference.append(0.0)
    quotient.append(0.0)

# 50 times per second while enabled
def enabledPeriodic():
    global drivetrain, lightLeft, lightRight, time, valLeft, valRight, quotient, difference

    drivetrain.setPowers(0.1,0.1)

    times.append(times[-1]+0.02)
    valLeft.append(lightLeft.getRawVal())
    valRight.append(lightRight.getRawVal())
    difference.append(valLeft[-1]-valRight[-1])
    quotient.append(  valLeft[-1]/valRight[-1])

    if(len(times) > 50*5):
        stop()

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
        print("ERROR")
        stop()

fig, ax1 = plt.subplots()

ax1.plot(times, valLeft, times, valRight, times, difference)

ax2 = ax1.twinx()
ax2.plot(times, quotient, color='r')

ax1.legend(['Left Sensor Value','Right Sensor Value', 'diff',])
ax2.legend(['quotient'])
plt.show()
