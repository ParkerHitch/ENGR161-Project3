from math import pi, radians
# corosponds to 50 ticks per second
NS_PER_TICK = 2e7

# physical info
BACK_SEPARATION = 7.5 # inches, distance between the centers of the back wheels
Y_SEPARATION = 9.75 # inches, distance between center of back to center of front wheel
WHEEL_RADIUS = 1.5
WHEEL_RADIUS_CM = 3.4

# brickpi ports (I really don't want to create 2 BrickPi3 instances)
BP_PORT_1 = 0x01
BP_PORT_2 = 0x02
BP_PORT_3 = 0x04
BP_PORT_4 = 0x08

BP_PORT_A = 0x01
BP_PORT_B = 0x02
BP_PORT_C = 0x04
BP_PORT_D = 0x08

# Ports
LEFT_MOTOR = BP_PORT_C
RIGHT_MOTOR = BP_PORT_B
FRONT_MOTOR = BP_PORT_A
DUMP_MOTOR = BP_PORT_D

G_LIGHT_LEFT = 1
G_LIGHT_RIGHT = 0

G_LINE_LEFT = 2
G_LINE_RIGHT = 7
G_HAL = 3
G_ULTRASONIC = 6

# Line follow
BASE_SPEED = 0.6
BASE_SPEED_DPS = 90
K_LINE_P = 1
K_LINE_MAX_I = 25
K_LINE_I = 1/25
K_LINE_D = 0
K_LINE_MAX = 1

R_MIN = 0.6

DIST_THRESH = 20

SPEED_TRANSFORM = 30/27

MAGNET_COOLDOWN = 1
DUMP_DRIVE_DIST = 20
DUMP_TIME = 2

PATH_ANG = pi/8
DOWNHILL_ANG = -radians(10)

# IMU
MAG_THRESH = 300
MAG_ANG = 0.1
FILTER = [[0.7,1.0],[0.7,1.0],[0.7,1.0],[0.7,1.0],[0.7,1.0],[0.7,1.0],[5,2],[5,2],[5,2]]
STDEV_COUNT = 3
