#   script to apply simplest calibration (just lin interpolate from measured cals in pkl files
#   March 1, 2012

import cofe_util as util
import pyfits
import numpy as np
from matplotlib import pyplot as plt
import cPickle
wd='/cofe/flight_data/Level1/1.2/'
wdmain='/cofe/flight_data/'
chans10=['ch0','ch1','ch2','ch3','ch4','ch5']
chans15=['ch0','ch1','ch2','ch3','ch4','ch5','ch8','ch9','ch10','ch11','ch12','ch13']

#start with 10 GHz
# open up the data and calibration files
d10=pyfits.open(wd+'all_10GHz_data_cal.fits',mode='update')
fc10=open(wdmain+'cal10ghz_c.pkl')
cal10=cPickle.load(fc10)
ut10=d10['TIME'].data['UT']
clist=cal10.keys()

caluts=np.array([cal10[cal]['ut'] for cal in clist[:5]])
caluts[4]=caluts[4]+24

for chan in chans10:
    chanlabel=chan+'_'
    cals=np.array([cal10[cal]['k_per_v'][chan] for cal in clist[:5]])
    cal10_interp=np.interp(ut10,caluts,cals)                            #interpolate to all UTs
    d10[chanlabel].data['t'][:]=d10[chanlabel].data['t']*cal10_interp
    d10[chanlabel].data['q'][:]=d10[chanlabel].data['q']*cal10_interp
    d10[chanlabel].data['u'][:]=d10[chanlabel].data['u']*cal10_interp
d10.flush()
d10.close()

# now 15 GHz
# open up the data and calibration files
d15=pyfits.open(wd+'all_15GHz_data_cal.fits',mode='update')
fc15=open(wdmain+'cal15ghz_c.pkl')
cal15=cPickle.load(fc15)
ut15=d15['TIME'].data['UT']
clist=cal15.keys()

caluts=np.array([cal15[cal]['ut'] for cal in clist[:5]])
caluts[4]=caluts[4]+24

for chan in chans15:
    chanlabel=chan+'_'
    cals=np.array([cal15[cal]['k_per_v'][chan] for cal in clist[:5]])
    cal15_interp=np.interp(ut15,caluts,cals)                            #interpolate to all UTs
    d15[chanlabel].data['t'][:]=d15[chanlabel].data['t']*cal15_interp
    d15[chanlabel].data['q'][:]=d15[chanlabel].data['q']*cal15_interp
    d15[chanlabel].data['u'][:]=d15[chanlabel].data['u']*cal15_interp
d15.flush()
d15.close()
