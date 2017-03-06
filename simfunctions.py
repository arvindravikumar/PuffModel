"""
Defines all simulation functions that are used in the main simulation, Puff_Sim
"""
import numpy as np
import os
from scipy import integrate
import pickle


def save_results(dir_out, results):
    """
    Save results to a file
    Inputs:
        dir_out             Name of output file to save
        results             A results object
    """
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)
    n_scenario = len(os.listdir(dir_out))
    file_out = dir_out + '/scenario' + str(n_scenario) + '.p'
    pickle.dump(results, open(file_out, 'wb'))
    
    

def Puff_model(x, y, z, current_time, leak, atm, time, wind, angle):
    """
    Puff model that calculates spatial concentration of a given leak at each timestep
    Inputs: 
        x,y,z:          1-D of spatial coordinates where concentration is calculated
        current_time:   current time-step in the simulation
        leak:           leak size
        atm:            Object containing atmospheric parameters like stability class
        time:           Object containing various time parameters (Windstep, totaltime, etc.)
        wind:           wind speed at time, current_time
        angle:          wind direction at time, current_time
    Outputs: 
        cppm:           preliminary spatial concentration map at time, current_time
    """
    
    X, Y, Z = np.meshgrid(x,y,z)
    H = leak.height
    Q = leak.size
    Ffactor = leak.factors
    u = wind
    theta = angle
    
    X2 = X*np.cos(theta) + Y*np.sin(theta)
    Y2 = -X*np.sin(theta) + Y*np.cos(theta)
    X2[X2<0]=0
    
    conc = np.zeros([len(x), len(y), len(z)])
    f2 = np.zeros([len(x), len(y), len(z)])
    f3 = np.zeros([len(x), len(y), len(z)])
    time_int = np.zeros([len(x), len(y), len(z)])
    
    if np.mod(current_time,time.Windstep)!=0:
        times = np.mod(current_time,time.Windstep)
    else:
        times = time.Windstep
        
    sigmay = atm.k*X2/(1+X2/atm.a)**atm.p
    sigmaz = atm.l*X2/(1+X2/atm.a)**atm.q
    Zm = H + 1.6*Ffactor**(1/3)*X2**(2/3)/u
    alpha = Q/(2*np.pi*sigmay*sigmaz)**1.5
    alpha[alpha==np.inf]=0

    f1a = np.exp(-Y2**2/(2*sigmay**2))
    f1a[np.isnan(f1a)]=0
    f2 = np.exp(-(Z-Zm)**2/(2*sigmaz**2))
    f3 = np.exp(-(Z+Zm)**2/(2*sigmaz**2))
    
    c1 = 2*sigmay*sigmaz;
    pp, qq, rr = X2.shape
    time_int = np.array([integrate.quad(lambda t: np.exp(-(X2[i,j,k]-u*t)**2/c1[i,j,k]),0,times) \
                         for i in range(0,pp) for j in range(0,qq) for k in range(0,rr)])
    conc_int = np.reshape(time_int[:,0],X2.shape)
    conc = alpha*f1a*conc_int*(f2+f3)
    
    cppm = conc*1e6/656
    
    return cppm
    
    
    
    
    
    