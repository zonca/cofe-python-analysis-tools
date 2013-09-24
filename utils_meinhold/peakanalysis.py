# These funtions read Jean-Luc's old trace data from fits files,
# find peaks, generate histograms and plot  histograms

from GUI.FileDialogs import *
import pyfits
import numpy as np
import UniversalLibrary as ul
import mpfit as mp
import matplotlib.pyplot as plt
import scipy.io
import time
import gc
from Tkinter import *
import tkFileDialog

caprange=np.arange(1,100000)-50000
sigma_cutoff=600  # ignore peaks this wide

def thicklegendlines(legendname,thick=3):
    lglines=legendname.get_lines()
    for line in lglines:
        line.set_linewidth(thick)
    plt.draw()


def check_stats_mc(pkpos,pkheights,pksigmas,pksnas,diffchis,minwidth=1,maxwidth=8,minsna=2,mindiffchis=.2):
    #function to match fitted peak positions to input montecarlo. Assume peaks at 10000, 12000 and 
    #every 10000 after that.
    #returns two lists of positions for good 'bigs' and good 'smalls'
    #first make the blind cuts:
    nfiltered=0;nfiltered_dups=0;nbig=00;nsmall=0
    g=np.where((pksnas>minsna) & (diffchis > mindiffchis)&(pksigmas<maxwidth)&(pksigmas>minwidth))
    test=pkpos[g[0]]
    nfiltered=len(test)
    if nfiltered>2:
        diff_filtered=test-np.roll(test,1)
        testfiltered=test[np.abs(diff_filtered)>maxwidth]
        nfiltered_dups=len(testfiltered)
        if nfiltered_dups>0:
            #now check in these blind filtered data for which ones line up on MC input particles
            testres=np.remainder(test+1000,10000)
            ggbig=np.where(np.abs(testres-1000)<maxwidth)
            ggsmall=np.where(np.abs(testres-3000)<maxwidth)
            #remove duplicates- use dumb idea of just keeping first point meeting peak criteria
            testbig=test[ggbig[0]]
            testsmall=test[ggsmall[0]]
            if len(testbig) >1:
                diffsbig=testbig-np.roll(testbig,1)
                if len(testsmall)>1:
                    testbig=testbig[np.abs(diffsbig)>maxwidth]
                    diffssmall=testsmall-np.roll(testsmall,1)
                    testsmall=testsmall[np.abs(diffssmall)>maxwidth]
                    nsmall=len(testsmall)
                    nbig=len(testbig)
    
    return nfiltered,nfiltered_dups,nbig,nsmall
    

def get_old_data():
    infileref=request_old_files(prompt='Choose a fits TOD file')
    datad={}
    data_arrays=np.zeros(0)
    vlowarray=[]
    vhiarray=[]
    gainarray=[]
    for fileref in infileref:
        filename=fileref.path
        hdulist=pyfits.open(filename)
        gain=hdulist[1].header['gain']
        v_high=hdulist[1].header['v_high']
        v_low=hdulist[1].header['v_low']
        n_samp=hdulist[1].header['n_samp']
        vlowarray.append(v_low)
        vhiarray.append(v_high)
        gainarray.append(gain)
        #period=hdulist[1].header['period']
        data_array=hdulist[1].data.field('samples')
        data_array*=(data_array/(v_high - v_low))/gain
        data_arrays=np.concatenate((data_arrays,data_array),axis=0)
    samplerate=1000000
    if 'samplerate' in hdulist[1].header.keys():
        samplerate=hdulist[1].header['samplerate']
    datad['samplerate']=samplerate
    datad['data']=data_arrays
    datad['gain']=np.array(gainarray)
    datad['v_low']=np.array(vlowarray)
    datad['v_hi']=np.array(vhiarray)
    return datad
    
