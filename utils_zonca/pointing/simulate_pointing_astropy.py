import datetime
import healpy as hp
from collections import OrderedDict
import numpy as np
from scipy import constants
from pointingtools import compute_parallactic_angle, altaz2ha

import ephem

from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, Angle, ICRS
from astropy.time import Time, TimeDelta

NSIDE = 128
HOURS = 24
SAMPLING = 1/30. # 1 sec
ELEVATION = Angle(50, unit=u.deg)
LOCATION = "Greenland"

# Barcroft
locations = dict(
        Barcroft = EarthLocation( lat=Angle(34.41, 'deg'),
                                  lon=Angle(-119.85, 'deg'),
                                  height=3800 * u.m),
        Greenland = EarthLocation( lat=Angle(72.5796, 'deg'),
                                  lon=Angle(-38.4592, 'deg'),
                                  height=3200 * u.m),
)

location = locations[LOCATION]

start_time = Time(datetime.datetime(2015, 8, 1), scale='ut1')
sampling_interval = TimeDelta(SAMPLING, format="sec")
time = start_time + sampling_interval * np.arange(0., HOURS*3600/SAMPLING)
#time = start_time

rotation_speed = (-1 * 360/60)
ut = np.arange(0., HOURS, SAMPLING/3600)
az = rotation_speed * (ut * 3600.) % 360

altaz = AltAz(az=Angle(az, unit=u.degree), alt=ELEVATION, obstime=time, location=location)

radec = altaz.transform_to(ICRS)
ra = radec.ra.radian
dec = radec.dec.radian

#ha = altaz2ha(el, az, lat)
#psi = compute_parallactic_angle(ha, lat, dec)

pix = hp.ang2pix(NSIDE, np.pi/2-dec, ra, nest=False)

from mapmaking import pix2map
import matplotlib.pyplot as plt
hit = hp.ma(pix2map(pix, NSIDE))
hit.mask = hit == 0
hp.mollview(np.log10(hit).filled(),min=0,max=3,unit='log10 hits',title='Hitmap {hours}hrs'.format(hours=HOURS))
plt.show()

import pandas as pd

pd.DataFrame({"ra_rad":ra, "dec_rad":dec}, index=time.datetime).to_hdf("pointing_24h_" + LOCATION.lower() + ".h5", "data")
