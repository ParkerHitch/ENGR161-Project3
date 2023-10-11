# corosponds to 50 ticks per second
NS_PER_TICK = 2e7

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
LEFT_MOTOR = BP_PORT_A
RIGHT_MOTOR = BP_PORT_B

G_LIGHT_LEFT = 0
G_LIGHT_RIGHT = 1

# Line follow
BASE_SPEED = 0.25
K_LINE_P = 0.5
K_LINE_I = 0
K_LINE_D = 0
K_LINE_MAX = 0.5
