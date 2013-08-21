def find_command_uts(command):
#script to read in cmdecho file, find lines with 
#requested command, and return adjusted UT (adjusted
#by offset to match v 0.5 level 1 files, calibration signal
# in ch a/d 1 of 15 GHz. near 16:42 UT.
    import datetime
    f=open('Q:\COFE\\Flight-2011-Fort-Sumner\\Flight\\FlightData\\CIP_commanding\\623nmisc\\cmdecho.dat')
    timelist=[]
   
    for line in f:
        linelist=line.split("\t")
        linedate=datetime.datetime.strptime(linelist[0]+' '+linelist[1],'%m/%d/%Y %H:%M:%S')
        addr=linelist[2]
        cmd=(linelist[3].strip('\n'))
        if ((cmd == command) and (addr == '0006')):
            print 'found one'
            #utadjusted=24*(linedate.day-17.)+linedate.hour+linedate.minute/60.+linedate.second/3600.
            #timelist.append(utadjusted)
            timelist.append((linedate.day,linedate.hour,linedate.minute,linedate.second))
    return timelist
    f.close()
