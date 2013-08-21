#get the moon crossings for COFE 10 GHz roof data from august 2nd
#pointing and science data were already combined in  combineda2

import cofe_util as util

ut=combineda2['sci_data']['ut'][542800:543600]
gaz=radians(combineda2['az'][542800:543600])
centerut=14.5118
azoffch3,moonazch3,moonelch3,fitutch3=util.get_cofe_crossing(ut,-toi,gaz,lat,longi,centerut,'Moon')
print azoffch3,moonazch3,moonelch3,fitutch3
# 192.082635101 326.807940765 55.5271839898 14.5117592593
eloffch3=moonelch3-mean(combineda2['el'][542800:543600])
eloffch3
# -3.1738160102228861

#so true az for ch3 = reported az+192.0826 degrees
#and true el for ch3= reported el-3.1738  degrees
#Now do ch1
gaz=radians(combineda2['az'][525150:525350])
ut=combineda2['sci_data']['ut'][525150:525350]
lat=resize(lat,len(ut))
longi=resize(longi,len(ut))
centerut=14.3217
azoffch1,moonazch1,moonelch1,fitutch1=util.get_cofe_crossing(ut,-toi,gaz,lat,longi,centerut,'Moon')
print azoffch1,moonazch1,moonelch1,fitutch1
# 198.781031036 324.008656036 53.0092484126 14.3216872428
eloffch1=moonelch1-mean(combineda2['el'][525150:525350])
eloffch1
# -5.6917515873690405
