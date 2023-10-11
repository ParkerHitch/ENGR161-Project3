import matplotlib.pyplot as plt
from src.util.PID import genericPID
import time
import config

controller = genericPID(0.2, 0.05, 1, 1, 0.01, 0.001)
controller.setDest(0)

pos = [-1]
t = [0]

tStep = 0.02

while not controller.atSetpoint() and len(pos) < 500:
    start = time.perf_counter_ns()
    correction = controller.updateLoop(pos[-1])
    pos.append(pos[-1]+correction)
    t.append(t[-1]+tStep)
    # limiting the speed of our loop
    diff = time.perf_counter_ns() - start
    if(diff > config.NS_PER_TICK):
        print(f"LOOP OVERRUN. TOOK {diff}ns")
    else:
        time.sleep((config.NS_PER_TICK - diff) / 1e9)

plt.plot(t, pos)
plt.show()