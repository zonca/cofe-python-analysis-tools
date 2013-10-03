from datetime import datetime, timedelta
import healpy as hp
import numpy as np
from pointingtools import compute_parallactic_angle, altaz2ha 
import cPickle
import sys

import ephem

filename = sys.argv[1]

if not locals().has_key("rawdata"): # in case we are rerunning with run -i
    with open(filename) as f:
        rawdata = cPickle.load(f)

NSIDE = 256
NPIX = hp.nside2npix(NSIDE)

lat = np.radians(34.41)
lon = np.radians(-119.85)
alt = 0

observer = ephem.Observer()
observer.lon = lon
observer.lat = lat
observer.elevation = alt

def conv(azimuth, elevation, utc):
    observer.date = utc
    return observer.radec_of(azimuth, elevation)

start_date = datetime(rawdata["sci_data"]["year"][0], rawdata["sci_data"]["month"][0], rawdata["sci_data"]["day"][0]) + timedelta(hours=rawdata["sci_data"]["ut"][0])
start = ephem.julian_date(start_date)

print "Start time: ", start_date
print "Start time [JD]: ", start

full_time_jd = start + (rawdata["sci_data"]["ut"] - rawdata["sci_data"]["ut"][0]) / 24.

az = np.radians(rawdata["az"])
el = np.radians(rawdata["el"])

ra = []
dec = []
for i in range(0, len(rawdata["sci_data"])):
    ra_i, dec_i = conv(az[i], el[i], start_date+timedelta(hours=rawdata["sci_data"]["localtime"][i]-rawdata["sci_data"]["localtime"][0]))
    ra.append(ra_i)
    dec.append(dec_i)

ra = np.array(ra)
dec = np.array(dec)
ha = altaz2ha(el, az, lat)
psi = compute_parallactic_angle(ha, lat, dec)

pix = hp.ang2pix(NSIDE, np.pi/2-dec, ra, nest=False)

import pandas as pd
h5data=pd.DataFrame({"THETA" : np.pi/2 - dec })
h5data["PHI"] = ra
h5data["TEMP"] = rawdata["sci_data"]["ch2"]["T"]
h5data["Q"] = rawdata["sci_data"]["ch2"]["Q"]
h5data["U"] = rawdata["sci_data"]["ch2"]["U"]
h5data["PSI"] = psi
h5data["FLAG"] = 0
import h5py
with h5py.File(filename.replace("pkl","h5"), mode="w") as f:
    f.create_dataset("data", data=h5data.to_records(index=False))
