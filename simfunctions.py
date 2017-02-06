"""
defines all simulation functions that are called by other files
"""
import numpy as np
from scipy import integrate

def set_kwargs_attrs(obj_in, kwargs, only_existing=True):
    """
    Function for overwriting parameters with key word arguments
    Inputs:
        obj_in          Object with parameters to be updated
        kwargs          Dict containing new parameter values
        only_existing   Determines with new parameters can be created with kwargs
    """
    for key in kwargs.keys():
        # If only_existing is true, only set attributes that already exist
        if only_existing:
            if not hasattr(obj_in, key):
                raise ValueError("Tried to set invalid attribute. Class: ", type(obj_in), 'attempted attribute:', key)
        setattr(obj_in, key, kwargs[key])
        
def Puff_model(x, y, z, current_time, leak, atm, time, wind, angle):
    
    X, Y, Z = np.meshgrid(x,y,z)
    H = leak.height
    Q = leak.size
    Qt = leak.delta_leak
    Ffactor = leak.factors
    u = wind
    theta = angle
    Tstep = time.timestep
    
    X2 = X*np.cos(theta) + Y*np.sin(theta)
    Y2 = -X*np.sin(theta) + Y*np.cos(theta)
    X2[X2<0]=0
    
    conc = np.zeros([len(x), len(y), len(z)])
    f2 = np.zeros([len(x), len(y), len(z)])
    f3 = np.zeros([len(x), len(y), len(z)])
    time_int = np.zeros([len(x), len(y), len(z)])
    x
    if np.mod(current_time,time.Windstep)!=0:
        times = np.mod(current_time,time.Windstep)
    else:
        times = time.Windstep
        
    sigmay = atm.k*X2/(1+X2/atm.a)**atm.p
    sigmaz = atm.l*X2/(1+X2/atm.a)**atm.q
    Zm = H + 1.6*Ffactor**(1/3)*X2**(2/3)/u
    alpha = Qt/(2*np.pi*sigmay*sigmaz)**1.5
    alpha[alpha==np.inf]=0

    f1a = np.exp(-Y2**2/(2*sigmay**2))
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
    
    
    
    
    
    