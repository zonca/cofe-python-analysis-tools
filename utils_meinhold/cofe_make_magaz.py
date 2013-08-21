#   script to produce alternative to fixaz, based on Develco magnetemter data in science channels
#   ch 14 and ch15 of each data set are magy and magz
#   azimuth=arctan2(ch15,ch14)

import cofe_util as util
import pyfits
import numpy as np
from matplotlib import pyplot as plt
import cPickle
#working directories: current level, old (for servofile), main data dir (for UT of crossings)
wd='/cofe/flight_data/Level1/1.2/'
wds='/cofe/flight_data/Level1/1.1/'
wdmain='/cofe/flight_data/Level1/'
magazfile10=wd+'magaz10.fits'
magazfile15=wd+'magaz15.fits'

d10=pyfits.open(wd+'all_10GHz_data.fits')
ut10=d10['TIME'].data['UT']
ndata =len(ut10)
#lat=s10['gyro_hid'].data['hybridlatitude']
#lon=s10['gyro_hid'].data['hybridlongitude']
my=d10['ch14_'].data['t']
mz=d10['ch15_'].data['t']
magang10=np.arctan2(mz,my)
#add 180 degrees, makes later fitting work well
magang10=magang10+np.pi
magang10[magang10>np.pi]=magang10[magang10>np.pi]-np.pi*2.0
d10.close()

# make the fits file and fill 
cols=[]
cols.append(pyfits.Column(name='UT',format='Float32',array=ut10))
cols.append(pyfits.Column(name='AZ',format='Float32',array=magang10))
coldefinitions=pyfits.ColDefs(cols)
tablehdu=pyfits.new_table(coldefinitions)
tablehdu.name='10GHz'
tablehdu.writeto(magazfile10,clobber=True)



d15=pyfits.open('c:/cofe/flight_data/Level1/1.1/all_15GHz_data.fits')
ut15=d15['TIME'].data['UT']
ndata =len(ut15)
#lat=s10['gyro_hid'].data['hybridlatitude']
#lon=s10['gyro_hid'].data['hybridlongitude']
my=d15['ch14_'].data['t']
mz=d15['ch15_'].data['t']
magang15=np.arctan2(mz,my)
#add 180 degrees, makes later fitting work well
magang15=magang15+np.pi
magang15[magang15>np.pi]=magang15[magang15>np.pi]-np.pi*2.0

d15.close()

# make the fits file and fill 
# make the fits file and fill 
cols=[]
cols.append(pyfits.Column(name='UT',format='Float32',array=ut15))
cols.append(pyfits.Column(name='AZ',format='Float32',array=magang15))
coldefinitions=pyfits.ColDefs(cols)
tablehdu=pyfits.new_table(coldefinitions)
tablehdu.name='15GHz'
tablehdu.writeto(magazfile15,clobber=True)
