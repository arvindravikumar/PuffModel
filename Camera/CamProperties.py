"""
"""
import numpy as np 
import scipy.ndimage as sn
from scipy import integrate

# Constants
h = 6.626e-34  # Planck's constant [J-s]
SIGMA = 5.67e-8  # Stefan-Boltzmann constant [W/m^2-K^4]
c = 3e8  # Speed of light [m/s]
k = 1.38e-23  # Boltzmann's constant [J/K]
N_A = 6.023e23  # Avogadro's number
ROOT2PI = np.sqrt(2*np.pi)
lambda1 = 3.2e-6
lambda2 = 3.4e-6
FoV1=24*np.pi/180
FoV2=18*np.pi/180
a_d=9e-10

def Pathlength(x0, y0, z0, x1, y1, z1, data):
    num = 201 #number of points in extrapolation
    x, y, z = np.linspace(x0, x1, num), np.linspace(y0, y1, num), np.linspace(z0, z1, num)
    concs = sn.map_coordinates(data, np.vstack((x,y,z)))
    test = sum(concs)/num #CPL as a fraction of total number of points in extrapolation
    return test


def pixelprop(T_g, T_plume):

    #Camera Properties assumed as default
    netd = 0.015
    f_number = 1.5
    e_a = 0.1
    e_g = 0.5
    
    if T_g is None:
        T_g = 300
    
    if T_plume is None:
        T_plume = 300
        
    T_a = T_g - 20
    
    w1g = h*c/(lambda2 * k * T_g)
    w2g = h*c/(lambda1 * k * T_g)
    n1 = 2 * np.pi * k**4 * T_g**3 / (h**3 * c**2)
    temp_y1 = -np.exp(-w1g) * (720+720 * w1g + 360 * w1g**2+120 * w1g**3 + 30 * w1g**4 + 6 * w1g**5 + w1g**6)
    temp_y2 = -np.exp(-w2g) * (720+720 * w2g + 360 * w2g**2+120 * w2g**3 + 30 * w2g**4 + 6 * w2g**5 + w2g**6)
    y1 = temp_y2 - temp_y1
    y = y1 * n1
    nep = y * netd * a_d / (4 * f_number**2)
    
    ppixelg = pixel_power(T_g)
    ppixelp = pixel_power(T_plume)
    ppixela = pixel_power(T_a)
    
    tec = ppixelp - e_g * ppixelg - e_a * (1-e_g) * ppixela
    
    Kav = 2.191e-20
    
    return nep, tec, Kav
    
def pixel_power(temp):
        """
        Calculate the the power incident on a pixel from an infinite blackbody emitter at a given temperature.
        Inputs:
            temp    Temperature of the emitter (K)
        Return:
            pixel_power   power incident on the pixel (W)
        """
        # Calculate the nondimensional frequency limits of the sensor
        w1 = h * c / (lambda2 * k * temp)
        w2 = h * c / (lambda1 * k * temp)
        # Integrate the blackobdy radiation over the frequency range
        temp_int = integrate.quad(lambda x: x**3 / (np.exp(x)-1), w1, w2)
        # calculate the power incident on one camera pixel
        frac = temp_int[0] / (np.pi**4 / 15)
        sblaw = SIGMA * temp**4 * a_d
        power = (4/np.pi) * sblaw * np.tan(FoV1 / 2) * np.tan(FoV2 / 2)
        pixel_power = power * frac
        return pixel_power