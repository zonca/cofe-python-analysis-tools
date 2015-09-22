import datetime
import healpy as hp
from collections import OrderedDict
import numpy as np
from scipy import constants
from pointingtools import compute_parallactic_angle, altaz2ha

from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, Angle, ICRS
from astropy.time import Time, TimeDelta

NSIDE = 128
HOURS = 24*365
SAMPLING = 600 #1/30. # 1 sec
ELEVATION = Angle(90, unit=u.deg)
LOCATION = "Tibet"

# Barcroft
locations = dict(
        Barcroft = EarthLocation( lat=Angle(34.41, 'deg'),
                                  lon=Angle(-119.85, 'deg'),
                                  height=3800 * u.m),
        Greenland = EarthLocation( lat=Angle(72.5796, 'deg'),
                                  lon=Angle(-38.4592, 'deg'),
                                  height=3200 * u.m),
        Tibet     = EarthLocation( lat=Angle(32.3166667, 'deg'),
                                  lon=Angle(80.0166666667, 'deg'),
                                  height=5100 * u.m),
)

location = locations[LOCATION]

start_time = Time(datetime.datetime(2015, 8, 1), scale='ut1')
sampling_interval = TimeDelta(SAMPLING, format="sec")
time = start_time + sampling_interval * np.arange(0., HOURS*3600/SAMPLING)

# zenith
altaz = AltAz(az=Angle(0., unit=u.degree), alt=ELEVATION, obstime=time, location=location)
radec = altaz.transform_to(ICRS)
ra_zenith = radec.ra.radian
dec_zenith = radec.dec.radian

# local north
altaz = AltAz(az=Angle(0., unit=u.degree), alt=Angle(0., unit=u.degree), obstime=time, location=location)
radec = altaz.transform_to(ICRS)
ra_north = radec.ra.radian
dec_north = radec.dec.radian

import pandas as pd

pd.DataFrame({"ra_zenith_rad":ra_zenith, "dec_zenith_rad":dec_zenith, 
    "ra_north_rad":ra_north, "dec_north_rad":dec_north}, index=time.datetime).to_hdf("zenith_pointing_" + LOCATION.lower() + ".h5", "data")
