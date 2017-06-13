"""
Defines detection as seen by a camera object
Inputs: 
       Conc:  2-D array with 4 columns with (X,Y,Z,Concentration) information. Each time-step should be passed
              separately to this program. Furthermore, it is also assumed that z-axis locations change the fastest 
              in the array, followed by Y and X. If X changes the fastest, followed by Y and then Z, the reshape 
              command for ppm on line 46 should be modified with order parameter as 'F' instead of 'C'. Concentration
              units are assumed to be in g/m^3
      X,Y,Z:  array of x-, y-, z-locations where concentration is calculated 
     CamLoc:  Location of IR cameras as an (x,y,z) tuple
     CamDir:  Direction camera is pointing as an (x,y,z) tuple.
Outputs:
     Detect:  Binary variable based on whether the leak is detected (1) or not (0) based on the given concentration
              map.
         
"""
import numpy as np
import CamProperties as cp

NA = 6.023e23 # Avogadro's number
tau_air = 1 #transmission coefficient of air (assumed 1)

def Camera(Conc=None, X=None, Y=None, Z=None, CamLoc=None, CamDir=None):
    
    if CamLoc is None:
        CamLoc = (0, 0, 0)
        
    if CamDir is None:
        CamDir = (1, 1, 1)
        
    if Conc is None:
        Conc = np.ones((18491, 4))*10e-3 #Example numbers: Uniform concentration of about 15 ppm
        #Conc = np.random.lognormal(mean=1.0, sigma=1.0, size=(50,50,10))
        
    if X is None:
        X = np.linspace(-200, 200, 41) #Default X values
        
    if Y is None:
        Y = np.linspace(-200, 200, 41) #Default Y values
        
    if Z is None:
        Z = np.linspace(0, 10, 11) #Default Z values
        
    nx, ny, nz = np.size(X), np.size(Y), np.size(Z)
    
    ppm = np.reshape(Conc[:,3], (nx, ny, nz), order='C') #reshaping concentration column as a 3D array
    
#---------Calculating angles (horizontal and vertical) associated with camera orientation. The vertical angle 
#         is complemented due to spherical coordinate convention.-------------------------------------------

    dir1 = np.array(CamDir) - np.array(CamLoc)
    dir2 = dir1/(np.sqrt(dir1[0]**2 + dir1[1]**2 + dir1[2]**2))
    horiz = np.arccos(dir2[0])
    vert = np.arccos(dir2[2])
    
#--------The camera has 320 X 240 pixels. To speed up computation, this has been reduced proportionally to 80 X 60.
#        The horizontal (vert) field of view is divided equally among the 80 (60) horizontal (vert) pixels.
    
    theta_h = np.linspace(horiz-np.pi/15, horiz+np.pi/15, 80)
    theta_v = np.linspace(vert-np.pi/20, vert+np.pi/20, 60)
    
#-------factor_x, factor_y, factor_z are used later for concentration-pathlength (CPL) calculations. This is because 
#       extrapolation to calculate CPL happens in pixel-coordinates rather than real-life coordinates. The value 500 
#       is used as a proxy for a large distance. Beyond 500 m, the IR camera doesn't see anything. 
    
    Xstep, Ystep, Zstep  = X[1]-X[0], Y[1]-Y[0], Z[1]-Z[0]
    factor_x, factor_y, factor_z = int(500/Xstep), int(500/Ystep), int(100/Zstep)
    
    p, q = len(theta_h), len(theta_v)
    x_end, y_end, z_end = np.zeros((p,q)), np.zeros((p,q)), np.zeros((p,q))

#-------Here, we calculate the real-life coordinate of a far-away point (say, 500 m away) for each pixel orientation.
#       This is used to calculate CPL. If 500 m goes outside the boundary of 3D considered, concentration is 0.
    
    for i in range(0, p):
        for j in range(0, q):
            x_end[i,j] = factor_x*np.cos(theta_h[i])*np.sin(theta_v[j])
            y_end[i,j] = factor_y*np.sin(theta_h[i])*np.sin(theta_v[j])
            z_end[i,j] = factor_z*np.cos(theta_v[j])
            
#-------Because calculations happen in pixel coordinates, the location of the camera (start of calculation) and the
#       location of far-away point (end of calculation) is converted to pixel coordinates.
    
    x_start, y_start, z_start = (CamLoc[0]-np.min(X))/Xstep, (CamLoc[1]-np.min(Y))/Ystep, (CamLoc[2]-np.min(Z))/Zstep
    
    #x_start, y_start, z_start = CamLoc[0]/Xstep + shiftx, CamLoc[1]/Ystep + shifty, CamLoc[2]/Zstep + shiftz
    x_end, y_end, z_end = x_end + x_start, y_end + y_start, z_end + z_start
    
#------Used to calculate camera properties including noise-equivalent power (nep), temperature-emissivity contrast 
#      (tec) and absorption coefficient (Kav). Temperature is assumed to be 300 K, with an emissivity of 0.5.
    camprop = cp.pixelprop(300, 300)
    nep, tec, Kav = camprop[0], camprop[1], camprop[2]

    IntConc,  CPL = np.zeros((p,q)), np.zeros((p,q))
    
#------This is where concentration pathlength (CPL) is calculated using properties of images.
    for i in range(0, len(theta_h)):
        for j in range(0, len(theta_v)):
            IntConc[i,j] = cp.Pathlength(x_start, y_start, z_start, x_end[i,j], y_end[i,j], z_end[i,j], ppm)
            CPL[i,j] = IntConc[i,j]*500

#-------This section converts CPL to image contrast and compares it to nep. 
    attn = CPL * Kav * NA * 1e-4  #1e-4 is conversion factor
    temp = 1 - 10**(-attn)
    contrast = temp * np.abs(tec) * tau_air
    
    pixels = 0
    for i in range(0, len(theta_h)):
        for j in range(0, len(theta_v)):
            if contrast[i,j] >= nep:
                pixels = pixels + 1
    
    pixel_final = 16 * pixels #Camera pixels were initially truncated to 80 x 60 px, which is re-converted.
    
    detect = 0
    if pixel_final >= 400:
        detect = 1
        
    return detect
                
    

    
            
        