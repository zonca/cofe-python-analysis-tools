#script to combine pointing and science data for COFE from
#broida roof measurements
#saves combined file as well as one with phasebin subtracted from each channel to remove
# an azimuth template (first order subtraction of sidelobe effects))

import sys
sys.path.append('/smbmount/labuse/software_github_repos/cofe-python-analysis-tools/utils_meinhold/')
sys.path.append('/smbmount/labuse/software_github_repos/cofe-python-analysis-tools/utils_zonca/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')
import cPickle
from glob import glob
import matplotlib
matplotlib.use('agg')
import cofe_util as cu
import realtime as rt
import numpy as np

yrmodays=['20130926','20130927','20130928','20130929','20130930','20131001','20131002','20131003']
for yrmoday in yrmodays:
    #yrmoday=sys.argv[1]
    cdata=rt.getdatanow(yrmoday)
    chans=[]
    for i in range(6):
        chans.append('ch'+str(i))
    for chan in chans:
        for mode in ['T','Q','U']:
            psmap=cu.phasebin(360,cdata['az'],cdata['sci_data'][chan][mode],degrees=True)
            template=np.mean(psmap,axis=1)
            alltemplate=np.interp(cdata['az'],np.arange(360),template)
            cdata['sci_data'][chan][mode]=cdata['sci_data'][chan][mode]-alltemplate

    cPickle.dump(cdata,open('combined_data_'+yrmoday+'_sub.pkl','w'),protocol=-1)
