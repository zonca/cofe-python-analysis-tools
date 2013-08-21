import cofe_util as util
import cPickle
import numpy as np

facgains=open('acgain15.pkl','rb')
acgains15=cPickle.load(facgains)
facgains.close()

facgains=open('acgain10.pkl','rb')
acgains10=cPickle.load(facgains)
facgains.close()

fcaluts=open('calutdic.pkl','rb')
calutdic=cPickle.load(fcaluts)
fcaluts.close()

floss=open('loss15.pkl','rb')
loss15=cPickle.load(floss)
floss.close()

floss=open('loss10.pkl','rb')
loss10=cPickle.load(floss)
floss.close()

cals=['cal1','cal2','cal3','cal4','cal5']
chans15ghz=['ch1','ch3','ch5','ch9','ch11','ch13']
acchans15ghz=['ch0','ch2','ch4','ch8','ch10','ch12']
chans10ghz=['ch1','ch3','ch5']
acchans10ghz=['ch0','ch2','ch4']

fcal10ghz=open('cal10ghz_b.pkl','rb')
cal10ghz=cPickle.load(fcal10ghz)
fcal10ghz.close()

fcal15ghz=open('cal15ghz_b.pkl','rb')
cal15ghz=cPickle.load(fcal15ghz)
fcal15ghz.close()

ftcal10dic=open('ftcal10dic.pkl','rb')
tcal10dic=cPickle.load(ftcal10dic)
ftcal10dic.close()

ftcal15dic=open('ftcal15dic.pkl','rb')
tcal15dic=cPickle.load(ftcal15dic)
ftcal15dic.close()

for cal in cals:
    cal10ghz[cal]['ut']=calutdic[cal]
    cal10ghz[cal]['tcal']=tcal10dic[cal]
    cal10ghz[cal]['k_per_v']={}
    for chan,acchan in zip(chans10ghz,acchans10ghz):
        delta_v=(np.mean(cal10ghz[cal]['on'][chan])-np.mean(cal10ghz[cal]['off1'][chan]))*(20./2.**16)
        delta_t=loss10[chan]*(cal10ghz[cal]['tcal']+273)
        cal10ghz[cal]['k_per_v'][chan]=delta_t/delta_v
        cal10ghz[cal]['k_per_v'][acchan]=delta_t/(delta_v*acgains10[acchan])
fcal10ghz_c=open('cal10ghz_c.pkl','wb')
cPickle.dump(cal10ghz,fcal10ghz_c)
fcal10ghz_c.close()


for cal in cals:
    cal15ghz[cal]['ut']=calutdic[cal]
    cal15ghz[cal]['tcal']=tcal15dic[cal]
    cal15ghz[cal]['k_per_v']={}
    for chan,acchan in zip(chans15ghz,acchans15ghz):
        delta_v=(np.mean(cal15ghz[cal]['on'][chan])-np.mean(cal15ghz[cal]['off1'][chan]))*(20./2.**16)
        delta_t=loss15[chan]*(cal15ghz[cal]['tcal']+273)
        cal15ghz[cal]['k_per_v'][chan]=delta_t/delta_v
        cal15ghz[cal]['k_per_v'][acchan]=delta_t/(delta_v*acgains15[acchan])
fcal15ghz_c=open('cal15ghz_c.pkl','wb')
cPickle.dump(cal15ghz,fcal15ghz_c)
fcal15ghz_c.close()


        

