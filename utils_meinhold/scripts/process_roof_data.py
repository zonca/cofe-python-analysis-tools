#script to combine pointing and science data for COFE from
#broida roof measurements
#saves combined file as well as one with phasebin subtracted from each channel to remove
# an azimuth template (first order subtraction of sidelobe effects))

import sys
sys.path.append('/smbmount/labuse/software_github_repos/cofe-python-analysis-tools/utils_meinhold/')
sys.path.append('/smbmount/labuse/software_github_repos/cofe-python-analysis-tools/utils_zonca/')
import cPickle
from glob import glob
import cofe_util as cu
import realtime as rt

yrmoday=string(sys.arg[1])
cdata=rt.getdatanow(yrmoday)

chans=[]
for i in range(6):
    chans.append('ch'+string(i))
for chan in chans:
    for mode in ['T','Q','U']:
        psmap=cu.phasebin(360,cdata['az'],cdata['sci_data'][chan][mode],degrees=True)
        template=mean(psmap,axis=1)
        alltemplate=np.interp(cdata['az'],arange(360),template
        cdata['sci_data'][chan][mode]=cdata['sci_data'][chan][mode]-alltemplate

cPickle.dump(cdata,open('combined_data_'+yrmoday+'_sub.pkl','w'),protocol=-1)
