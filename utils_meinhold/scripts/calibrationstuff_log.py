# IPython log file

get_ipython().magic(u"cd ..")
get_ipython().magic(u"cd 0.5")
import pyfits
import cofe_util as util
import toitools as toi
s15=pyfits.open('all_15GHz_v0.5_servo.fits')
s15.info()
s15[GYRO_HID].columns
s15['GYRO_HID'].columns
dir 
get_ipython().system(u"dir /on ")
get_ipython().magic(u"cd ..")
get_ipython().magic(u"cd ..")
get_ipython().system(u"dir /on ")
get_ipython().system(u"dir /on 10GHz/")
get_ipython().system(u"dir /on 10GHz")
get_ipython().system(u"dir /on 10GHz/20110917")
get_ipython().system(ur"dir /on 10GHz\20110917")
import glob
fl=glob.glob('10GHz\20110917\*.dat')
fl[100]
fl10_17=glob.glob('10GHz\20110917\*.dat')
fl10_17[740]
fl10_17
get_ipython().system(u"dir /on ")
fl10_17=glob.glob('10GHz/20110917/*.dat')
fl10_17
fl10_17[740]
calstarts=util.find_command_uts('0050')
calstops=util.find_command_uts('0051')
calstarts
cal3=demod.read_raw_data(filenames=fl10_17[730:755])
import demod
cal3=demod.read_raw_data(filenames=fl10_17[730:755])
cal3
cal3.info
plot(cal3[)
plot(cal3['rev'],cal3['ch1'])
cal3off=arange(500)+10000
cal3on=arange(500)+11000
t1=cal3['ch1'][cal3off]
t1.shape
t1r=rebin(t1,(1,256))
t1r=util.rebin(t1,(1,256))
t1r
t1r.shape
t1r=util.rebin(t1,(256))
t1r=util.rebin(t1,(256,1))
t1.shape\
t1.shape
t1.shape
t1r=util.rebin(transpose(t1),(1,256))
t1r=util.rebin(transpose(t1),(256,1))
t1r.shape
t1r=util.rebin(transpose(t1),(500,1))
t1r=util.rebin(t1,(500,1))
t1r.shape
reload(util)
t1r=util.rebin(t1,(1,2576))
t1r=util.rebin(t1,(1,256))
reload(util)
t1r=util.rebin(t1,(500,1))
figure()
plot(t1r)
t1r.shape
plot(t1r[0,])
t1.shape
plot(t1[0,])
for i in range(500):
    plot(t1[i,])
    
plot(t1[0,],linethickness=30)
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,])
plot(t1r[0,],'+')
reload(util)
t1r=util.rebin(t1,(1,256))
t1r.shape
t1r=util.rebin(t1,(256))
t1r.shape
t1r.shape.flatten()
t1r.flatten()
t1r.shape
t1rr=t1r.flatten()
t1rr.shape
plot(t1r)
plot(t1rr)
t1r=util.rebin(t1,(2,256))
t1r.shape
t1rr=t1r.flatten()
t1rr.shape
reload(util)
t1r=util.rebin(t1,(2,256))
reload(util)
t1r=util.rebin(t1,(2,256))
reload(util)
t1r=util.rebin(t1,(2,256))
reload(util)
t1r=util.rebin(t1,(2,256))
t1r.shape
t1r=util.rebin(t1,(1,256))
t1r.shape
t1=
t1=cal3['ch1'][cal3off]
t2=cal3['ch1'][cal3on]
figure()
plot(rebin(t1,(1,256))-mean(t1))
plot(util.rebin(t1,(1,256))-mean(t1))
plot(util.rebin(t2,(1,256))-mean(t2))
plot(util.rebin(t2,(1,256))-mean(t2))
t2r=util.rebin(t2,(1,256))-mean(t2)
t1r=util.rebin(t1,(1,256))-mean(t1)
reload(util)
fp=toi.linfit(t1r,t2r)
fp
hold(False)
plot(t1r)
hold(True)
plot(t2r)
plot(t1r*fp[1])
get_ipython().magic(u"pwd ")
get_ipython().magic(u"pinfo %logstart")
get_ipython().magic(u"logstart calibrationstuff_log.py")
exit()
