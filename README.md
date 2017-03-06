# PuffModel

This repo describes a time-dependent Gaussian plume model for methane leaks in relatively flat terrain. This read-me file describes all the files and folders present in the simulation.

Data_Input:

This folder contains helper code to convert input databases (leak sizes and wind speed/direction) in CSV format to easily readable python object data files. In addition to the code, the folder contains the following two python object files:

LeakData.p - an object with leak sizes in g/s taken from empirically measured values in Texas by Eastern Research Group as part of Texas Air Quality Study. Source data can be found here: http://fortworthtexas.gov/gaswells/air-quality-study/final/

WindData.p - an object with wind-speed (m/s) and wind-direction (degrees) information at 1-min time resolution for Dallas Fort-Worth area for the month of July, 2015, obtained from NOAA (National Weather Service) here: ftp://ftp.ncdc.noaa.gov/pub/data/asos-onemin/6405-2015/ 
Data for the Dallas-FortWorth location can be found by downloading the file starting with '64050KDFW...'

In addition, original CSV files can also be found for the leak data (ProdPop.csv) and wind data (DFW07clean.csv).

Code files: 
LeakPopulation.py: converting leak size csv files to python object files.
windreader.py: converting wind data csv files to python object files. 
inputclass.py: Classes that define object data files.

-----------------------------------------------------------------------------------------


Puff_Sim.py

This is the main simulation file that takes input data (user provided or otherwise) and calculates time dependent concentration profiles for a given leak size. Currently, it calculates concentration for a single leak, assumed to be at the origin. Results from this simulation (concentration, wind speed, wind direction, etc.) will be stored in a folder called 'Results' with each simulation having the name 'scenario#', where # represents the number of the simulation. Details regarding input parameters can be found within the python file. 

Sim_classes.py 

This file contains all simulation classes used by the main Puff_Sim simulation. Briefly, 
Atmos: stores atmospheric parameters to calculate dispersion coefficients based on various stability classes.
Time: Defines time parameters required for simulation (Total simulation time, time step for simlation, time step for wind-speeds, current time of simulation)
Results: Parameters that are saved after each simulation
Leak Defines leak parameters including leak size, height of leak, density of methane and air, gravity and buoyancy factor. 

simfunctions.py

This file contains two functions, one for saving final simulation results and another to calculate the gaussian puff. More details can be found within the file.