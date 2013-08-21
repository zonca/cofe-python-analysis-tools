#script to read in COFE calibrations, already extracted
#perform fit to find emissivities, and plot results

import matplotlib.pyplot as plt
import numpy as np
import cPickle
import cofe_util as util

chans10ghz=['ch1','ch3','ch5']
chans15ghz=['ch1','ch3','ch5','ch9','ch11','ch13']
cals=['cal1','cal2','cal3','cal4','cal5']
vcal=20./(2.**16)

f10=open('cal10ghz.pkl','rb')
f15=open('cal15ghz.pkl','rb')
cal10ghz=cPickle.load(f10)
cal15ghz=cPickle.load(f15)
f10.close()
f15.close()
f10a=open('cal10ghz_b.pkl','wb')
f15a=open('cal15ghz_b.pkl','wb')
for cal in cals:
    cal10ghz[cal]['loss']={}
    cal10ghz[cal]['loss2']={}
    for chan in chans10ghz:
        fp=util.linfit(cal10ghz[cal]['on'][chan],cal10ghz[cal]['off1'][chan])
        cal10ghz[cal]['loss'][chan]=1.- 1./fp[1]
        fp2=util.linfit(cal10ghz[cal]['off1'][chan],cal10ghz[cal]['on'][chan])
        cal10ghz[cal]['loss2'][chan]=1.-fp2[1]
        plt.figure()
        plt.plot(cal10ghz[cal]['off1'][chan]*vcal-10.,label='Pre-calibration')
        plt.plot(cal10ghz[cal]['off2'][chan]*vcal-10.0,label='Post-calibration')
        plt.plot((fp[0]+fp[1]*(cal10ghz[cal]['on'][chan]))*vcal-10.0,label='Cal, scaled by '+str(fp[1])[0:4])
        plt.title('10 GHz calibration of loss by fit.  cal: '+str(cal)+ '  Channel: '+ chan)
        plt.xlabel('Sector');plt.ylabel('Volts');plt.grid();plt.legend(loc=0)
        plotfilename='cal_loss_10ghz_'+str(cal)+'_'+str(chan)+'.png'
        plt.savefig(plotfilename)
cPickle.dump(cal10ghz,f10a)
f10.close()

for cal in cals:
    cal15ghz[cal]['loss']={}
    cal15ghz[cal]['loss2']={}
    for chan in chans15ghz:
        fp=util.linfit(cal15ghz[cal]['on'][chan],cal15ghz[cal]['off1'][chan])
        cal15ghz[cal]['loss'][chan]=1.- 1./fp[1]
        fp2=util.linfit(cal15ghz[cal]['off1'][chan],cal15ghz[cal]['on'][chan])
        cal15ghz[cal]['loss2'][chan]=1.-fp2[1]
        plt.figure()
        plt.plot(cal15ghz[cal]['off1'][chan]*vcal-10.,label='Pre-calibration')
        plt.plot(cal15ghz[cal]['off2'][chan]*vcal-10.0,label='Post-calibration')
        plt.plot((fp[0]+fp[1]*(cal15ghz[cal]['on'][chan]))*vcal-10.0,label='Cal, scaled by '+str(fp[1])[0:4])
        plt.title('15 GHz calibration of loss by fit.  cal: '+str(cal)+ '  Channel: '+ chan)
        plt.xlabel('Sector');plt.ylabel('Volts')
        plt.grid()
        plt.legend(loc=0)
        plotfilename='cal_loss_15ghz_'+str(cal)+'_'+str(chan)+'.png'
        plt.savefig(plotfilename)
cPickle.dump(cal15ghz,f15a)
f15a.close()
