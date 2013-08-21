#   script to add new flags
#   8 flag bits per channel:
#   0   calibration 
#   1   sun xing
#   2   Moon Xing
#   3   Geosynch Satellite
#   4   By hand bad ut list
#   5
#   6
#   7

import cofe_util as util
import pyfits
import numpy as np
from matplotlib import pyplot as plt
import cPickle

chans10=['ch0','ch1','ch2','ch3','ch4','ch5']
chans15=['ch0','ch1','ch2','ch3','ch4','ch5','ch8','ch9','ch10','ch11','ch12','ch13']

flags10file='v11_flags10ghz.fits'
flags15file='v11_flags15ghz.fits'

# retrieve the start and stop times of the new bad data
baddatalistfile='c:/cofe/flight_data/baduts_for_flags_based_on_10Ghz_ch0.pkl'
baddata=open(baddatalistfile,'rb')
badstarts,badstops=cPickle.load(baddata)
baddata.close()

f10=pyfits.open(flags10file,mode='update')
ut10=f10['time'].data['ut']

for ichan,chan in enumerate(chans10):
    flags=f10[chan].data['FLAGS']
    for badutstart,badutstop in zip(badstarts,badstops):
        badd=np.where((ut10 > badutstart) & (ut10 < badutstop))
        flags[badd]=util.raise_bit(flags[badd],bit=4)
    f10.flush()
        
f10.flush()
f10.close()

f15=pyfits.open(flags15file,mode='update')
ut15=f15['time'].data['ut']
for ichan,chan in enumerate(chans15):
    flags=f15[chan].data['FLAGS']
    for badutstart,badutstop in zip(badstarts,badstops):
        badd=np.where((ut15 > badutstart) & (ut15 < badutstop))
        flags[badd]=util.raise_bit(flags[badd],bit=4)
    f15.flush()
        
f15.flush()
f15.close()
