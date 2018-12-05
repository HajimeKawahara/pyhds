#!/usr/bin/env python
from astropy.io import fits
import sys
from pyraf import iraf
import os
import glob
import argparse
import numpy as np
import file_type as ft

parser = argparse.ArgumentParser(description='hdsis_ecf for all files having the specified type. Set other parameters by [epar hdsis_ecf] in iraf')
parser.add_argument('-f', nargs="+", required=True, help='fits')
parser.add_argument('-b', nargs=1, required=True, help='Type (obj,comp,flat)')
parser.add_argument('-r', nargs=1, required=True, help='reference aperture (e.g. b05883)')

####CHECK THESE VALUES##
plotyn="no"    #plot
apflat="flatn" #ref_ap
#IS2
#lower="-11"    #st_x
#upper="6"      #ed_x
#IS3
lower="-11"    #st_x
upper="9"      #ed_x
#lower="-15"    #st_x
#upper="14"      #ed_x

#badf="none"  #badfix
badf="fixpix"  #badfix

########################

args = parser.parse_args()    
fitstype=args.b[0]
ref=args.r[0]

obs,bias,comp,flat,expflat,expbias,obsname,flatt=ft.checktype(args.f)

print "Do hdsis_ecf for ",fitstype 
print "REFERENCE = ", ref
print "Applying to ",obs

iraf.imred()
iraf.eche()
#sys.exit("--")

if fitstype == "obj":
    for i in range(0, len(obs)):
        iraf.hdsis_ecf(inimg=obs[i],outimg="a"+obs[i],plot=plotyn,st_x=lower,ed_x=upper,flatimg=apflat,ref_ap=ref, badfix=badf)

elif fitstype == "comp":
    for i in range(0, len(comp)):
        iraf.hdsis_ecf(inimg=comp[i],outimg="a"+comp[i],plot=plotyn,st_x=lower,ed_x=upper,flatimg=apflat,ref_ap=ref, badfix=badf)
elif fitstype == "flat":
    for i in range(0, len(flat)):
        iraf.hdsis_ecf(inimg=flat[i],outimg="a"+flat[i],plot=plotyn,st_x=lower,ed_x=upper,flatimg=apflat,ref_ap=ref, badfix=badf)
else:
    print "No type."


