"""set of utility functions for acquisition software"""

import numpy as np
import pyfits as pyfits
import ephem 
import peakanalysis as pk
import matplotlib.pyplot as plt
from glob import glob
from scipy.signal import butter,filtfilt,iirdesign
from demod import datparsing
from matplotlib import pyplot as plt
from matplotlib import mlab
import time
import os


rtd=180/np.pi

def bcd_to_int(int_1):
    #function to pull out bytes from int_1 and int_2 and reconstruct BCD decimal number
        b_1=[]
        for i1 in int_1:
            b_1.append(bin(i1))
        outinteger=[]
        ob1=[]
        ob2=[]
        ob3=[]
        ob4=[]
        ob5=[]
        bb1=0
        bb2=0
        bb3=0
        bb4=0
        bb5=0
        for b1 in b_1:
            if len(b1)==20:
                bb1=int(b1[18:20],2)
                bb2=int(b1[14:18],2)
                bb3=int(b1[10:14],2)
                bb4=int(b1[6:10],2)
                bb5=int(b1[4:6],2)
                ob1.append(bb1)
                ob2.append(bb2)
                ob3.append(bb3)
                ob4.append(bb4)
                ob5.append(bb5)
                outinteger.append( bb1+ bb2*10+100*bb3+1000*bb4+10000*bb5)
        return outinteger,ob1,ob2,ob3,ob4,ob5

def rev_to_int(rev):
    #function to pull out bytes from  revecounter input and reconstruct  number
        outinteger=[]
        out1=[]
        out2=[]
        for r in rev:
            int1=int(bin(int(r))[4:12],2)
            int2=int(bin(int(r))[12:20],2)
            out1.append(int1)
            out2.append(int2)
            outinteger.append(int1+256*int2)
        return outinteger,out1,out2


def thicklegendlines(legendname,thick=3):
    lglines=legendname.get_lines()
    for line in lglines:
        line.set_linewidth(thick)
    plt.draw()

def rebin(a, (m, n)):
    """
    Downsizes a 2d array by averaging, new dimensions must be integral factors of original dimensions
    Credit: Tim http://osdir.com/ml/python.numeric.general/2004-08/msg00076.html
    """
    M, N = a.shape
    ar = a.reshape((M/m,m,N/n,n))
    return np.sum(np.sum(ar, 2), 0) / float(m*n)


def psd_function(freqs,wnlevel,fknee,alpha):
    """ 
    function to generate model PSD function (for fitting).
    Inputs freqs(array), wnlevel (value), Fknee (value), Alpha (value, for
    simple 1/f give alpha = 1)
    result will be power spectrum for all freqs in freqs, with
    wnlevel (input should be units/sqrt(Hz)) alpha will be for Power spectrum
    slope, not amplitude spectrum
    """
    nf=len(freqs)
    psdoutput=(wnlevel**2)*(1.+ (freqs/fknee)**(-alpha))
    return(psdoutput)
    
def psd_fit_function(p,x):
    # Parameter values are passed in "p"
    # for PSD p=[wnlevel,fknee,alpha]
    # form is f(x)=(p[0]**2)*(1.+ (x/p[1])**(-p[2]))
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # model = psd_function(x,p[0],p[1],p[2])
    model=(p[0]**2)*(1.+(x/p[1])**(-p[2]))
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return(model)
    
def psd_fit_function_resid(p,x,y,err):
    # Parameter values are passed in "p"
    # for PSD p=[wnlevel,fknee,alpha]
    # form is f(x)=(p[0]**2)*(1.+ (x/p[1])**(-p[2]))
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # model = psd_function(x,p[0],p[1],p[2])
    model=(p[0]**2)*(1.+(x/p[1])**(-p[2]))
    status = 0
    return((y-psd_fit_function(p,x))/err)

def fit_fknee(psd,freqs):
    """
    function to call scipy optimize.leastsq to fit PSD function, assumed output of
    nps function above
    """
    if min(freqs) == 0:
        freqs=freqs[1:]
        psd=psd[1:]
    nfreq=len(freqs)
    topfreqs=np.where(freqs>.8*np.max(freqs))
    err=(np.zeros(nfreq,dtype=float)+np.std(np.sqrt(psd[topfreqs])))#*(1/freqs)
    p=np.array([np.sqrt(np.mean(psd[topfreqs])),.15,1.0])
    m=optimize.leastsq(psd_fit_function_resid,p,args=(freqs,psd,err),full_output=1)
    pfinal=m[0]
    print 'wnlevel',pfinal[0]
    print 'Fknee' ,pfinal[1]
    print 'alpha' ,pfinal[2]
    return(m)
    


