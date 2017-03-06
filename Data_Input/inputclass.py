"""
This module defines classes to re-format input data files
@author: arvindr
"""

class WindInfo():
    def __init__(self, wind_speed, direction):
        self.wind = wind_speed
        self.direction = direction
        
class LeakInfo():
    def __init__(self, leak_size):
        self.leak_size = leak_size
        
        
        
