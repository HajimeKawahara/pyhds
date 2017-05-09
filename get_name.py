#!/usr/bin/python
from astropy.io import fits
import sys
argvs = sys.argv
file=argvs[1]
print file
hduread=fits.open(file)
name=hduread[0].header["Object"]
obs=hduread[0].header["Observer"]
expt=hduread[0].header["EXPTIME"]
wavmax=hduread[0].header["WAV-MAX"]
wavmin=hduread[0].header["WAV-MIN"]
ax1=hduread[0].header["NAXIS1"]
ax2=hduread[0].header["NAXIS2"]

print name
print obs
print expt
print wavmax, wavmin
print ax1,ax2

#print hduread[0].header.ascardlist()
