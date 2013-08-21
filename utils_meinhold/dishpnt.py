# Revisions:
# 2003-04-29 MPW Wrong message instead of "Satellite is vertically overhead."
# 2002-12-20 MPW Fix YesNo test before resaving parameters
#                Make tests for file errors more comprehensive
#                Make sure YesNo returns a 1-character string
#                Fix serious bug in altitude calculation
#                Show bearing in the range 0..360, not -180..180
#                Deprecate `Spacebar` routine,
#                since the Python version required the enter key;
#                replace use with `raw_input` call

#Path: nnrp1.uunet.ca!news.uunet.ca!nf3.bellglobal.com!sjc70.webusenet.com!news.webusenet.com!newsfeed2.earthlink.net!newsfeed.earthlink.net!stamper.news.pas.earthlink.net!stamper.news.atl.earthlink.net!harp.news.atl.earthlink.net!rime.news!RGXMod.BBSWORL
#D.News.Gateway!rime.news!rime.nethub!RIMEGateQWK.MoonDog.BBS
#From: rmoderator@rime.org (david williams)
#Newsgroups: comp.programming
#Subject: satellite-dish pointer pr
#Date: 12 Dec 2002 15:50:00 -0400
#Organization: RelayNet(tm), Brooklyn, NY (718) 692-2498
#Lines: 358
#Distribution: World
#Message-ID: <1227117665.522.239.8900510.1214819386.RIMEGateQWK@MoonDog.BBS>
#Reply-To: rmoderator@rime.org (david williams:comp.programming)
#NNTP-Posting-Host: d8.87.84.75
#X-Server-Date: 13 Dec 2002 02:18:03 GMT
#X-Newsreader: PCBoard Version 15.4
#X-Mailer: RIMEGate(tm)
#X-Process: RIMEGateQWK
#X-Original-NNTP-Posting-Host: 209.166.49.226
#X-Original-Trace: 12 Dec 2002 21:08:27 +1000, 209.166.49.226
#Xref: news.uunet.ca comp.programming:171642
#X-Received-Date: Thu, 12 Dec 2002 21:18:04 EST (nnrp1.uunet.ca)
#
#
#
#About 20 years ago, I wrote a program in BASIC that calculated the
#direction (compass bearing and angle of elevation) in which a satellite
#dish should be pointed in order to receive signals from any
#geostationary satellite, given the latitude and longitude of the
#receiving point on the earth and the longitude of the satellite on the
#geostationary orbit. The program worked just fine, and some people made
#use of it. However, there were few dishes back then.
#
#Much more recently, with the proliferation of dishes, I have seen
#people asking for this sort of program. So I dug out my old code and
#updated it somewhat, from the original Commodore BASIC to QBasic.
#
#But all BASICs are now somewhat dated, so to be really useful the
#program should probably be translated into other languages. This
#shouldn't be difficult. The algorithm is straightforward, involving no
#trickery. But... I'm not really familiar with any "modern" languages.
#So the translation(s) should probably be done by somebody else.
#
#If anyome feels like taking this on, please do so! The QBasic code is
#below. It's all public-domain stuff, written by myself. Distribute it
#however you want.
#
#Have fun!
#
#                           dow
#
#------------------------------------------------------
#
#' TV_SATS.BAS
#' TV Satellites, Commodore PET version, David Williams, 1982
#
#' david.williams@ablelink.org
#
#' Updated for other computers 1995, 2000, 2002
#' This version dated 2002 Nov. 22
# Python version by Mel Wilson, Dec. 13, 2002

import math, sys

# Subroutines moved to here from the end of the BASIC code
#
def InNum (prompt, v, mx):
    while 1:
        inp = raw_input (prompt + " (or ENTER for no change)?")
        print
        if inp == "\n":
            print "Value unchanged (%.3g)" % v
            print
            return v

        try:
            w = float (inp)
            if abs (w) >= mx:
                raise ValueError
            return w

        except ValueError:
            print "\aInput illegal or out of range (-%g to %g)" % (mx, mx)
            print "Try again ..."
            print
# end InNum


def Instructions():
    print "This program calculates the position in the sky, as true"
    print "compass bearing and altitude (or angle of elevation), of"
    print "any satellite that is in geostationary orbit. (Almost all"
    print "T.V. broadcasting and relay satellites are geostationary.)"
    print
    print "You will be asked for your latitude and longitude, and for"
    print "the longitude of the satellite. Enter these quantities, in"
    print "degrees, accurate to at least one place of decimals (0.1"
    print "degree) if possible. Errors greater than 0.1 degree will"
    print "cause significantly inaccurate calculated results. It is"
    print "a good idea to use a G.P.S. receiver to find your own"
    print "latitude and longitude."
    print
    print "Note that the bearings are true. If you want a magnetic"
    print "bearing, look up the local magnetic deviation. To find"
    print "the magnetic bearing, add the deviation to the true"
    print "bearing if magnetic north is west of true north. Subtract"
    print "the deviation if magnetic north is east of true north."
    print
    print "Your entries of latitude and longitudes can be kept on disk"
    print "and used in subsequent runs. Initially, arbitary defaults"
    print "are used."
    raw_input ('Press Enter to continue.')  ## 2002-12-20 MPW
