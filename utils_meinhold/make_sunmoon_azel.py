#   script to produce moon and sun az an el synchronized to 10 and 15 GHz pointing files

import cofe_util as util
import pyfits
import numpy as np
import cPickle

#start with 10 GHz
# open up the data and pointing files


s10=pyfits.open('c:/cofe/flight_data/Level1/1.1/all_10GHz_servo.fits')
ut10=s10['TIME'].data['UT']
lat=s10['gyro_hid'].data['hybridlatitude']
lon=s10['gyro_hid'].data['hybridlongitude']
s10.close()
ndata =len(ut10)
lat=np.zeros(ndata,dtype=np.float32)+0.596
lon=np.zeros(ndata,dtype=np.float32)-1.8179
azsun,elsun=util.get_cofe_target(ut10,lat,lon,'Sun')
azmoon,elmoon=util.get_cofe_target(ut10,lat,lon,'Moon')
azsun=azsun*180./np.pi
elsun=elsun*180./np.pi
azmoon=azmoon*180./np.pi
elmoon=elmoon*180./np.pi
sun=[azsun,elsun]
moon=[azmoon,elmoon]
sunfile10=open('c:/cofe/flight_data/Level1/1.1/sunazel10ghz.pkl','wb')
cPickle.dump(sun,sunfile10)
sunfile10.close()
moonfile10=open('c:/cofe/flight_data/Level1/1.1/moonazel10ghz.pkl','wb')
cPickle.dump(moon,moonfile10)
moonfile10.close()

s15=pyfits.open('c:/cofe/flight_data/Level1/1.1/all_15GHz_servo.fits')
ut15=s15['TIME'].data['UT']
lat=s15['gyro_hid'].data['hybridlatitude']
lon=s15['gyro_hid'].data['hybridlongitude']
s15.close()
ndata =len(ut15)
lat=np.zeros(ndata,dtype=np.float32)+0.596
lon=np.zeros(ndata,dtype=np.float32)-1.8179
azsun,elsun=util.get_cofe_target(ut15,lat,lon,'Sun')
azmoon,elmoon=util.get_cofe_target(ut15,lat,lon,'Moon')
azsun=azsun*180./np.pi
elsun=elsun*180./np.pi
azmoon=azmoon*180./np.pi
elmoon=elmoon*180./np.pi
sun=[azsun,elsun]
moon=[azmoon,elmoon]
sunfile15=open('c:/cofe/flight_data/Level1/1.1/sunazel15ghz.pkl','wb')
cPickle.dump(sun,sunfile15)
sunfile15.close()
moonfile15=open('c:/cofe/flight_data/Level1/1.1/moonazel15ghz.pkl','wb')
cPickle.dump(moon,moonfile15)
moonfile15.close()