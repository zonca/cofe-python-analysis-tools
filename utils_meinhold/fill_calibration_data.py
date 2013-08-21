cal10ghz={}

calstarts=util.find_command_uts('0050')
calstops=util.find_command_uts('0051')
cal3_10ghz_files=['12273400.dat', '12280400.dat', '12283500.dat', '12290600.dat', '12293600.dat']
cal3_10ghz_hitoff1=range(500)
cal3_10ghz_hiton=range(500)+1100
cal3_10ghz_hitoff2=range(500)+3000
cal3=demod.read_raw_data(filenames=cal3_10ghz_files)
chans10ghz=['ch1','ch3','ch5']
cals=['cal1','cal2','cal3','cal4','cal5','cal6']
calstates=['off1','on','off2']
cal_losses=['off1/on','off2/on']
#build a nested dictionary for the calibration information


hits1={}
hits1['off1']=arange(500)+3000
hits1['on']=arange(500)+5000
hits1['off2']=arange(500)+9000

for cal in cals:
    cal10ghz[cal]={}
    for state in calstates:
        cal10ghz[cal][state]={}

cal10ghz['cal3']

cal1=demod.read_raw_data(filenames=cal10ghz['cal1']['files'])


fl15=glob.glob("15gHz/20110917/*.dat")
fl10=glob.glob("10gHz/20110917/*.dat")

cal15ghz['cal1']['files']=fl15[109:118]
cal15ghz['cal2']['files']=fl15[242:251]
cal15ghz['cal3']['files']=fl15[533:539]
cal15ghz['cal4']['files']=fl15[815:828]
cal15ghz['cal5']['files']=fl15[1348:1356]

cal10ghz['cal1']['files']=fl10[225:235]
cal10ghz['cal2']['files']=fl10[429:437]
cal10ghz['cal3']['files']=fl10[740:745]
cal10ghz['cal4']['files']=fl10[1045:1058]
cal10ghz['cal5']['files']=fl10[1594:1601]


for chan in chans10ghz:
    for state in calstates:
            cal10ghz['cal1'][state][chan]=util.rebin(cal1[chan][hits1[state]],(1,256))
            
for chan in chans10ghz:
    for state in calstates:
            cal10ghz['cal2'][state][chan]=util.rebin(cal2[chan][hits2[state]],(1,256))
            
for chan in chans10ghz:
    for state in calstates:
            cal10ghz['cal3'][state][chan]=util.rebin(cal3[chan][hits3[state]],(1,256))
            
for chan in chans10ghz:
    for state in calstates:
            cal10ghz['cal4'][state][chan]=util.rebin(cal4[chan][hits4[state]],(1,256))

for chan in chans10ghz:
    for state in calstates:
            cal10ghz['cal5'][state][chan]=util.rebin(cal5[chan][hits5[state]],(1,256))


for chan in chans15ghz:
    for state in calstates:
            cal15ghz['cal1'][state][chan]=util.rebin(cal1a[chan][hits1a[state]],(1,256))
            
for chan in chans15ghz:
    for state in calstates:
            cal15ghz['cal2'][state][chan]=util.rebin(cal2a[chan][hits2a[state]],(1,256))
            
for chan in chans15ghz:
    for state in calstates:
            cal15ghz['cal3'][state][chan]=util.rebin(cal3a[chan][hits3a[state]],(1,256))
            
for chan in chans15ghz:
    for state in calstates:
            cal15ghz['cal4'][state][chan]=util.rebin(cal4a[chan][hits4a[state]],(1,256))

for chan in chans15ghz:
    for state in calstates:
            cal15ghz['cal5'][state][chan]=util.rebin(cal5a[chan][hits5a[state]],(1,256))
