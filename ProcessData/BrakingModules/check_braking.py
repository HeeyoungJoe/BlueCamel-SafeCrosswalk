from ProcessData.BrakingModules.python_wrapper_braking import getbrakinginfo
import numpy as np

LATENCY = 1
DRIVER_RESPONSE = 1

def checkBraking(velocity, distance, safe_time = 5):
    braking_distance, arrival_time = getbrakinginfo(velocity)

    safe_distance = (safe_time + LATENCY+DRIVER_RESPONSE) * velocity + braking_distance
    critical_distance = (LATENCY+DRIVER_RESPONSE)*velocity + braking_distance

    if distance < critical_distance:
        return 1
    if distance <= safe_distance :
        maxtime = safe_time            # interval : [t_L + t_d <= t <= (dis_safe-dis_brake)/velocity)
        mintime = (LATENCY + DRIVER_RESPONSE)
        x = (distance-braking_distance)/velocity - (maxtime + mintime)/2
        return 1-(1/(1+np.exp(-x)))
    return 0







