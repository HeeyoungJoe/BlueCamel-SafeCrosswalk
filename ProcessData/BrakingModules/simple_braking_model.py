import numpy as np

LATENCY = 1
DRIVER_RESPONSE = 1


def simplemodel(vehicle_Initial_Speed, brake_acc = 4 ):

    vehicle_Mass = 1145;

    distance = (vehicle_Initial_Speed**2)/(2*brake_acc)
    time = vehicle_Initial_Speed/brake_acc
    return distance, time

def simplecheckBraking(velocity, distance, safe_time = 5):
    velocity = velocity / 3.6
    #print(velocity)
    braking_distance, arrival_time = simplemodel(velocity)

    safe_distance = (safe_time + LATENCY+DRIVER_RESPONSE) * velocity + braking_distance
    critical_distance = (LATENCY+DRIVER_RESPONSE)*velocity + braking_distance
    #print(critical_distance)
    if distance < critical_distance:
        return 1
    if distance <= safe_distance :
        maxtime = safe_time            # interval : [t_L + t_d <= t <= (dis_safe-dis_brake)/velocity)
        mintime = (LATENCY + DRIVER_RESPONSE)
        x = (distance-braking_distance)/velocity - (maxtime + mintime)/2
        return 1-(1/(1+np.exp(-x)))
    return 0



#print(simplemodel(100))
#print(simplecheckBraking(100,200, safe_time=5))

