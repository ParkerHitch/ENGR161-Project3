# corosponds to 50 ticks per second
NS_PER_TICK = 2e7

# physical info
BACK_SEPARATION = 7.5 # inches, distance between the centers of the back wheels
Y_SEPARATION = 9.75 # inches, distance between center of back to center of front wheel

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

G_LIGHT_LEFT = 1
G_LIGHT_RIGHT = 0

G_LINE_LEFT = 2
G_LINE_RIGHT = 7

# Line follow
BASE_SPEED = 0.075
BASE_SPEED_DPS = 45
K_LINE_P = 1
K_LINE_MAX_I = 25
K_LINE_I = 1/25
K_LINE_D = 0
K_LINE_MAX = 1

