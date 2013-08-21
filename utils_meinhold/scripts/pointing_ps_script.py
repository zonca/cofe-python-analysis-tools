


import pyfits
import cPickle
import cofe_util as util
get_ipython().magic(u"cd /cofe/flight_data/Level1/1.2")
get_ipython().magic(u"autocall 2")
c10=pyfits.open('all_10GHz_data_cal.fits')
p10=pyfits.open('all_10ghz_pointing.fits')
p10mag=pyfits.open('all_10ghz_pointing_mag.fits')
ut10=c10['Time'].data['ut']
utstartend=[16.8 ,38.4]
c101= c10['ch1_'].data['t'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
az101mag=p10mag[1].data['az1'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
#az101=p10[1].data['az1'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
ps101mag=util.phasebin(3600,az101mag*np.pi/180.-np.pi,c101)
#ps101=util.phasebin(3600,az101*np.pi/180.-np.pi,c101)
#need to remove zeros:
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0]-1,ps101magbad[1]]
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0]-1,ps101magbad[1]]
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
ps=copy(ps101mag)
#now set up to get cross correlations one row at at time
nrows=ps.shape[1]-1
lags=[]
for i in range(nrows):
    cc=xcorr(ps[1700:1900,0],ps[1700:1900,i],maxlags=20)
    lag=cc[0][cc[1]==np.max(cc[1])][0]
    lags.append(lag)
    ps[:,:i]=np.roll(ps[:,:i],-lag,axis=0)

psmag_flat=copy(ps)
    
#Getting satellite angles:
f=open('ut_lags_from_mag_10ghz_sataz.pkl','rb')
ut_lags_satoff=cPickle.load(f)
f.close()
wds='/cofe/flight_data/Level1/1.1/'
s10=pyfits.open(wds+'all_10GHz_servo.fits')
lon=s10[5].data['HYBRIDLONGITUDE']
lat=s10[5].data['HYBRIDLATITUDE']
sut=s10['time'].data['ut']
g=where(abs(lon+1.8)<.15)
utlist=ut_lags_satoff[:,0]
lonlist=interp(utlist,sut[g],lon[g])
latlist=interp(utlist,sut[g],lat[g])
lonlistd=-lonlist*180./np.pi
latlistd=latlist*180./np.pi
raw_offset=178.5  #this seems to be where satellite of long 101 shows up in corrected pseudomap
from satazel import *
sat101az=zeros(743)
sat101el=zeros(743)
for i in range(743):
    sat101az[i],sat101el[i]=GetSatAzEl(lonlistd[i],latlistd[i],101)
for rev in range(743):
    psoff101[:,rev]=roll(psoff101[:,rev],np.int(10.*(sat101az[rev]-raw_offset)))

az101=p10[1].data['az1'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
ps101=util.phasebin(3600,az101*np.pi/180.-np.pi,c101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0],ps101bad[1]-1]
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0],ps101bad[1]-1]
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0],ps101bad[1]-1]
ps=copy(ps101)
nrows=ps.shape[1]-1
lags=[]
for i in range(nrows):
    cc=xcorr(ps[1700:1900,0],ps[1700:1900,i],maxlags=20)
    lag=cc[0][cc[1]==np.max(cc[1])][0]
    lags.append(lag)
    ps[:,:i]=np.roll(ps[:,:i],-lag,axis=0)
    
psgyro_flat=copy(ps)

    