import config
import brickpi3
from src.subsystems.sensors.g_LineFinder import GroveLineFinder
from src.subsystems.Drivetrain import RearWheelDriveFrontWheelSteer
import src.subsystems.LineFollow as LineFollow
from src.subsystems.sensors.IMU import IMU

glfl = GroveLineFinder(config.G_LINE_LEFT)
glfr = GroveLineFinder(config.G_LINE_RIGHT)

BP = brickpi3.BrickPi3()
drivetrain = RearWheelDriveFrontWheelSteer(BP, config.LEFT_MOTOR, config.RIGHT_MOTOR, config.FRONT_MOTOR, 0)
LineFollow.initLineFollow()
imu = IMU()
imu.initialize()

while True:
    # print(glfl.getRawVal(), glfr.getRawVal())
    LineFollow.keepLeft(drivetrain, glfl, glfr)
#    imu.update()
    if imu.hasMagnet():
        print("MAGNET!!")
