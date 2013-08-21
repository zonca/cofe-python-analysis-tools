#   script to produce flags
#   8 flag bits per channel:
#   0   calibration 
#   1   sun xing
#   2   Moon Xing
#   3   Geosynch Satellite
#   4
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

chan_az_cuts_10=[40,40,40,40,40,40]
chan_el_10=[50,50,50,50,50]

chan_el_names=['el1','el1','el3','el3','el5','el5']
chan_az_names=['az1','az1','az3','az3','az5','az5','az9','az9','az11','az11','az13','az13']
chan_el_names=['el1','el1','el3','el3','el5','el5','el9','el9','el11','el11','el13','el13']

chan_az_cuts_15=[0,0,0,0,0,0,0,0,0,0,25,25]

flags10file='v11_flags10ghz.fits'
flags15file='v11_flags15ghz.fits'

#start with 10 GHz
# open up the data and pointing files
d10=pyfits.open('c:/cofe/flight_data/Level1/1.1/all_10GHz_data.fits')
p10=pyfits.open('c:/cofe/flight_data/Level1/1.1/v11_all_10ghz_pointing.fits')
ut10=d10['TIME'].data['UT']
ndata =len(ut10)

s10=pyfits.open('c:/cofe/flight_data/Level1/1.1/all_10GHz_servo.fits')
lat=s10['gyro_hid'].data['hybridlatitude']
lon=s10['gyro_hid'].data['hybridlongitude']
s10.close()

fazel10=open('c:/cofe/flight_data/Level1/1.1/sunazel10ghz.pkl','rb')
sunazel10ghz=cPickle.load(fazel10)
fazel10.close()
azsun=sunazel10ghz[0]
elsun=sunazel10ghz[1]
fazel10=open('c:/cofe/flight_data/Level1/1.1/moonazel10ghz.pkl','rb')
moonazel10ghz=cPickle.load(fazel10)
fazel10.close()
azmoon=moonazel10ghz[0]
elmoon=moonazel10ghz[1]
suncut=15.
mooncut=5.


#lat=np.zeros(ndata,dtype=np.float32)+0.596
#lon=np.zeros(ndata,dtype=np.float32)-1.8179
#azsun,elsun=util.get_cofe_target(ut10,lat,lon,'Sun')
#azmoon,elmoon=util.get_cofe_target(ut10,lat,lon,'Moon')
#azsun=azsun*180./np.pi
#elsun=elsun*180./np.pi
#azmoon=azmoon*180./np.pi
#elmoon=elmoon*180./np.pi

flags=np.zeros(ndata,dtype=np.uint8)
#first time, make the fits files and fill with empty flags
cols=[]
cols.append(pyfits.Column(name='UT',format='Float32',array=ut10))
coldefinitions=pyfits.ColDefs(cols)
tablehdu=pyfits.new_table(coldefinitions)
tablehdu.name='TIME'
tablehdu.writeto(flags10file,clobber=True)

cols=[]
cols.append(pyfits.Column(name='FLAGS',format='B',array=flags))
coldefinitions=pyfits.ColDefs(cols)
f10=pyfits.open(flags10file,mode='update')
for chan in chans10:
    tablehdu=pyfits.new_table(coldefinitions)
    tablehdu.name=chan
    f10.append(tablehdu)
f10.flush()
    
# retrieve the start and stop times of the calibrations
calstops=util.find_command_uts('0051')
calstarts=util.find_command_uts('0050')
cals=['cal1','cal2','cal3','cal4','cal5','cal6']

