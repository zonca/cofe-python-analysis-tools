import numpy as np

def signum (n):
    "Return the sign value of n as -1, 0 or 1 for negative, zero or positive n"
    if n < 0:
        return -1
    if n == 0:
        return 0
    return 1
# end signum

def GetSatAzEl(olong,olat,slong):
    "function to return az,el of geosynch satellite at longitude slong, when viewed from position olong olat"
    "Inputs in degrees, west is positive longitude"
    rorbit = 6.615   # Radius of geosynchronous orbit in units of earth radius
    dtr=np.pi / 180   # Degree/radian factor
    rtd=1/dtr    
    longdiff=(olong-slong)*dtr # longitude difference in radians
    latdiff= (90 + olat) * dtr # latitude from s. pole in radians
    #' satellite's x,y,z coordinates
    Y = 0       # equatorial orbit
    X = rorbit * np.sin (longdiff)
    Z = rorbit * np.cos (longdiff)
    #' rotate system to put observer at s. pole
    dist = abs(Z)  # distance from x-axis
    angle = signum (Z) * np.pi/2
    # azimuth angle onto y-z plane (y-axis as zero)
    angle += latdiff    # rotate system
    Y = dist * np.cos (angle)   # new y
    Z = dist * np.sin (angle)   # new z    
    if X == 0  and  Z == 0:
        elevation = np.pi/2
    else:
        elevation = np.arctan ((-1-Y) / np.hypot (X, Z)) 
        elevation *= rtd    # convert elevation to degrees
    if Z == 0:
        azimuth = signum (X) * PIby2
    else:
        azimuth = np.arctan (X / Z)
        if Z < 0:
            azimuth += np.pi
    azimuth *= rtd    # bearing in degrees
    azimuth = np.mod (azimuth, 360.0)
    if azimuth < 0:          
        azimuth += 360.0     
    return [azimuth,elevation]