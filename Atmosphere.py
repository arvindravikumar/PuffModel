# -*- coding: utf-8 -*-
"""
Basic classes used by FEAST
"""

import numpy as np
from simfunctions import set_kwargs_attrs

class Atmos:
  """
  Defines atmosphere variables for puff simulation: calm conditions assumed
  """
  def __init__(self, wind_speed, **kwargs):
    
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

      set_kwargs_attrs(self,kwargs)
    
      self.a = a[int(self.stab_class)]
      self.l = l[int(self.stab_class)]
      self.q = q[int(self.stab_class)]
      self.k = k[int(self.stab_class)]
      self.p = p[int(self.stab_class)]


class Time:
  """
  Defines time parameters that are used for the entire simulation
  """
  def __init__(self, TSim, TStep, Windstep):
    
      self.totaltime = TSim
      self.timestep = TStep
      self.Windstep = Windstep
      self.T = np.linspace(TStep,TSim,TSim/TStep)
      

class Results:
  """
  Used to save the results from a simulation
  """
  def __init__(self, time, leak, ppm):
      self.time = time
      self.leak = leak
      self.ppm = ppm
      
class Leak:
  """
  Used to define all paramters for a single leak 
  """
  def __init__(self, leakrate, leaksize, H):
      self.size = leakrate
      self.delta_leak = leaksize
      self.height = H
      rhom = 681
      rhoa = 1225
      g = 9.8
      self.factors = g*leakrate*(1/np.pi)*(1/rhom - 1/rhoa)
            