f10=pyfits.open(flags10file,mode='update')
for ichan,chan in enumerate(chans10):
    flags=f10[chan].data['FLAGS']
    azname=chan_az_names[ichan]
    elname=chan_el_names[ichan]
    #take care of calibration sections first
    for i,cal in enumerate(cals):
        uttime=calstarts[i]
        calutstart=uttime[1]+uttime[2]/60. + uttime[3]/3600.
        uttime=calstops[i]
        calutstop=uttime[1]+uttime[2]/60. + uttime[3]/3600.
        if cal == 'cal6':
            calutstart=calutstart+24
            calutstop=calutstop+24
        badd=np.where((ut10 > (calutstart-1./60.)) & (ut10 < (calutstop+1./60.)))
        flags[badd]=util.raise_bit(flags[badd],bit=0)
    #now do the azimuth cut for relevant channels (satellite interference)
    azcut=chan_az_cuts_10[ichan]
    if (azcut != 0):
        azbad=np.where(np.abs(p10[1].data[azname] - 190.)<azcut)
        flags[azbad]=util.raise_bit(flags[azbad],bit=3)
    # now sun cut.
    sunbad=np.where((np.abs(p10[1].data[azname]-azsun) < suncut) & (np.abs(p10[1].data[elname]-elsun) < suncut))
    flags[sunbad]=util.raise_bit(flags[sunbad],bit=1)
    moonbad=np.where((np.abs(p10[1].data[azname]-azmoon) < mooncut) & (np.abs(p10[1].data[elname]-elmoon) < mooncut))
    flags[moonbad]=util.raise_bit(flags[moonbad],bit=2)
    f10.flush()
        
f10.flush()
d10.close()
p10.close()
# now do 15 GHz
# open up the data and pointing files
d15=pyfits.open('c:/cofe/flight_data/Level1/1.1/all_15GHz_data.fits')
p15=pyfits.open('c:/cofe/flight_data/Level1/1.1/v11_all_15ghz_pointing.fits')
ut15=d15['TIME'].data['UT']
ndata=len(ut15)

fazel15=open('c:/cofe/flight_data/Level1/1.1/sunazel15ghz.pkl','rb')
sunazel15ghz=cPickle.load(fazel15)
fazel15.close()
azsun=sunazel15ghz[0]
elsun=sunazel15ghz[1]
fazel15=open('c:/cofe/flight_data/Level1/1.1/moonazel15ghz.pkl','rb')
moonazel15ghz=cPickle.load(fazel15)
fazel15.close()
azmoon=moonazel15ghz[0]
elmoon=moonazel15ghz[1]
suncut=15.
mooncut=10.


flags=np.zeros(ndata,dtype=np.uint8)
#first time, make the fits files and fill with empty flags
cols=[]
cols.append(pyfits.Column(name='UT',format='Float32',array=ut15))
coldefinitions=pyfits.ColDefs(cols)
tablehdu=pyfits.new_table(coldefinitions)
tablehdu.name='TIME'
tablehdu.writeto(flags15file,clobber=True)

cols=[]
cols.append(pyfits.Column(name='FLAGS',format='B',array=flags))
coldefinitions=pyfits.ColDefs(cols)
f15=pyfits.open(flags15file,mode='update')
for chan in chans15:
    tablehdu=pyfits.new_table(coldefinitions)
    tablehdu.name=chan
    f15.append(tablehdu)
f15.flush()
    
f15=pyfits.open(flags15file,mode='update')
for ichan,chan in enumerate(chans15):
    flags=f15[chan].data['FLAGS']
    azname=chan_az_names[ichan]
    elname=chan_el_names[ichan]
    #take care of calibration sections first
    for i,cal in enumerate(cals):
        uttime=calstarts[i]
        calutstart=uttime[1]+uttime[2]/60. + uttime[3]/3600.
        uttime=calstops[i]
        calutstop=uttime[1]+uttime[2]/60. + uttime[3]/3600.
        if cal == 'cal6':
            calutstart=calutstart+24
            calutstop=calutstop+24
        badd=np.where((ut15 > (calutstart-1./60.)) & (ut15 < (calutstop+1./60.)))
        flags[badd]=util.raise_bit(flags[badd],bit=0)
    #now do the azimuth cut for relevant channels (satellite interference)
    azcut=chan_az_cuts_15[ichan]
    if (azcut != 0):
        azbad=np.where(np.abs(p15[1].data[azname] - 190.)<azcut)
        flags[azbad]=util.raise_bit(flags[azbad],bit=3)
    # now sun cut.
    sunbad=np.where((np.abs(p15[1].data[azname]-azsun) < suncut) & (np.abs(p15[1].data[elname]-elsun) < suncut))
    flags[sunbad]=util.raise_bit(flags[sunbad],bit=1)
    moonbad=np.where((np.abs(p15[1].data[azname]-azmoon) < mooncut) & (np.abs(p15[1].data[elname]-elmoon) < mooncut))
    flags[moonbad]=util.raise_bit(flags[moonbad],bit=2)
    f15.flush()
    
f15.flush()
d15.close()
p15.close()
