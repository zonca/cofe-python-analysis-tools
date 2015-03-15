
# coding: utf-8

# In[1]:

import pandas as pd


# With `simulate_zenith_pointing.py` I created the pointing of the local zenith and of the local north for 1 year for Greenland with a sampling of 6 minutes

# In[2]:



# In[3]:



# Therefore I know the location in Equatorial coordinates of the axis of the telescope and of the direction of view of the telescope, for simplicity I can assume the telescope starts from pointing at North.

# In[4]:

import quaternionarray as qa
from mapmaking import pix2map


# In[5]:

import healpy as hp
import numpy as np
NSIDE = 128

for LOCATION in ["Greenland", "Barcroft"]:

    for OPENING_ANGLE in [20, 40, 60]:
        hit = hp.ma(np.zeros(hp.nside2npix(NSIDE)))
        for day in range(1, 31):

            # In[6]:
            print(day)

            pointing = pd.read_hdf("zenith_pointing_%s.h5" % LOCATION.lower(), "data")["2015-08-%02d" % day]

            # I can define `z` as the axis of the telescope, `x` as defining the plane of the direction of view and `y` as the vector of polarization sensitivity for a fixed altitiude mount.

            # In[7]:

            vec = hp.dir2vec(
                             np.degrees(pointing.ra_zenith_rad), 
                             np.degrees(pointing.dec_zenith_rad), lonlat=True).T


            # In[8]:

            vec_north = hp.dir2vec(
                             np.degrees(pointing.ra_north_rad), 
                             np.degrees(pointing.dec_north_rad), lonlat=True).T


            # In[9]:

            x = np.array([1,0,0])
            y = np.array([0,1,0])
            z = np.array([0,0,1])


            # In[10]:

            #rotmat = np.hstack([ vec_north[:,0][:,np.newaxis], np.cross(vec[:,0], vec_north[:,0])[:,np.newaxis], vec[:,0][:,np.newaxis]])


            # In[11]:

            vec_north.T[:,0][:,np.newaxis]


            # Need to prepend a column of zeros to `vec`, because I need to have an input with a dimension equal to 4 to declare the signature

            # In[12]:

            lon, lat= hp.vec2dir(vec[:,0], vec[:,1], vec[:,2], lonlat=True)


            # In[13]:

            q = np.empty([len(vec), 4], dtype=np.float)


            # In[14]:

            n = len(vec)
            for i in range(n):
                rotmat = np.hstack([ vec_north[i,:][:,np.newaxis],
                                     np.cross(vec[i,:], vec_north[i,:])[:,np.newaxis],
                                     vec[i,:][:,np.newaxis]
                                ])
                q[i] = qa.norm(qa.from_rotmat(rotmat))
                if (i > 0):
                    if np.dot(q[i], q[i-1]) < 0:
                        q[i] *= -1


            # `rotmat` / `q` are the rotation matrix / quaternion between the local system and Equatorial coordinates

            # ### Interpolation

            # In[18]:

            jd = pointing.index.to_julian_date()


            # In[19]:

            ut_h = (jd - jd[0])*24


            # In[20]:

            target_ut_h = np.arange(0, ut_h[-1], 1/30/3600)


            qfull = qa.nlerp(target_ut_h, ut_h, q)


            # In[ ]:

            #qfull = q


            # In[ ]:

            #target_ut_h = ut_h.values


            # ### Elevation and spinning

            # Elevation is a rotation with respect to the `y` axis of the opening angle

            # In[ ]:



            # In[ ]:

            q_elev = qa.rotation(y, np.radians(OPENING_ANGLE))


            # Rotation is a rotation with respect to the `z` axis

            # In[ ]:

            rotation_speed = np.radians(-1 * 360/60)
            az = rotation_speed * (target_ut_h * 3600.) % (2*np.pi)


            q_rotation = qa.rotation(z, az)


            # We compose the rotations

            direction = qa.rotate(
                qa.mult(qfull, qa.mult(q_rotation, q_elev)),
                        z)


            lon, lat= hp.vec2dir(direction[:,0], direction[:,1], direction[:,2], lonlat=True)


            # ### Hitmap

            pix = hp.vec2pix(NSIDE,direction[:,0], direction[:,1], direction[:,2] )

            hit += hp.ma(pix2map(pix, NSIDE))

        hit.mask = hit == 0
        hp.write_map('hitmap_%s_%d_opening.fits' % (LOCATION, OPENING_ANGLE),hit)