def nps(s, Fs,minfreq=None):
    """
    returns two vectors, frequencies and PSD
    PSD is in units^s/Hz
    """
    if minfreq != None:
        nfft=np.min([len(s),np.int(2.*Fs/minfreq)])
        nfft=2**(np.int(np.log2(nfft)))
    elif minfreq == None:
        nfft=len(s)
        nfft=2**(np.int(np.log2(nfft)))
    #Pxx, freqs = plt.psd(s, NFFT=nfft, Fs = Fs)
    Pxx, freqs = mlab.psd(s, NFFT=nfft, Fs = Fs)
    #we hate zero frequency
    freqs=freqs[1:]
    Pxx=Pxx[1:]
    return freqs, Pxx 
    
def nonlinmodel(g_0,b,t_in):
    """
    function to calculate nonlinear Vout for given input 
    gain, bparameter, voltage
    """
    v_out=t_in*(g_0/(1+b*g_0*t_in))
    return vout

def phasebin(nbins, az, signal,degrees=True):
    if degrees:
        az=(az*np.pi/180.)-np.pi
    ring_edges=np.where(np.diff(az) < -np.pi)
    nrings=len(ring_edges[0])
    phasebin_edges = np.linspace(-np.pi,np.pi, nbins+1)
    #SPLIT THE PHASE FOR EACH RING
    pseudomap = np.zeros([nbins,nrings-1],dtype=np.float32 ) 
    #plt.figure()
    #plt.hold(False)
    for ring in range(nrings-1):
        az_ring=az[ring_edges[0][ring]:ring_edges[0][ring+1]]
        signal_ring=signal[ring_edges[0][ring]:ring_edges[0][ring+1]]
        pseudomap[:,ring], edges = np.histogram(az_ring, bins=phasebin_edges, weights=signal_ring)
        #plt.plot(edges[:-1],pseudomap[:,ring])
        #plt.show()
        hits, edges = np.histogram(az_ring, bins=phasebin_edges)
        pseudomap[hits>0,ring] /= hits[hits>0]
    return pseudomap

def lowpass(d,sample_rate,cutoff):
    '''
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html#scipy.signal.filtfilt
    just stuff in an example from scipy to get this functional
    '''
    frac_cutoff=cutoff/(sample_rate/2.)
    print frac_cutoff
    b,a=butter(3,frac_cutoff)
    #b,a=iirdesign(frac_cutoff-.001,frac_cutoff+.1,.9,.1)
    filtered_d = filtfilt(b,a,d)
    return(filtered_d)

def highpass(d,sample_rate,cutoff):
    '''
    just do the lowpass above and subtract
    '''
    filtered_d=d-lowpass(d,sample_rate,cutoff)
    return(filtered_d)
    
def rebin(a, *args):
    '''rebin ndarray data into a smaller ndarray of the same rank whose dimensions
    are factors of the original dimensions. eg. An array with 6 columns and 4 rows
    can be reduced to have 6,3,2 or 1 columns and 4,2 or 1 rows.
    example usages:
    >>> a=rand(6,4); b=rebin(a,3,2)
    >>> a=rand(6); b=rebin(a,2)
    '''
    shape = a.shape
    lenShape = len(shape)
    factor = np.asarray(shape)/np.asarray(args)
    evList = ['a.reshape('] + \
             ['args[%d],factor[%d],'%(i,i) for i in range(lenShape)] + \
             [')'] + ['.sum(%d)'%(i+1) for i in range(lenShape)] + \
             ['/factor[%d]'%i for i in range(lenShape)]
    print ''.join(evList)
    return eval(''.join(evList))

def rebin_factor( a, newshape ):
        '''Rebin an array to a new shape.
        newshape must be a factor of a.shape.
        '''
        assert len(a.shape) == len(newshape)
        assert not np.sometrue(np.mod( a.shape, newshape ))

        slices = [ slice(None,None, old/new) for old,new in zip(a.shape,newshape) ]
        return a[slices]

if __name__ =='__main__':
    import matplotlib.pyplot as plt
    array_100x100= np.arange(100) * np.arange(100)[:,None]
    array_10x10 = rebin(array_100x100, (10, 10))
    plt.figure()
    plt.contourf(array_100x100)
    plt.contourf(array_10x10)
    plt.colorbar()
    
def remove_bad_raw_data(d):
    """
    function to find noise triggered data 
    returns cut down memmap whie still needs to be0
    tested for incomplete revolutions etc.
    """
    encoder=d['enc']/16
    g=np.where(np.diff(encoder) != 0)
    return (d[g])

