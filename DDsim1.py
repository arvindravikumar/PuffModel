"""
Program to calculate methane concentration in ppm across given domain
"""
import Atmosphere as At
import numpy as np 
import simfunctions as sf

TSim = 600
Tstep = 30
Windstep = 60

sim_time = At.Time(TSim, Tstep, Windstep)

rate = 1
size = rate*Tstep
height = 2.01

leak = At.Leak(rate, size, height)

xloc = np.linspace(-51,49,20)
yloc = np.linspace(-50,50,20)
zloc = np.linspace(0,5,6)

wind_speed = np.array([2.2, 2.5, 1.8, 4, 5.5, 6.2, 4.7, 3.2, 3.8, 5.1])
wind_angle = np.array([211, 206, 199, 198, 196, 196, 204, 205, 200, 206])
wind_angle = wind_angle - 180
wind_angle = wind_angle*np.pi/180

rep_factor = Windstep/Tstep

wind = np.repeat(wind_speed, rep_factor)
angle = np.repeat(wind_angle, rep_factor)

concentration = np.empty((len(wind),1),dtype=object)

for ind in range(0, len(sim_time.T)):
    curr_time = sim_time.T[ind]
    atm = At.Atmos(wind[ind])
    concentration[ind,0] = sf.Puff_model(xloc, yloc, zloc, curr_time, leak, atm, sim_time, wind[ind], angle[ind])
    
quotient = (sim_time.T-1)//Windstep
index = (1+quotient)*rep_factor-1

off = np.zeros((len(wind)+2,1),dtype=object)

for m in range(0, len(sim_time.T)):
    temp = int(index[m])
    off[int(m+rep_factor),0] = concentration[temp,0]-concentration[m,0]

final = np.empty((len(wind),1),dtype=object)

for p in range(0, len(sim_time.T)):
    final[p,0] = concentration[p,0] + off[p,0]



    
    
    




