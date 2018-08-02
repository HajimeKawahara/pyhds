#!/usr/bin/env python
from astropy.io import fits
import sys
from pyraf import iraf
import os
import glob

#os.remove()

#(A) overscan
ovold=glob.glob("ov*.fits")
if len(ovold)>0:
    print("-(A) ov exists. Skip the overscan correction.")
#    print ovold
else:
    print("(A) overscan correction")
    iraf.overscan(inimage='@raw.list',outimage='@ov.list')

#(B)
nlold=glob.glob("nl*.fits")
if len(nlold)>0:
    print("-(B) nl exists. Skip the linearity correction.")
#    print nlold
else:
    print("(B) linearity correction")
    iraf.hdslinear(inimage='@ov.list',outimage='@nl.list',auto_b="yes")

#(C1)
biasold=glob.glob("bias.fits")
if len(biasold)>0:
    print("-(C1) bias.fits exists. Skip to make the master bias.")
else:
    print("(C1) make the master bias (bias.fits)")
    iraf.imcombine(input='@bias.list',output='bias.fits',combine="median")

#(C2)
bold=glob.glob("b*.fits")
if len(bold)>1:
    print("-(C2) b exists. Skip the bias correction.")
else:
    print("(C2) the bias correction")
    iraf.imarith(operand1='@nl.list',op="-",operand2='bias.fits',result="@b.list")

#(E1)
f=glob.glob("flat.fits")
if len(f)>0:
    print("-(E1) flat.fits exists. Skip creation of unnormalized master flat (flats.fits).")
else:
    print("(E1) the unnormalized master flat (flats.fits)")
    iraf.imcombine(input='@flat.list',output='flat.fits',combine="median")



fn=glob.glob("f*.fits")
fnc=glob.glob("flat*.fits")

if len(fn)-len(fnc)>0:
    print("-(E3) f exists. Skip the flat correction.")
elif os.path.exists("flatn.fits"):
    print("(E3) the flat correction b/flatn.fits")
    iraf.imarith(operand1='@b.list',op="/",operand2='flatn.fits',result="@f.list")
else:
    print("-(E3) flatn.fits does not exist. Perform (E2) process before (E3).")