def get_raw_data(utmin,utmax,freq='10'):
    '''
    function to turn the UT range into filenames and read in the raw data
    '''
    ltmin=utmin-7.0 #convert to local time first
    ltmax=utmax-7.0
    data_dir='/cofe/flight_data/'+str(freq)+'GHz/'
    if (ltmin<24) & (ltmax <24):
        data_dir=data_dir+'20110917/'     
    elif (ltmin>24) & (ltmax >24):
        data_dir=data_dir+'20110917/'
        ltmin=ltmin-24.
        ltmax=ltmax-24.
    
    #list the available files
    fl=glob(data_dir+'*.dat')
    ltfl=[]
    for file in fl:
        ltfl.append(file[-12:-4])
    ltflhours=np.zeros(len(ltfl))
    for i,lt in enumerate(ltfl):
        ltflhours[i]=np.float(lt[0:2])+np.float(lt[2:4])/60.+np.float(lt[4:6])/3600.
    fl=np.array(fl)
    ltflhours=np.array(ltflhours,dtype=float)
    files2read=fl[(ltflhours>ltmin) & (ltflhours<ltmax)]
    len(files2read)
    d=datparsing.read_raw(files2read)
    return(d)
    
    
    
def get_cofe_target(ut,lat,lon,target):
#function to use ephem to find az and el of specified target for COFE
#parameters: UT, LAt Lon Target
    cofe=ephem.Observer()
    cofe.elevation=0.0
    year=2013
    month=10
    day=04
    az=[]
    el=[]
    for u,la,lo in zip(ut,lat,lon):
        if (u >24):
            u=u-24
            day=05
        hour=int(np.fix(u))
        minute=(u-hour)*60
        iminute=int(np.fix(minute))
        second=int(np.fix((minute-iminute)*60))
        datestring=str(year)+'/'+str(month)+'/'+str(day)+' '+str(hour)+':'+str(iminute)+':'+str(second)
        datestring
        cofe.date=datestring
        cofe.lon=str(rtd*lo)
        cofe.lat=str(rtd*la)
        pos=ephem.__getattribute__(target)(cofe)
        az.append(pos.az)
        el.append(pos.alt)
        
    return np.array(az),np.array(el)
    
def get_cofe_crossing(ut,toi,gaz,centerut,lat=None,lon=None,target='Sun',plot=False):
    import peakanalysis as pk
    #function to find maximum peak signal crossing
    #in toi, return azoffset, elevation at crossing
    sblong=np.radians(-119.699)
    sblat=np.radians(34.4217)
    if lat==None:
        lat=np.zeros(len(ut))+sblat
        lon=np.zeros(len(ut))+sblong
    t=np.where(abs(ut-centerut) < .3/60.)
    h,=np.where(toi[t] == np.min(toi[t]))
    h=np.int(np.median(h))
    targetpos=get_cofe_target(ut[t],lat[t],lon[t],target)
    gfit=pk.fit_a_peak_ser(toi[t],h,invert=1)
    print gfit[0].params
    x=np.arange(1,len(ut[t])+1)
    gauss=pk.gaussian(gfit[0].params,x)
    if plot==True:
        plt.plot(x,toi[t])
        plt.hold(True)
        plt.plot(x,gauss)
    center=np.round(gfit[0].params[2])
    print(center)
    targetaz=rtd*targetpos[0][center]
    targetel=rtd*targetpos[1][center]
    azoffset=targetaz-gaz[center+t[0][0]]*rtd
    fitut=ut[center+t[0][0]]
    return azoffset,targetaz,targetel,fitut
    
def cctout(cc, gpstime):
    """cc and gpstime must be already synched"""
    utc = np.mod(((gpstime+15.)/3600.), 24)
    ut = utc[0]+(((cc - cc[0])*2e-9)/3600.)
    return ut
    
    
def oplot(*params):
    """function to emulate one good feature of IDL oplot with nice features of Python plot"""
    plt.hold(True)
    plot(*params)
    plt.hold(False)
    return
    
    
def linfit(x,y):
    """embed python lin algebra fitting to look like idl tool"""
    if len(y) != len(x):
        print 'inputs need to be same length arrays'
        
    a=np.vstack([x,np.ones(len(x))]).T
    m,b=np.linalg.lstsq(a,y)[0]
    return np.array([b,m])

