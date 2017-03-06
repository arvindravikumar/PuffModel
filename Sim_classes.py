"""
Basic classes used by in Puff Simulation
"""

import numpy as np

class Atmos:
  """
  Defines atmosphere variables for puff simulation, including parameters for various stability classes
  """
  def __init__(self, wind_speed):
      
      """
      Inputs: wind_speed, automatically passed in Puff_Sim function
      """
      self.stab_class = []
      a = np.array([927, 370, 283, 707, 1070])
      l = np.array([0.102, 0.0962, 0.0722, 0.0475, 0.0335])
      q = np.array([-1.918, -0.101, 0.102, 0.465, 0.624])
      k = np.array([0.25, 0.202, 0.134, 0.0787, 0.0566])
      p = np.array([0.189, 0.162, 0.134, 0.135, 0.137])
      
      if wind_speed < 2:
        self.stab_class = 0
      elif wind_speed < 5:
        self.stab_class = 1
      elif wind_speed < 6:
        self.stab_class = 2
      else:
        self.stab_class = 3

      self.a = a[int(self.stab_class)]
      self.l = l[int(self.stab_class)]
      self.q = q[int(self.stab_class)]
      self.k = k[int(self.stab_class)]
      self.p = p[int(self.stab_class)]


class Time:
  """
  Defines time parameters that are used for the entire simulation
  TSim:         Total simulation time in seconds
  TStep:        Time step used for simulation
  Windstep:     Time step at which wind data will be updated (60 seconds)
  """
  def __init__(self, TSim, TStep, Windstep):
    
      self.totaltime = TSim
      self.timestep = TStep
      self.Windstep = Windstep
      self.T = np.linspace(TStep,TSim,TSim/TStep)
      

class Results:
  """
  Used to save the results from a single simulation. Data stored include:
  time:     Time series of simulation
  leak:     Leak size
  ppm:      Spatial and temporal leak concentration in ppm as a python object
  x,y,z:    Spatial coordinates where ppm is calculated
  height:   Leak height
  winds:    Array of winds used in calculation
  angles:   Array of angles used in calculation
  """
  def __init__(self, time, leak, ppm, x, y, z, height, winds, angles):
      self.time = time
      self.leak = leak
      self.ppm = ppm
      self.x = x
      self.y = y
      self.z = z
      self.height = height
      self.winds = winds
      self.angles = angles
      
class Leak:
  """
  Used to define all paramters for a single leak, assumed to be at (0,0,H) 
  leakrate:     leak size in g/s
  H:            height of leak above ground in m
  rhom:         Density of methane
  rhoa:         Density of air
  g:            Acceleration due to gravity
  factors:      Buoyancy factor for methane
  """
  def __init__(self, leakrate, H):
      self.size = leakrate
      self.height = H + 0.01
      rhom = 681
      rhoa = 1225
      g = 9.8
      self.factors = g*leakrate*(1/np.pi)*(1/rhom - 1/rhoa)
            