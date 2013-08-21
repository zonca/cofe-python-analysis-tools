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

for ch in ['ch1','ch3','ch5']:
    calsecco[ch]=(tamb-tsky)/(np.mean(cal[ch].flatten()[secco])/np.mean(cal[ch].flatten()[ssky2]))
calsecco['ch0']=calsecco['ch1']/bbgain['ch0']
calsecco['ch2']=calsecco['ch3']/bbgain['ch2']
calsecco['ch4']=calsecco['ch5']/bbgain['ch4']

#now get the other sky data
get_ipython().magic(u"cd 'c:/cofe/cofe_ground_fall_2012/data/20121113'")
fl=glob('*.dat')
dsky=[]
for f in fl:
    dsky.append(demod.demodulate_dat(f,10))
    
dsky=np.concatenate(dsky)

for ch in chans:
    zsky1t=cu.nps(dsky[ch]['T'][:5200],rotrate,minfreq=.1)
    zsky1q=cu.nps(dsky[ch]['Q'][:5200],rotrate,minfreq=.1)
    zsky1u=cu.nps(dsky[ch]['U'][:5200],rotrate,minfreq=.1)
    plt.figure(figsize=(12,6))
    hold(True)
    plt.plot(zsky1t[0],np.sqrt(zsky1t[1])*calsecco[ch]*1000.,label='T')
    plt.plot(zsky1q[0],np.sqrt(zsky1q[1])*calsecco[ch]*1000.,label='Q')
    plt.plot(zsky1u[0],np.sqrt(zsky1u[1])*calsecco[ch]*1000.,label='U')
    
    plt.title('Sky test Nov 13, 2012 (Rough cal to 300K). 10 GHz COFE detector '+ch)
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude Spectral Density, mK/sqrt(Hz)')
    leg=legend()
    cu.thicklegendlines(leg)
    #plt.xscale('log'),plt.yscale('log')
    plt.show()
    plt.ylim([0,3]),plt.xlim([0,12])
    plt.savefig('asd_ecco_cal_demod_coarse'+ch)
    
#now get the other sky data nov 14
get_ipython().magic(u"cd 'c:/cofe/cofe_ground_fall_2012/data/20121114'")
fl=glob('*.dat')
dsky=[]
for f in fl[5:80]:
    dsky.append(demod.demodulate_dat(f,10))
    
dsky=np.concatenate(dsky)

for ch in chans:
    zsky1t=cu.nps(dsky[ch]['T'][:5200],rotrate,minfreq=.01)
    zsky1q=cu.nps(dsky[ch]['Q'][:5200],rotrate,minfreq=.01)
    zsky1u=cu.nps(dsky[ch]['U'][:5200],rotrate,minfreq=.01)
    plt.figure(figsize=(12,6))
    hold(True)
    plt.plot(zsky1t[0],np.sqrt(zsky1t[1])*calsecco[ch]*1000.,label='T')
    plt.plot(zsky1q[0],np.sqrt(zsky1q[1])*calsecco[ch]*1000.,label='Q')
    plt.plot(zsky1u[0],np.sqrt(zsky1u[1])*calsecco[ch]*1000.,label='U')
    
    plt.title('Sky test Nov 14, 2012 (Rough cal to 300K). 10 GHz COFE detector '+ch)
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude Spectral Density, mK/sqrt(Hz)')
    leg=legend()
    cu.thicklegendlines(leg)
    #plt.xscale('log'),plt.yscale('log')
    plt.show()
    plt.ylim([0,3]),plt.xlim([0,12])
    plt.savefig('asd_ecco_cal_demod_nov14'+ch)
    