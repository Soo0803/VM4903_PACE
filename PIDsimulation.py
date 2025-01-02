import numpy as np
import matplotlib.pyplot as plt
from itertools import count
import pandas as pd
import PID as pid
import time 

from matplotlib.animation import FuncAnimation

# Simulation parameters
# Ku = 1
Kp = 1
Ki = 0
Kd = 0

current_load = 0
simulation_time = 100
last_time = time.time()
# dt = 0.1

targetload = 50
xvalue = []
currentloadvalue = []
setpointvalue = [] # the target load 

index = count()

# Initialize PID controller
pidinit = pid.PID(Kp, Ki, Kd, targetload)


def animate(frame):
    global current_load
    current_load = pidinit.compute(current_load)
    print(current_load)
    print("\n")

    currentloadvalue.append(current_load)
    xvalue.append(frame)
    setpointvalue.append(targetload)
    plt.cla()
    plt.plot(xvalue, setpointvalue, color = 'red') # the targetload
    plt.plot(xvalue, currentloadvalue) # current load 

fig = plt.figure()

ani = FuncAnimation(fig, animate, interval = 1000, frames= 100) 

plt.show()
    


# time = np.arange(0, simulation_time + dt , dt)
# feedbacks = []
# outputs = []
# current_value = initial_value

# for t in time:
#     feedbacks.append(current_value)
#     output = pid.compute(current_value, dt)
#     current_value += output * dt
#     outputs.append(output)

# # Plot the results
# plt.figure(figsize=(10, 6))
# plt.plot(time, feedbacks, label='Feedback')
# plt.plot(time, [setpoint] * len(time), linestyle='--', color='red', label='Setpoint')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.title('PID Simulation')
# plt.legend()
# plt.grid(True)
# plt.show()