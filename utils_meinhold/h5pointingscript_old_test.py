"""
script to synchronize h5py az, el, time (rev) files with acq_tel data
"""
#first step, read the files

def get_h5_pointing(filelist,startrev=None, stoprev=None,angles_in_ints=True):
    
    #filelist is complete path list to the h5 files
    elconversion=-360./40000.
    azconversion=-360./(2.**16)
    eloffset=290. #just a guess right now
    hpointing=[]
    filelist.sort()
    for f in filelist:
        h=h5py.File(f)
        hpointing.append(h['data'][:])
    
    hpointing = np.concatenate(hpointing)
    #cut out blank lines from unfilled files
    hpointing = hpointing[hpointing['time'] > 0]
    if startrev != None:
        hpointing=hpointing[hpointing['time'] > startrev]
    if stoprev != None:
        hpointing=hpointing[hpointing['time'] < stoprev]

    hrevlist=np.unique(hpointing['time'])
    elmeans=[]
    azmeans=[]

    for rev in hrevlist:
        test=hpointing[hpointing['time'] == rev]
        els=np.std(test['el'])
        azs=np.std(test['az'])
        if ((els > 5) and len(test) > 3):
            if ((np.max(test['el'] ) - np.mean(test['el'])) > 10 ):
                test = test[test['el'] < np.max(test['el'])]
            if ((np.mean(test['el']) - np.min(test['el'])) > 10 ):
                test = test[test['el'] > np.min(test['el'])]
        els=np.std(test['el'])
        azs=np.std(test['az'])
        if ((els > 5) and len(test) > 2):
            if ((np.max(test['el'] ) - np.mean(test['el'])) > 10 ):
                test = test[test['el'] < np.max(test['el'])]
            if ((np.mean(test['el']) - np.min(test['el'])) > 10 ):
                test = test[test['el'] > np.min(test['el'])]

        elmeans.append(np.mean(test['el']))
        azmeans.append(np.mean(test['az']))
    elmeans=np.array(elmeans)
    azmeans=np.array(azmeans)
    if angles_in_ints==True:
        elmeans=elmeans*elconversion+eloffset
        azmeans=azmeans*azconversion
     
    return {'el':elmeans,'az':azmeans,'rev':hrevlist}

