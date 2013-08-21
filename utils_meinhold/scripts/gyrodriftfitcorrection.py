#script to generate 15 GHz pointing model
#based on the sun1, sun1 moon crossing fits
#note that the slopes from the fit were not self
#consistent. CH1 and ch9 both seem to fit all
#three points. other  suck. We make the ad hoc
#decision to use the slope of ch9 and offsets
#pegged to the moon crossings for all channels.
import cPickle
import numpy as np
wd='/cofe/flight_data/Level1/1.2/'

f=open(wd+'azoff_15.pkl','rb')
azoffdic15=cPickle.load(f)
f.close()
f=open(wd+'utcrossings_15.pkl','rb')
utcrossdic15=cPickle.load(f)
f.close()
f=open(wd+'fitparams_15.pkl','rb')
fitdic15=cPickle.load(f)
f.close()

f=open(wd+'azoff_10.pkl','rb')
azoffdic10=cPickle.load(f)
f.close()
f=open(wd+'utcrossings_10.pkl','rb')
utcrossdic10=cPickle.load(f)
f.close()
f=open(wd+'fitparams_10.pkl','rb')
fitdic10=cPickle.load(f)
f.close()


chans15=[1,3,5,9,11,13]
newfitdic15={}
for c in chans15:
 newfitdic15[c] = np.array(fitdic15[9])
 newfitdic15[c][0] = azoffdic15[c][2]-utcrossdic15[c][2]*fitdic15[9][1]
 
chans10=[1,3,5]
newfitdic10={}
for c in chans10:
 newfitdic10[c] = np.array(fitdic15[9])
 newfitdic10[c][0] = azoffdic10[c][2]-utcrossdic15[c][2]*fitdic15[9][1]

f=open(wd+'fitparams_moonfixed_15.pkl','wb')
cPickle.dump(newfitdic15,f)
f.close()

f=open(wd+'fitparams_moonfixed_10.pkl','wb')
cPickle.dump(newfitdic10,f)
f.close()


    
