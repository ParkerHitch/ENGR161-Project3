from src.subsystems.sensors.g_Ultrasonic import GroveUltrasonic
import config
import time

dist = GroveUltrasonic(config.G_ULTRASONIC)

while True:
    d = dist.getRawVal()
    if (d < config.DIST_THRESH):
        print(d, "WALL")
    else:
        print(d)
    time.sleep(0.02)
