#script to find sun1,2 and moon crossings, fit gyro drift
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
d10=pyfits.open(wd+'all_10GHz_data.fits')
s10=pyfits.open(wds+'all_10GHz_servo.fits')
a10=pyfits.open(wd+'fixaz.fits')
ut=d10['TIME'].data['UT']
lon=s10[5].data['HYBRIDLONGITUDE']
lat=s10[5].data['HYBRIDLATITUDE']
gaz=a10['10ghz'].data['az']

utcf=open(wd+'utcrossinputs10.pkl','rb')
utcrossings=cPickle.load(utcf)
utcf.close()
print utcrossings
azoffdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3) }
eltargetdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3)}
aztargetdic = {1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3) }
utcrossdic = { 1:np.zeros(3), 3:np.zeros(3), 5:np.zeros(3) }
    
targs=['Sun','Sun','Moon']    
    
chans=[1,3,5]

for c,ch in enumerate(chans):
    for crossn, targ in enumerate(targs):
        print c,ch,crossn,targ,'now the lengths'
        azoffdic[ch][crossn],aztargetdic[ch][crossn],eltargetdic[ch][crossn],utcrossdic[ch][crossn]=util.get_cofe_crossing(ut,d10[ch+2].data['T'],gaz,lat,lon,utcrossings[ch][crossn],targ)

#fitdic = { 'offset':np.zeros(5), 'slope':np.zeros(5)  }
fitdic={}
for ch in chans:
    fitdic[ch]=util.linfit(utcrossdic[ch],azoffdic[ch])
    
f=open(wd+'azoff_10.pkl','wb')
cPickle.dump(azoffdic,f)
f.close()
f=open(wd+'eltarget_10.pkl','wb')
cPickle.dump(eltargetdic,f)
f.close()
f=open(wd+'aztarget_10.pkl','wb')
cPickle.dump(aztargetdic,f)
f.close()
f=open(wd+'utcrossings_10.pkl','wb')
cPickle.dump(utcrossdic,f)
f.close()

f=open(wd+'fitparams_10.pkl','wb')
cPickle.dump(fitdic,f)
f.close()

plt.figure()
clr=['b','g','r','c','m','y']

for c,ch in enumerate(chans):
    plt.plot( utcrossdic[ch],azoffdic[ch],'+',label=str(ch),color=clr[c])
    plt.plot(ut,fitdic[ch][0]+fitdic[ch][1]*ut,color=clr[c])

plt.xlabel('UT hours')
plt.ylabel('Azimuth offset (from gyro), degrees')
plt.title('Sun1, Sun2, Moon crossing fits to v 1.0 pointing: 10 GHz')
plt.legend()
plt.show()
plt.savefig(wd+'azfit_v11_10ghz.png')