def read_matfile(infiles=None):
    """function to read in andrew's matlab files"""
    master=Tk()
    master.withdraw()
    if infiles==None:
        infiles=tkFileDialog.askopenfilenames(title='Choose one or more matlab TOD file',initialdir='c:/ANC/data/matlab_data/')
        infiles=master.tk.splitlist(infiles)
    data_arrays=np.zeros(0)
    datad={}
    vlowarray=[]
    vhiarray=[]
    gainarray=[]
    for filename in infiles:
        #print filename
        mat=scipy.io.loadmat(filename)
        toi=-mat['out']['V1'][0][0][0]/(mat['out']['Vb'][0][0][0][0]-mat['out']['Va'][0][0][0][0])
        gainarray.append(1.)
        vlowarray.append(mat['out']['Va'][0][0][0][0])
        vhiarray.append(mat['out']['Vb'][0][0][0][0])
        samplerate=np.int(1/(mat['out']['t'][0][0][0][1]-mat['out']['t'][0][0][0][0]))
        data_arrays=np.concatenate((data_arrays,toi),axis=0)
    datad['data']=data_arrays
    datad['samplerate']=samplerate
    datad['gain']=np.array(gainarray)
    datad['v_low']=np.array(vlowarray)
    datad['v_hi']=np.array(vhiarray)
    return datad
    
def find_peaks(toi,pksigma=1.5,pkwidth=5):
# find peaks in toi data first
#first remove saturation
    print 'params pk',pksigma,pkwidth,len(toi)
    satlevel=np.max(toi)
    s=np.where(toi == satlevel)
    s=np.array(s[0])
    bad=np.zeros(0)
    for si in s:
        newbad=caprange+si
        bad=np.concatenate((bad,newbad),axis=0)
    if len(bad)>0:
        toi[np.int32(bad)]=0
    print 'satpoints',len(bad)
    g=np.where(toi < pksigma*np.std(toi))
    sig=np.std(toi[g])
    pks=np.array(np.where(toi > pksigma*sig)[0])
    print 'in pk lenpks',len(pks)
    return pks
    
def remove_saturation(toi):
# algorithm to cut out saturated data points
    outtoi=np.copy(toi)
    satlevel=np.max(outtoi)
    outtoi=outtoi[outtoi<satlevel]
#    s=np.where(outtoi == satlevel)
#    s=np.array(s[0])
#    bad=np.zeros(0)
#    for si in s:
#        newbad=caprange+si
#        bad=np.concatenate((bad,newbad),axis=0)
#    outtoi[np.int32(bad)]=0  
#    outtoi=outtoi[outtoi != 0]
    return(outtoi)
    
