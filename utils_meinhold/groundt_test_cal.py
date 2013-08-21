#script to run through cal test data
import demod
from glob import glob
import cofe_util as cu

get_ipython().magic(u"cd 'c:/cofe/cofe_ground_fall_2012/data/20121109'")
fl=glob('*.dat')
flcal=fl[77:]
cal=demod.read_raw(flcal)
#first capture specific timezones for nov 9 2012 dataset
ssky1=arange(100000)
ssky2=arange(100000)+450000
ssky3=arange(100000)+840000
sfoam1=arange(100000)+260000
sfoam2=arange(100000)+1030000
secco=arange(100000)+645000

chans=['ch0','ch1','ch2','ch3','ch4','ch5']

#base rotation rate
rotrate=25 
samprate=rotrate*256
bbgain={}
bbgain['ch0']=100.
bbgain['ch2']=100.
bbgain['ch4']=100.
tamb=295
#arbitrary, but hopefully low impact on the gain
tsky=40 
epsilons={}
calsecco={}
calfoam={}
for ch in chans:
    zsky1=cu.nps(cal[ch].flatten()[ssky1],samprate,minfreq=1)
    zsky3=cu.nps(cal[ch].flatten()[ssky3],samprate,minfreq=1)
    zfoam1=cu.nps(cal[ch].flatten()[sfoam1],samprate,minfreq=1)
    zfoam2=cu.nps(cal[ch].flatten()[sfoam2],samprate,minfreq=1)
    zecco=cu.nps(cal[ch].flatten()[secco],samprate,minfreq=1)
    epsilon=np.sqrt((zfoam1[1][zfoam1[0]==50] + zfoam2[1][zfoam2[0]==50]))/(np.sqrt(zsky1[1][zsky1[0]==50]) + np.sqrt(zsky3[1][zsky3[0]==50]))
    epsilons[ch]=epsilon[0]
    plt.figure(figsize=(12,6))
    plt.plot(zsky1[0],np.sqrt(zsky1[1]),label='Sky1')
    plt.plot(zsky3[0],np.sqrt(zsky3[1]),label='Sky3')
    plt.plot(zfoam1[0],np.sqrt(zfoam1[1]),label='Foam1')
    plt.plot(zfoam2[0],np.sqrt(zfoam2[1]),label='Foam2')
    plt.plot(zecco[0],np.sqrt(zecco[1]),label='eccosorb')
    plt.title('Sky tests Nov , 2012 (thRu  pit door). 10 GHz COFE detector '+ch+' emissivity='+np.str(epsilon[0]))
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude Spectral Density, V/sqrt(Hz)')
    leg=legend()
    cu.thicklegendlines(leg)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    plt.savefig('asd_uncal_'+ch)
for ch in ['ch1','ch3','ch5']:
    calsecco[ch]=(tamb-tsky)/(np.mean(cal[ch].flatten()[secco])/np.mean(cal[ch].flatten()[ssky2]))
calsecco['ch0']=calsecco['ch1']/bbgain['ch0']
calsecco['ch2']=calsecco['ch3']/bbgain['ch2']
calsecco['ch4']=calsecco['ch5']/bbgain['ch4']

for ch in chans:
    zsky1=cu.nps(cal[ch].flatten()[ssky1],samprate,minfreq=1)
    zsky3=cu.nps(cal[ch].flatten()[ssky3],samprate,minfreq=1)
    zfoam1=cu.nps(cal[ch].flatten()[sfoam1],samprate,minfreq=1)
    zfoam2=cu.nps(cal[ch].flatten()[sfoam2],samprate,minfreq=1)
    zecco=cu.nps(cal[ch].flatten()[secco],samprate,minfreq=1)
    plt.figure(figsize=(12,6))
    plt.plot(zsky1[0],np.sqrt(zsky1[1])*calsecco[ch]*1000.,label='Sky1')
    plt.plot(zsky3[0],np.sqrt(zsky3[1])*calsecco[ch]*1000.,label='Sky3')
    plt.plot(zfoam1[0],np.sqrt(zfoam1[1])*calsecco[ch]*1000.,label='Foam1')
    plt.plot(zfoam2[0],np.sqrt(zfoam2[1])*calsecco[ch]*1000.,label='Foam2')
    plt.plot(zecco[0],np.sqrt(zecco[1])*calsecco[ch]*1000.,label='eccosorb')
    plt.title('Sky tests Nov , 2012 (Rough cal to 300K). 10 GHz COFE detector '+ch)
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude Spectral Density, mK/sqrt(Hz)')
    leg=legend()
    cu.thicklegendlines(leg)
    #plt.xscale('log'),plt.yscale('log')
    plt.show()
    plt.ylim([0,3]),plt.xlim([0,1000])
    plt.savefig('asd_ecco_cal_'+ch)
    
