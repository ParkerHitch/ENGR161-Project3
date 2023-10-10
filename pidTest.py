import matplotlib.pyplot as plt
from util.PID import genericPID
import time

controller = genericPID(0.2, 0.05, 1, 1, 0.01, 0.001)
controller.setDest(0)

pos = [-1]
t = [0]

tStep = 0.02

while not controller.atSetpoint() and len(pos) < 500:
    time.sleep(tStep)
    correction = controller.updateLoop(pos[-1])
    pos.append(pos[-1]+correction)
    t.append(t[-1]+tStep)

plt.plot(t, pos)
plt.show()