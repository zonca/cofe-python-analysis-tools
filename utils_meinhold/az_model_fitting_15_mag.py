#script to find sun1,2 and moon crossings, fit 'drift' to longitude
#this code takes develco az value as input rather than gyro.
import pyfits
import cofe_util as util
import toitools as toi
import cPickle
import numpy as np
import matplotlib.pyplot as plt
#working directories: current level, old (for servofile), main data dir (for UT of crossings)
wd='/cofe/flight_data/Level1/1.2/'
wds='/cofe/flight_data/Level1/1.1/'
wdmain='/cofe/flight_data/Level1/'
d15=pyfits.open(wd+'all_15GHz_data.fits')
s15=pyfits.open(wds+'all_15GHz_servo.fits')
a15=pyfits.open(wd+'magaz15.fits')
ut=d15['TIME'].data['UT']
lon=s15[5].data['HYBRIDLONGITUDE']
mlon=np.mean(lon[abs(lon+1.8)<.3])
lon[abs(lon+1.8) >=.3]=mlon
uts15=s15['time'].data['ut']
lon=s15[5].data['HYBRIDLONGITUDE']
lat=s15[5].data['HYBRIDLATITUDE']
gaz=a15['15ghz'].data['az']

utcf=open(wd+'utcrossinputs15.pkl','rb')
utcrossings=cPickle.load(utcf)
utcf.close()
print utcrossings
azoffdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3), 9:np.zeros(3), 11:np.zeros(3), 13:np.zeros(3) }
eltargetdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3), 9:np.zeros(3), 11:np.zeros(3), 13:np.zeros(3) }
aztargetdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3), 9:np.zeros(3), 11:np.zeros(3), 13:np.zeros(3) }
utcrossdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3), 9:np.zeros(3), 11:np.zeros(3), 13:np.zeros(3) }
loncrossdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3), 9:np.zeros(3), 11:np.zeros(3), 13:np.zeros(3) }

targs=['Sun','Sun','Moon']    
    
chans=[1,3,5,9,11,13]

for c,ch in enumerate(chans):
    for crossn, targ in enumerate(targs):
        print c,ch,crossn,targ,'now the lengths'
        azoffdic[ch][crossn],aztargetdic[ch][crossn],eltargetdic[ch][crossn],utcrossdic[ch][crossn]=util.get_cofe_crossing(ut,d15[ch+2].data['T'],gaz,lat,lon,utcrossings[ch][crossn],targ)

#fitdic = { 'offset':np.zeros(5), 'slope':np.zeros(5)  }
fitdic={}
for ch in chans:
    for i,target in enumerate(targs):
        loncrossdic[ch][i]=lon[abs(uts15-utcrossdic[ch][i])==min(abs(uts15-utcrossdic[ch][i]))]

for ch in chans:
    fitdic[ch]=util.linfit(loncrossdic[ch],azoffdic[ch])
    
f=open(wd+'azoff_15_mag.pkl','wb')
cPickle.dump(azoffdic,f)
f.close()
f=open(wd+'eltarget_15_mag.pkl','wb')
cPickle.dump(eltargetdic,f)
f.close()
f=open(wd+'aztarget_15_mag.pkl','wb')
cPickle.dump(aztargetdic,f)
f.close()
f=open(wd+'utcrossings_15_mag.pkl','wb')
cPickle.dump(utcrossdic,f)
f.close()

f=open(wd+'fitparams_15_mag.pkl','wb')
cPickle.dump(fitdic,f)
f.close()

plt.figure()
clr=['b','g','r','c','m','y']

for c,ch in enumerate(chans):
    plt.plot( loncrossdic[ch],azoffdic[ch],'+',label=str(ch),color=clr[c])
    plt.plot(lon,fitdic[ch][0]+fitdic[ch][1]*lon,color=clr[c])

plt.xlabel('UT hours')
plt.ylabel('Azimuth offset (from gyro), degrees')
plt.title('Sun1, Sun2, Moon crossing fits to v 1.0 pointing: 15 GHz')
plt.legend()
plt.show()
plt.savefig(wd+'azfit_v11_15ghz_mag.png')

