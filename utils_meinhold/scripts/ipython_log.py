# IPython log file

get_ipython().magic(u"logstart")
import pyfits
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
az101=p10[1].data['az1'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
ps101mag=util.phasebin(3600,az101mag*np.pi/180.-np.pi,c101)
ps101=util.phasebin(3600,az101*np.pi/180.-np.pi,c101)
c10=0
p10=0
p10mag=0
c101=0
az101mag=0
az101=0
imshow(ps101)
get_ipython().magic(u"pinfo imshow")
get_ipython().magic(u"pinfo imshow")
im=imshow ps101
im=imshow(ps101)
im=imshow(ps101,interpolation=)
im=imshow(ps101,interpolation='nearest')
im.show()
im.show
figure()
show(im)
get_ipython().magic(u"pinfo im")
type(im)
im.make_image()
im.make_image()
im
show()
show(im)
show(im.make_image)
get_ipython().magic(u"pinfo fig.figimage")
get_ipython().magic(u"pinfo fig")
get_ipython().magic(u"pinfo plt.figimage")
figimage(ps101)
figure(0
)
figimage(ps101)
countour(ps101)
contour(ps101)
ps101.shape
ps101r=util.rebin(ps101,360,731)
ps101r.shape
imshow(ps101r)
contourf(ps101r)
axes()
get_ipython().magic(u"pinfo contourf")
ps101bad=where(ps101 == 0)
ps101bad[0]
ps101bad[1]
len(ps101bad[0]
)
len(ps101bad[1])
ps101.shape
ps101[ps101bad[0],ps101bad[1])
ps101[ps101bad[0],ps101bad[1]]
ps101[ps101bad[0][0],ps101bad[1][0]]
ps101[ps101bad]=ps101[ps101bad[0]+1,ps101bad[1]+1]
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0],ps101bad[1]-1]
imshow(ps101)
ps101=util.phasebin(3600,az101*np.pi/180.-np.pi,c101)
c10=pyfits.open('all_10GHz_data_cal.fits')
p10=pyfits.open('all_10ghz_pointing.fits')
p10mag=pyfits.open('all_10ghz_pointing_mag.fits')
ut10=c10['Time'].data['ut']
utstartend=[16.8 ,38.4]
c101= c10['ch1_'].data['t'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
az101mag=p10mag[1].data['az1'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
az101=p10[1].data['az1'][(ut10 > utstartend[0]) & (ut10 < utstartend[1])]
ps101mag=util.phasebin(3600,az101mag*np.pi/180.-np.pi,c101)
ps101=util.phasebin(3600,az101*np.pi/180.-np.pi,c101)
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0],ps101bad[1]-1]
imshow(ps101)
ps101=util.phasebin(3600,az101*np.pi/180.-np.pi,c101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101bad=where(ps101 == 0)
ps101[ps101bad]=ps101[ps101bad[0]-1,ps101bad[1]]
imshow(ps101)
ps101magbad=where(ps101mag == 0)
figure()
imshow(ps101mag)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0]-1,ps101magbad[1]]
imshow(ps101mag)
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0]-1,ps101magbad[1]]
imshow(ps101mag)
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
imshow(ps101mag)
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
imshow(ps101mag)
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
ps101magbad=where(ps101mag == 0)
imshow(ps101mag)
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
imshow(ps101mag)
ps101magbad=where(ps101mag == 0)
ps101mag[ps101magbad]=ps101mag[ps101magbad[0],ps101magbad[1]-1]
imshow(ps101mag)
imshow(ps101mag,vmax=100)
figure()
plot(ps101mag[:,50])
get_ipython().magic(u"pinfo c_corr")
get_ipython().magic(u"pinfo correlate")
get_ipython().magic(u"pinfo np.corrcoef")
np.correlate()
get_ipython().magic(u"pinfo np.correlate")
get_ipython().magic(u"pinfo convolve")
test=correlate(ps101mag[:,50],ps101mag[:55])
test=correlate(ps101mag[:,50].flatten(),ps101mag[:55].flatten())
test.shape
plot(test)
figure()
plot(test)
plot(ps101mag[:,50].flatten())
ps101mag.shape
plot(ps101mag[:,50])
hold(False)
plot(ps101mag[:,50])
test=correlate(ps101mag[:,50],ps101mag[:55])
test=correlate(ps101mag[:,50],ps101mag[:55],mode='Full')
test=correlate(ps101mag[:,50],ps101mag[:55],mode='valid')
test=correlate(ps101mag[:,50],ps101mag[:55],mode='Valid')
plot(ps101mag[:,50])
plot(ps101mag[:,50].flatten())
test=correlate(ps101mag[:,50].flatten(),ps101mag[:55].flatten())
plot(test)
len(ps101mag[:,50])
len(ps101mag[:,50].flatten())
a=ps101mag[:,50].flatten()
b=ps101mag[:,55].flatten()
plot(a)
hold(True)
plot(b)
test=correlate(a,b)
test.shape
test.shape()
test.shape()[0]
test[0]
get_ipython().magic(u"pinfo xcorr")
test=xcorr(a,b,maxlags=20)
test.shape
test.shape()
plot(test[0],test[1])
figure()
plot(test[0],test[1])
b=ps101mag[:,65].flatten()
test=xcorr(a,b,maxlags=20)
plot(test[0],test[1])
b=ps101mag[:,85].flatten()
test=xcorr(a,b,maxlags=20)
plot(test[0],test[1])
b=ps101mag[:,125].flatten()
test=xcorr(a,b,maxlags=20)
plot(test[0],test[1])
b=ps101mag[:,115].flatten()
test=xcorr(a,b,maxlags=20)
plot(test[0],test[1])
test=xcorr(ps101mag[:,0],ps101mag[:,1],maxlags=20)
figure()
plot(test[0],test[1])
figure(5)
hold(False)
plot(ps101mag[:,0])
plot(ps101mag[:,1])
hold(True)
plot(ps101mag[:,0])
figure(5)
plot(ps101mag[:,0])
plot(roll(ps101mag[:,1],5,axis=0))
plot(roll(ps101mag[:,1],0,axis=0))
plot(ps101mag[:,1])
plot(ps101mag[:,1])
plot(roll(ps101mag[:,1],4,axis=0))
figure(50
)
figure(5)
plot(roll(ps101mag[:,1],4,axis=0))
s=ps101mag.shape()
s=ps101mag.shape
s[0]
s[1]
ps101mag.shape[1]
ps=copy(ps101mag)
ps[0,0]
ps[0,0]=1
ps[0,0]
ps101mag[0,0]
ps.shape
ps=copy(ps101mag)
#now set up to get cross correlations one row at at time
nrows=ps.shape[1]
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:i+1],maxlags=15)
        lag=cc[cc[1]=np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
nrows=ps.shape[1]
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:i+1],maxlags=15)
        lag=cc[cc[1]=np.max(np.abs(cc[1]))][0]]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:i+1],maxlags=15)
        lag=cc[cc[1]==np.max(np.abs(cc[1]))][0]]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:i+1],maxlags=15)
        lag=cc[cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:i+1],maxlags=15)
        lag=cc[cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
ps.sape
ps.shzpe
ps.shape
nrows
nrows=ps.shape[1]
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:,i+1],maxlags=15)
        lag=cc[cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
i=1
cc=xcorr(ps[:,i],ps[:,i+1],maxlags=15)
np.max(np.abs(cc[1]))
cc[cc[1]==np.max(np.abs(cc[1]))]
cc[1]==np.max(np.abs(cc[1]))
cc[0][cc[1]==np.max(np.abs(cc[1]))]
cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
cc[0][cc[1]==np.max(np.abs(cc[1]))][1]
cc[0]
cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:,i+1],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
nrows=ps.shape[1]-1
for i in range(nrows):
        cc=xcorr(ps[:,i],ps[:,i+1],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
imshow(ps)
figure()
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
ps=copy(ps101mag)
nrows=ps.shape[1]-1
for i in range(nrows):
        cc=xcorr(ps[1700:1850,i],ps[1700:1850,i+1],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
figure(6)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
ps=copy(ps101mag)
nrows=ps.shape[1]-1
for i in range(nrows):
        cc=xcorr(ps[1700:1850,i],ps[1700:1850,i+1],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        ps[:,i+1]=np.roll(ps[:,i+1],-lag,axis=0)
        
figure(6)
imshow(ps101mag)
imshow(ps)
for i in range(50):
        cc=xcorr(ps[1700:1850,i],ps[1700:1850,i+1],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        print i,lag
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
imshow(ps)
imshow(ps101mag)
ps=copy(ps101mag)
nrows=ps.shape[1]-1
for i in range(nrows):
        cc=xcorr(ps[1700:1850,i],ps[1700:1850,i+1],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        print i,lag
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
imshow(ps)
imshow(ps101mag)
ps=copy(ps101mag)
#now set up to get cross correlations one row at at time
nrows=ps.shape[1]-1
for i in range(nrows):
        cc=xcorr(ps[1700:1850,50],ps[1700:1850,i],maxlags=15)
        lag=cc[0][cc[1]==np.max(np.abs(cc[1]))][0]
        print i,lag
        ps[:,i+1]=np.roll(ps[:,i+1],lag,axis=0)
        
figure(6)
imshow(ps)
c10
c10=0
p10=0
imshow(ps)
get_ipython().magic(u"whos ")
a=0
az101=0
az101mag=0
b=0
c101=0
ut10=0
imshow(ps101mag)