def get_some_data(npts):
#acquire from the board
    BoardNum=0
    Gain=ul.BIP5VOLTS
    Chan=0
    v=zeros(npts)
    for i in arange(npts):
        d=ul.cbAIn(BoardNum,Chan,Gain)
        v[i]=ul.cbToEngUnits(BoardNum,Gain,d)
    return v
   
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
def gaussiansatresid(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # for gaussian p=[offset,amplitude,sigma]
    # form is f(x)=p[0]+p[1]*exp(-((x-p[2])/p[3])^2) < p[4]
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # p=np.array(p)
    model = p[0]+p[1]*np.exp(-((x-p[2])/p[3])**2)    
    model[model>p[4]]=p[4]
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return([status, (y-model)/err])


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
def gaussiansat(p, x):
    # Parameter values are passed in "p"
    # for gaussian p=[offset,amplitude,xposition,sigma,saturation cutoff]
    # form is f(x)=p[0]+p[1]*exp(-((x-p[2])/p[3])^2)
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    p=np.array(p)
    model = p[0]+p[1]*np.exp(-((x-p[2])/p[3])**2)
    model[model>p[4]]=p[4]
    return(model)
    

def fit_a_peak_ser(toi, peak, pplot=True,invert=None,maxiter=3,pkcapwidth=20,toierr=None):
    # procedure to run mpfit on a toi at the position peak
    # use this to test consistency by hand
    #this one just fits the subset of toi provided
    x=np.arange(len(toi))
    if toierr==None:
        toierr=np.std(toi)
    err=toierr*(np.zeros(x.size,dtype=float)+1.)
    fa={'x':x,'y':toi,'err':err}
    dd=toi-np.mean(toi)
    ddr=dd/toierr
    startchi=np.sum(ddr**2)
    startredchi=startchi/len(ddr)
    sat=False
    #if len(toi[toi==np.max(toi)])>2:
    #    sat=True
    if sat==True:
        peakval=x[dd==np.max(dd)][0]
        parinfo = [{'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]} for i in range(5)]
        parinfo[0]['limited'][0] = 1
        parinfo[0]['limited'][1] = 1
        parinfo[0]['limits']  = [np.min(toi),np.max(toi)]        
        parinfo[1]['limited'][0] = 1
        parinfo[1]['limits'][0]  = 0.
        parinfo[2]['limited'][0] = 1
        parinfo[2]['limited'][1] = 1
        parinfo[2]['limits']  = [np.min(x),np.max(x)]        
        parinfo[3]['limited'][0] = 1
        parinfo[3]['limited'][1] = 1
        parinfo[3]['limits']  = [1,pkcapwidth/2.]        
        #values = [np.min(toi), np.max(toi)-np.min(toi),peak, pkcapwidth/10.,np.max(toi)/2.0]
        
        values = [np.min(toi), np.max(toi)-np.min(toi),peakval, pkcapwidth/10.,np.max(toi)/2.0]
        for i in range(5): parinfo[i]['value']=values[i]
        p=np.array([np.min(toi),np.max(toi)-np.min(toi),peakval,pkcapwidth/10.,np.max(toi)/2.0])
        m=mp.mpfit(gaussiansatresid,p,functkw=fa,quiet=1,maxiter=maxiter,parinfo=parinfo)
        #print m.status
    if sat==False:
        peakval=x[dd==np.max(dd)][0]
        parinfo = [{'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]} for i in range(4)]
        parinfo[0]['limited'][0] = 1
        parinfo[0]['limited'][1] = 1
        parinfo[0]['limits']  = [np.min(toi),np.max(toi)]        
        parinfo[1]['limited'][0] = 1
        parinfo[1]['limits'][0]  = 0.
        parinfo[2]['limited'][0] = 1
        parinfo[2]['limited'][1] = 1
        parinfo[2]['limits']  = [np.min(x),np.max(x)]        
        parinfo[3]['limited'][0] = 1
        parinfo[3]['limited'][1] = 1
        parinfo[3]['limits']  = [1,pkcapwidth/2.]        
        values = [np.min(toi), np.max(toi)-np.min(toi),peakval, pkcapwidth/10.,np.max(toi)/2.0]
        for i in range(4): parinfo[i]['value']=values[i]        
        p=np.array([np.min(toi),np.max(toi)-np.min(toi),peakval,pkcapwidth/10.])
        m=mp.mpfit(gaussianresid,p,functkw=fa,quiet=1,maxiter=maxiter,parinfo=parinfo)
    if m.status<1:
        print(p)
        print(values)
        print(fa)
        print(parinfo)
        plt.plot(toi)
        plt.plot(toierr)
        
    sigma=abs(m.params[3])
    center=m.params[2]
    
    redchi=m.fnorm
    if m.dof>0:
        redchi=redchi/m.dof
    diffchi=startredchi-redchi
    if sat == False:
        g=gaussian(m.params,x)   
    if sat ==True:
        g=gaussiansat(m.params,x)
    #if diffchi < .1:
        toi=np.mean(toi)
    if pplot:
        plt.ion()
        plt.figure(3)
        plt.hold(False)
        plt.plot(x,toi,label='Raw TOI,red chi = '+np.str(startredchi))
        plt.hold(True)
        plt.plot(x,g,label='Gaussian fit')
        plt.plot(x,toi-g,label='Residual, red chi = '+np.str(redchi))
        plt.legend()
        plt.xlabel('Sample index')
        plt.ylabel('Signal, V')
        plt.title('Single Peak Gaussian Fit')
        plt.show()
    return(m,toi,diffchi)

def gather_stats(toi,pkcapwidth=40,pksigmacut=3.0,min_sn=3,min_width=1,max_width=20,min_diffchis=.3,pplot=False,toierr=None,runninghist=False,fignum=None):
    """
    function to break toi into manageable chunks for gather peaks bysize, and concatenate
    results
    """
    if fignum==None:
        fignum=100
    npts=len(toi)
    nsub=1+np.int(npts/200000)
    toisubs=np.array_split(toi,nsub)
    peakstats={}
    peakstats['pk_size']=np.array([])
    peakstats['pk_position']=np.array([])
    peakstats['pk_width']=np.array([])
    peakstats['pk_sn']=np.array([])
    peakstats['pk_diffchis']=np.array([])
    plt.ion()    
    for subtoi in toisubs:
        pksub=gather_peaks_bysize(subtoi,pkcapwidth=pkcapwidth,pksigmacut=pksigmacut,pplot=pplot,toierr=toierr)
        peakstats['pk_size']=np.concatenate([peakstats['pk_size'],pksub['pk_size']])
        peakstats['pk_position']=np.concatenate([peakstats['pk_position'],pksub['pk_position']])
        peakstats['pk_width']=np.concatenate([peakstats['pk_width'],pksub['pk_width']])
        peakstats['pk_sn']=np.concatenate([peakstats['pk_sn'],pksub['pk_sn']])
        peakstats['pk_diffchis']=np.concatenate([peakstats['pk_diffchis'],pksub['pk_diffchis']])
        if runninghist==True:
            h=get_histogram(peakstats,min_sn=min_sn,min_diffchis=min_diffchis,min_width=min_width,max_width=max_width,plotdiff=False,running=True,fignum=fignum)
    return peakstats
    
def get_histogram(peakstats,nbins=100,pplot=True,min_width=1,max_width=20,min_sn=3,min_diffchis=.5,sizecal=1.,plotfile=None,plotdiff=True,fignum=None, running=False):
    """
    function to create histogram from fit statistics of peaks. Use several cuts. Returns
    histogram dictionary. If available, sizecal calibrates x axis to nM radius.
    if 'running' then use fignum to ovewrited histogram. to be used when plotting histogram while running the fits at the same time
    """
    pkhist=None
    intotal=len(peakstats['pk_size'])
    pksizes=np.array(peakstats['pk_size'][(peakstats['pk_width']>min_width) & (peakstats['pk_width']<max_width) & (peakstats['pk_sn']>min_sn) & (peakstats['pk_diffchis']>min_diffchis)])
    outtotal=len(pksizes)
    if outtotal>-1:
        pksizes=pksizes**0.333
        if len(pksizes)>0:
            pkhist=np.histogram(pksizes,bins=nbins,range=[0,np.max(pksizes)])
            histmin=np.min(pkhist[0])
            histmax=np.max(pkhist[0])
            pkhistraw=np.histogram((peakstats['pk_size'])**0.333,bins=nbins,range=[0,np.max(pksizes)])
        if len(pksizes)==0:
            pkhistraw=np.histogram((peakstats['pk_size'])**0.333,bins=nbins)
            histmin=np.min(pkhistraw[0])
            histmax=np.max(pkhistraw[0])
        if pplot:
            if running==False:
                plt.figure(fignum)
                plt.hold(True)
                plt.bar(sizecal*pkhistraw[1][1:],(pkhistraw[0]),width=pkhistraw[1][2]-pkhistraw[1][1],label='Raw, n='+np.str(intotal),color='blue')
                if len(pksizes)>0:
                    plt.bar(sizecal*pkhist[1][1:],(pkhist[0]),width=pkhist[1][2]-pkhist[1][1],label='Filtered, n='+np.str(outtotal),color='red')
                if plotdiff==True:
                    plt.bar(sizecal*pkhistraw[1][1:],(pkhistraw[0]-pkhist[0]),width=pkhistraw[1][2]-pkhistraw[1][1],label='Difference',color='green')
                plt.legend()
                plt.xlabel('Particle diameter (not normalized)')
                plt.ylabel('Number of particles')
                plt.title('Cuts: '+np.str(min_width)+'<width<'+np.str(max_width)+',s/n >'+np.str(min_sn)+',Chisqdiff>'+np.str(min_diffchis))
                plt.draw()

            if running==True:
                plt.ion()
                if fignum==None:
                    fignum=100
                plt.figure(fignum)
                plt.close()
                plt.hold(False)
                plt.bar(sizecal*pkhistraw[1][1:],(pkhistraw[0]),width=pkhistraw[1][2]-pkhistraw[1][1],label='Raw, n='+np.str(intotal),color='blue')
                plt.hold(True)
                if len(pksizes)>0:
                    plt.bar(sizecal*pkhist[1][1:],(pkhist[0]),width=pkhist[1][2]-pkhist[1][1],label='Filtered, n='+np.str(outtotal),color='red')
                plt.legend()
                plt.xlabel('Particle diameter (not normalized)')
                plt.ylabel('Number of particles')
                plt.title('Cuts: '+np.str(min_width)+'<width<'+np.str(max_width)+',s/n >'+np.str(min_sn)+',Chisqdiff>'+np.str(min_diffchis))
                plt.show()
                print 'did I plot?'
            if plotfile!=None:
                plt.savefig(plotfile)
    return pkhist
    
    
def gather_peaks_bysize(toi,pkcapwidth=40,pksigmacut=3.0,pplot=False,toierr=None):
    """
    function fits and removes peaks one by one, in sort ordering of input toi fit is done
    over pkcapwidth samples centered on each successive lower size point. Keep track of already
    fit areas with blank array    don't do subtraction, do keep peaks every time
    """
    toi=remove_saturation(toi)
    toisigma=np.std(toi)
    blank=[]
    tstart=time.ctime()
    pksizes=[]
    pksigmas=[]
    pksize_sn=[]
    pkpos=[]
    diffchis=[]
    #print toisigma,toisigma*pksigmacut
    peakxlist=np.array([peakfitcenters[0] for peakfitcenters in sorted(enumerate(toi),reverse=True,key=lambda x:x[1])])
    peakvlist=np.array(sorted(toi,reverse=True))
    peakvlist=np.array(peakvlist[peakvlist > pksigmacut*toisigma])
    npeaks=len(peakvlist)
    peakxlist=peakxlist[:npeaks]
    
    for peakx in peakxlist:
        if peakx in blank:
            #print 'skip duplicate'
            continue
        xlo=np.max([peakx-pkcapwidth/2,0])
        xhi=np.min([peakx+pkcapwidth/2,len(toi)-1])
        d=toi[xlo:xhi]
        blank.extend(range(xlo,xhi))
        m,dummy,diffchi=fit_a_peak_ser(d,pkcapwidth/2,pplot=pplot,pkcapwidth=pkcapwidth,toierr=toierr)
        if m.perror[3]!=0:
            sn=m.params[3]/m.perror[3]
        if sn>.5:
            pksizes.append(m.params[1])
            pkpos.append(m.params[2]+xlo)
            pksigmas.append(m.params[3])
            pksize_sn.append(sn)
            diffchis.append(diffchi)
    tstop=time.ctime()
    gc.collect()
    print tstart
    print tstop
    #print len(pksizes)
    peakstats={}
    peakstats['pk_size']=np.array(pksizes)
    peakstats['pk_position']=np.array(pkpos)
    peakstats['pk_width']=np.array(pksigmas)
    peakstats['pk_sn']=np.array(pksize_sn)
    peakstats['pk_diffchis']=np.array(diffchis)
    return peakstats
    
def quickpeak(toi,peak,cut=None,invert=None):
    #fast and dirty way to get peaks. use JL method, hardwired
    bw=5
    meanrange=np.concatenate((np.arange(bw)-3*bw,np.arange(bw)+3*bw),axis=0)
    pksize=toi[peak]-np.mean(toi[peak+meanrange])
    toi=np.concatenate((toi[0:peak-bw],toi[peak+bw:]),axis=0)
    return(pksize,toi)
def quick_get_next_peak(toi):
    #fast version of get next peak using quickpeak
    peak=np.where(toi == np.max(toi))
    peak=peak[0][0]
    pksize,toi=quickpeak(toi,peak)
    return(pksize,toi)
def quick_gather_peaks(toi,npeaks):
    pksizes=[]
    pksize_sn=[]
    for i in range(npeaks):
        pksize,toi=quick_get_next_peak(toi)
        sn=pksize/np.std(toi)
        pksizes.append(pksize)
        pksize_sn.append(sn)
    return(np.array(pksizes),np.array(pksize_sn),toi)
        
    
    
    










































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































