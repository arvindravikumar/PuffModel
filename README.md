# PuffModel

This repo describes a time-dependent Gaussian plume model for methane leaks in relatively flat terrain.
It contains 3 files: 

DDSim1.py

This is the main simulation file that contains all required parameters. Variables like simulation time, leak-size, wind parameters can be manually changed. The output of this program is an python object called 'Final'. 'Final' gives the leak concentration as a function of space and time.

Atmosphere.py 

This file contains all the classes used by the puff model. The important ones include time parameters, atmosphere parameters, and leak parameters. It is called by the DDSim1 file. 

simfunctions.py

This file computes the puff model for different time itervals and returns the concentration map. Note that the concentration output from this program is only an intermediate step. The actual concentrations (called 'final') are computer in the main simulation file (DDSim1.py).
