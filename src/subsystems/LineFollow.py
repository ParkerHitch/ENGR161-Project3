from src.subsystems.Drivetrain import TwoWheel
from src.subsystems.sensors.g_Light import GroveLightSensor
from src.util.PID import genericPID
import config

followPID: genericPID

def initLineFollow():
    global followPID
    followPID = genericPID(config.K_LINE_P, config.K_LINE_I, config.K_LINE_D, config.K_LINE_MAX)
    followPID.setDest(0)

def followBasicLine(dt: TwoWheel, lsl: GroveLightSensor, lsr: GroveLightSensor):
    global followPID

    # +1 if left is white, right is black, -1 if left is black, right is white
    diff = lsl.getBrightness() - lsr.getBrightness()
    correction = followPID.updateLoop(diff)
    # <0 if too far left, >0 if too far right
    print(diff)
    print(correction)
    powerL = config.BASE_SPEED - correction
    powerR = config.BASE_SPEED + correction

    dt.setPowers(powerL, powerR)


