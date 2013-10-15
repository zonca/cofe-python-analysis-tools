from datetime import datetime, timedelta
import numpy as np
from pointingtools import compute_parallactic_angle, altaz2ha 
import cPickle
import sys

import h5py
import pandas as pd
import ephem
import logging as l

def compute_pointing(filename, channel="ch2"):

    with open(filename) as f:
        rawdata = cPickle.load(f)

    # UCSB
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

    l.info("Start time: %s", str(start_date))

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

    h5data=pd.DataFrame({"THETA" : np.pi/2 - dec })
    h5data["PHI"] = ra
    h5data["TEMP"] = rawdata["sci_data"][channel]["T"]
    h5data["Q"] = rawdata["sci_data"][channel]["Q"]
    h5data["U"] = rawdata["sci_data"][channel]["U"]
    h5data["PSI"] = psi
    h5data["FLAG"] = 0
    return h5data

def write_h5data(h5data, filename):
    with h5py.File(filename.replace("pkl","h5"), mode="w") as f:
        f.create_dataset("data", data=h5data.to_records(index=False))

if __name__ == "__main__":
    filename = sys.argv[1]
    h5data = compute_pointing(filename)
    write_h5data(h5data, filename)
