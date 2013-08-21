#script to add bad sections (hand selected) to flags

ft=open('baduts_for_flags_based_on_10Ghz_ch0.pkl','rb')
rawlist=cPickle.load(ft)
starts=np.array(rawlist[0])
stops=np.array(rawlist[1])

f10=pyfits.open('../../v6_flags10ghz.fits',mode='update')
f15=pyfits.open('../../v6_flags15ghz.fits',mode='update')
chans15=[1,3,5,9,11,13]
chans10=[1,3,5]
ut10=f10['time'].data['ut']
ut15=f15['time'].data['ut']
for sta,sto in zip(starts,stops):
    h15=where((ut15>sta) & (ut15 < sto))
    for chan in chans15
        flags15=f15[chan].data['FLAGS']
    
    
f10.flush()
p10.close()
