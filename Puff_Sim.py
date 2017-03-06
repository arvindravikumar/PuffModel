import Sim_classes as At
import numpy as np 
import simfunctions as sf
import random
import pickle

def Sensor(Leaksize=None, LeakHeight=None, TSim=None, Tstep=None, x=None, y=None, z=None, dir_out='Results'):
    
    """
    Main program that calculates leak concentration from a single leak across a given time period. Inputs are described below: 
        Leaksize:       size of the leak in g/s (default: random leak from the Python object file LeakData.p)
        LeakHeight:     height of leak above ground in m (default: 2 m)
        x:              Locations along x-axis where concentration is to be calculated, input as array (default: -51 to 49 m in steps of 5 m)
        y:              Locations along y-axis where concentration is to be calculated, input as array (default: -50 to 50 m in steps of 5 m)
        z:              Locations along z-axis where concentration is to be calculated, input as array (default: 0 to 5 m in steps of 1 m)
        TSim:           Total simulation time in seconds (default: 600 sec / 10 min)
        Tstep:          Step size of temporal concentration profiles required (default: 30 sec)
        
        Wind data is automatically extracted from the object file WindData.p, based on the total simulation time. Wind data is taken from 1-min data \\
        Dallas FortWorth (DFW) weather monitoring site published by NOAA
        
        Leak source is assumed to be at the origin (since only one leak is being considered). The program can be modified to \\
        address non-0 locations for the source.
    """
    #-----------------Define Default Settings------------------------------------------
    
    if Leaksize is None:
        AllLeaks = pickle.load(open('LeakData.p', 'rb'))
        Leaks = random.sample(AllLeaks.leak_size, 1)
        Leaksize = Leaks[0]

    if LeakHeight is None:
        LeakHeight = 2
    
    if TSim is None:
        TSim = 600
        
    if Tstep is None:
        Tstep = 30
        
    if x is None:
        xloc = np.linspace(-51, 49, 21)
        
    if y is None:
        yloc = np.linspace(-50, 50, 21)
        
    if z is None:
        zloc = np.linspace(0, 5, 6)
        
    #------------------------------------------------------------------------------------
    # Initializing wind data from python object, including angles 
    # Wind is selected sequentially depending on total simulation time

    Windstep = 60
    Windsize = int(TSim/Windstep)

    sim_time = At.Time(TSim, Tstep, Windstep)
    leak = At.Leak(Leaksize, LeakHeight)

    W = pickle.load(open('WindData.p','rb'))
    start = random.randint(0, len(W.wind) - Windsize)
    list1 = W.wind[start: start+Windsize]   #sequential selection
    list2 = W.direction[start: start+Windsize]
    wind_speed = np.array(list1)
    wind_angle = np.array(list2)
    wind_angles = (wind_angle - 180)*np.pi/180

    rep_factor = int(Windstep/Tstep)

    winds = np.repeat(wind_speed, rep_factor)
    angles = np.repeat(wind_angles, rep_factor)

    concentration = np.empty((len(winds),1),dtype=object)
    
    ##--------------------Puff Model Simulation---------------------------------------

    for ind in range(0, len(sim_time.T)):
        curr_time = sim_time.T[ind]
        atm = At.Atmos(winds[ind])
        concentration[ind,0] = sf.Puff_model(xloc, yloc, zloc, curr_time, leak, atm, sim_time, winds[ind], angles[ind])
        
    #-----------Calculating Concentration-------------------------------------------
    
    quotient = (sim_time.T-1)//Windstep
    index = (1+quotient)*rep_factor-1

    off = np.zeros((len(winds)+rep_factor,1),dtype=object)

    for m in range(0, len(sim_time.T)):
        temp = int(index[m])
        off[m+rep_factor,0] = concentration[temp,0]-concentration[m,0]

    final = np.empty((len(winds),1),dtype=object)

    for p in range(0, len(sim_time.T)):
        final[p,0] = concentration[p,0] + off[p,0]

    #---------------Saving results as a python object for further analysis----------------
    #Results will be stored as scenario# in the folder 'Results' in the working directory

    Result = At.Results(sim_time.T, Leaksize, final, xloc, yloc, zloc, LeakHeight, winds, wind_angle)
    sf.save_results(dir_out, Result)




    
    
    




