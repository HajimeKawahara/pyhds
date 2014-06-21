#!/usr/bin/python
from astropy.io import fits
import sys
argvs = sys.argv

flat=[]
expflat=[]
comp=[]
bias=[]
expbias=[]
obs=[]
obsname=[]
for i in range(1,len(argvs)):
    file=argvs[i]
    hduread=fits.open(file)
    name=hduread[0].header["Object"]
    expt=hduread[0].header["EXPTIME"]

    if name=="FLAT":
        flat.append(file)
        expflat.append(expt)
    elif name=="COMPARISON":
        comp.append(file)        
    elif name=="BIAS":
        bias.append(file)
        expbias.append(expt)
    else:
        obs.append(file)
        obsname.append(name)
print str(len(flat))+" FLAT files found:"
print flat
print "EXPOSURE TIME="
print expflat
print ''
print str(len(bias))+" BIAS files found:"
print bias
print "EXPOSURE TIME="
print expbias
print ''
print str(len(comp))+" COMPARISON files found:"
print comp
print ''
print str(len(obs))+" OBJECTS files found:"
print obs
print "OBJECT NAME="
print obsname