ssky1d=ssky1[::256]/256
ssky2d=ssky2[::256]/256
ssky3d=ssky3[::256]/256
sfoam1d=sfoam1[::256]/256
sfoam2d=sfoam1[::256]/256
seccod=secco[::256]/256
caldemod=demod.demodulate(cal,10)   
for ch in chans:
    zsky1d=cu.nps(caldemod[ch]['Q'][ssky1d],rotrate,minfreq=.1)
    zsky2d=cu.nps(caldemod[ch]['Q'][ssky2d],rotrate,minfreq=.1)
    zsky3d=cu.nps(caldemod[ch]['Q'][ssky3d],rotrate,minfreq=.1)
    zfoam1d=cu.nps(caldemod[ch]['Q'][sfoam1d],rotrate,minfreq=.1)
    zfoam2d=cu.nps(caldemod[ch]['Q'][sfoam2d],rotrate,minfreq=.1)
    zeccod=cu.nps(caldemod[ch]['Q'][seccod],rotrate,minfreq=.1)
    plt.figure(figsize=(12,6))
    plt.plot(zsky1d[0],np.sqrt(zsky1d[1])*calsecco[ch]*1000.,label='Sky1')
    plt.plot(zsky3d[0],np.sqrt(zsky3d[1])*calsecco[ch]*1000.,label='Sky3')
    plt.plot(zfoam1d[0],np.sqrt(zfoam1d[1])*calsecco[ch]*1000.,label='Foam1')
    plt.plot(zfoam2d[0],np.sqrt(zfoam2d[1])*calsecco[ch]*1000.,label='Foam2')
    plt.plot(zeccod[0],np.sqrt(zeccod[1])*calsecco[ch]*1000.,label='eccosorb')
    plt.title('Sky tests Nov 9, 2012 (Rough cal to 300K Demod 10 GHz COFE detector Q '+ch)
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude Spectral Density, mK/sqrt(Hz)')
    leg=legend()
    cu.thicklegendlines(leg)
    #plt.xscale('log'),plt.yscale('log')
    plt.show()
    plt.ylim([0,3]),plt.xlim([0,12])
    plt.savefig('asd_ecco_cal_demod_Q_'+ch)    
    
flskytest=fl[71:77]
skytest=demod.read_raw(flskytest)   
skytestdemod=demod.demodulate(skytest,10)
for ch in chans:
    ztd=cu.nps(skytestdemod[ch]['T'],rotrate,minfreq=.1)
    zqd=cu.nps(skytestdemod[ch]['Q'],rotrate,minfreq=.1)
    zud=cu.nps(skytestdemod[ch]['U'],rotrate,minfreq=.1)
    plt.figure(figsize=(12,6))
    plt.plot(ztd[0],np.sqrt(ztd[1])*calsecco[ch]*1000.,label='T')
    plt.plot(zqd[0],np.sqrt(zqd[1])*calsecco[ch]*1000.,label='Q')
    plt.plot(zud[0],np.sqrt(zud[1])*calsecco[ch]*1000.,label='U')
    plt.title('Sky tests Nov 9, 2012 (Rough cal to 300K Demod 10 GHz COFE detector '+ch)
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude Spectral Density, mK/sqrt(Hz)')
    leg=legend()
    cu.thicklegendlines(leg)
    #plt.xscale('log'),plt.yscale('log')
    plt.show()
    plt.ylim([0,3]),plt.xlim([0,12])
    plt.savefig('asd_ecco_cal_demod_TQU_'+ch)   



    