def find_command_uts(command):
#script to read in cmdecho file, find lines with 
#requested command, and return adjusted UT (adjusted
#by offset to match v 0.5 level 1 files, calibration signal
# in ch a/d 1 of 15 GHz. near 16:42 UT.
    import datetime
    f=open('C:\\cofe\\flight_data\\CIP_commanding\\623nmisc\\cmdecho.dat')
    
    timelist=[]
   
    for line in f:
        linelist=line.split("\t")
        linedate=datetime.datetime.strptime(linelist[0]+' '+linelist[1],'%m/%d/%Y %H:%M:%S')
        addr=linelist[2]
        cmd=(linelist[3].strip('\n'))
        if ((cmd == command) and (addr == '0006')):
            print 'found one'
            #utadjusted=24*(linedate.day-17.)+linedate.hour+linedate.minute/60.+linedate.second/3600.
            #timelist.append(utadjusted)
            timelist.append((linedate.day,linedate.hour,linedate.minute,linedate.second))
    return timelist
    f.close()
    
def raise_bit(flag, bit=0):
    '''Raise bit of the flag array'''
    return np.bitwise_or(flag, 2**bit)

def check_bit(flag, bit=0):
    '''Check if bit of the flag array is raised'''
    return np.bitwise_and(flag, int(2**bit)) > 0
    
def grab_x_from_plot(fig):

    print 'right button press selects xvalue to store. middle click to  end function'
    global startlist,stoplist,start
    global cid
    global ptnum
    ptnum=0
    start=True
    startlist=[]
    stoplist=[]
    
    def onclick(event):
        global ptnum,startlist,stoplist,start
        global cid
        print ptnum
        print ptnum%2
        if event.button == 3:
            if ptnum%2 == 0:
                startlist.append(event.xdata)
                print 'chose start point',event.xdata
                print 'select stop point'
            elif ptnum%2 == 1:
                stoplist.append(event.xdata)
                print 'chose stop point',event.xdata
                print 'select next startpoint'
            start=False
            ptnum+=1
        elif event.button ==2:
            print 'should quit now, was here: ',event.xdata
            print cid
            fig.canvas.mpl_disconnect(cid)
    cid=fig.canvas.mpl_connect('button_press_event',onclick)
    outlist=np.concatenate((np.array(startlist),np.array(stoplist)),axis=2)
    return(outlist)

def gaussian(p, x):
    # Parameter values are passed in "p"
    # for gaussian p=[offset,amplitude,xposition, sigma]
    # form is f(x)=p[0]+p[1]*exp(-((x-p[2])/p[3])^2)
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    p=np.array(p)
    model = p[0]+p[1]*np.exp(-((x-p[2])/p[3])**2)
    return(model)            
       
def gaussianresid(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # for gaussian p=[offset,amplitude,sigma]
    # form is f(x)=p[0]+p[1]*exp(-((x-p[2])/p[3])^2)
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # p=np.array(p)
    model = p[0]+p[1]*np.exp(-((x-p[2])/p[3])**2)    
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return([status, (y-model)/err])
    
    
def fit_gaussian(x,y,yerr=None):
    import mpfit as mp
    if yerr==None:
        yerr=np.std(y)
    err=yerr*np.ones(x.size,dtype=float)
    fa={'x':x,'y':y,'err':err}
    peakval=x[y==np.max(y)][0]
    p=np.array([np.min(y),np.max(y)-np.min(y),peakval,.1])
    m=mp.mpfit(gaussianresid,p,functkw=fa,quiet=1,maxiter=10)
    if m.status<1:
        print(p)
        print(values)
        print(fa)
        print(parinfo)
        plt.plot(toi)
        plt.plot(toierr)
    
#    sigma=abs(m.params[3])
#    center=m.params[2]
#    redchi=m.fnorm
    return m
    
def fixlong(longitude):
    """just get rid of outrageous points for smooth values"""
    
    bd=np.where((abs(longitude[1:-1]-longitude[0:-2]) > .002) | (abs(longitude[1:-1]) > 6.5))
    bd=bd[0]
    gd=np.where((abs(longitude[1:-1]-longitude[0:-2]) < .002) & (abs(longitude[1:-1]) < 6.5))
    gd=gd[0]
    longitudef=longitude
    if ((bd.size >0) & (gd.size >0)):
        for bad in bd:
            longitudef[bad]=longitudef[gd[np.where(abs(gd-bad) == min(abs(gd-bad)))][0]]
        
    return longitudef
    
def linfit(x,y):
    """embed python lin algebra fitting to look like idl tool"""
    if len(y) != len(x):
        print 'inputs need to be same length arrays'
        
    a=np.vstack([x,np.ones(len(x))]).T
    m,b=np.linalg.lstsq(a,y)[0]
    return np.array([b,m])
    
        
        
    
        
        