# end Instructions


def signum (n):
    "Return the sign value of n as -1, 0 or 1 for negative, zero or positive n"
    if n < 0:
        return -1
    if n == 0:
        return 0
    return 1
# end signum


def YesNo (prompt=''):
    "Prompt the user and wait for a response of 'y' or 'n'"
    while 1:
        g = raw_input (prompt + '? (y/n)').strip().lower()
        if g  and  g[0] in 'yn':    ## 2002-12-20 MPW
            return g[0]
# end YesNo


# Mainline code resumes here..

R = 6.615   # Radius of geosynchronous orbit in units of earth radius
PI = math.pi
PIby2 = PI / 2.0
CF = PI / 180   # Degree/radian factor

paramfilename = "TVSATDAT.DAT"
try:
    infile = open (paramfilename, "rt")
    FA, FO, FS = map (float, infile.readline().split())
    infile.close()
except IOError:
    FA, FO, FS = 45, 80, 90     # Default latitude & longitudes, used if file not found

LA, LO, LS = FA, FO, FS

if YesNo ("Do you want instructions") == 'y':
    Instructions()

#Newcalc:
while 1:    # Newcalc .. to perform each new calculation ..

    #' Input section
    print "For your current position on the ground:"
    print "Latitude is %.2g degrees north." % LA
    print "Longitude is %.3g degrees west." % LO
    print
    if YesNo ("Keep these values") == 'n':
        print "Input latitude and longitude in degrees."
        print "Use negative numbers for angles in"
        print "opposite directions to those shown."
        LA = InNum ("Your latitude (deg. north)", LA, 90 )
        LO = InNum ("Your longitude (deg. west)", LO, 180 )

    LT = LA
    LG = LO

    print "For current satellite:"
    print "Longitude is %.2g degrees west." % LS
    print
    if YesNo ("Keep this value") == 'n':
        print "Input longitued of satellite in"
        print "degrees west. (Use negative number"
        print "if you want to input degrees east.)"
        LS = InNum ("Satellite's longitude", LS, 180)

    LD = (LG - LS) * CF # longitude difference in radians
    LT = (90 + LT) * CF # latitude from s. pole in radians

    #' satellite's x,y,z coordinates
    Y = 0       # equatorial orbit
    X = R * math.sin (LD)
    Z = R * math.cos (LD)


    #' rotate system to put observer at s. pole
    D = abs(Z)  # distance from x-axis
    AN = signum (Z) * PIby2
    # azimuth angle onto y-z plane (y-axis as zero)
    AN += LT    # rotate system
    Y = D * math.cos (AN)   # new y
    Z = D * math.sin (AN)   # new z

    if Y > -1:
        print "Satellite is invisible (below horizon)."

    else:
        if X == 0  and  Z == 0:
            AL = PIby2
        else:
            AL = math.atan ((-1-Y) / math.hypot (X, Z)) ## 2002-12-20 MPW
        AL /= CF    # alt. in degrees
        A = "%.1f" % AL

        if 89.9 < AL < 90.1:
            print "Satellite is vertically overhead."   ## 2003-04-29 MPW
            print "(Altitude is 90.0 degrees.)"

        else:
            # calculate new bearing
            if Z == 0:
                BE = signum (X) * PIby2
            else:
                BE = math.atan (X / Z)
                if Z < 0:
                    BE += PI
            BE /= CF    # bearing in degrees

            #' roundoff and printout
            BE = math.fmod (BE, 360.0)
            if BE < 0:          ## 2002-12-20 MPW
                BE += 360.0     ## 2002-12-20 MPW
            print "Satellite's position:"
            print
            BE = round (BE, 1)
            print "Bearing is %.1f degrees." % BE

            X = BE / 90
            if X == int (X):
                Y1 = ['North', 'East', 'South', 'West'][int(X)]
                print "(Due", Y1, ")"
            else:
                Z = abs (180-BE)
                if Z < 90:
                    Y1 = "South"
                else:
                    Y1 = "North"
                    Z = 180 - Z
                if X < 2:
                    Y2 = 'East'
                else:
                    Y2 = 'West'
                print "(%s, %.1f degrees %s)" % (Y1, Z, Y2)

            print
            print "Altitude is %s degrees." % A
            if AL < 5:
                print
                print "Very low altitude - Communication unreliable"

    if YesNo ("Another calculation")  == 'n':
        break   # no more calculations

# end while 1 .. to perform each new calculation

if LA != FA  or  LO != FO  or  LS != FS:
    if YesNo ("Keep current latitude & longitudes for next run") == 'y':
        try:
            outfile = open (paramfilename, 'wt')
            outfile.write ('%g\t%g\t%g\t\n' % (LA, LO, LS))
            outfile.close()
        except IOError:
            sys.exit (1)    # Couldn't save params - exit with error code

sys.exit (0)    # normal exit


