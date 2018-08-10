#!/usr/bin/env python
from astropy.io import fits
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='Make lists for HDS analysis')
parser.add_argument('-f', nargs="+", required=True, help='HDSA fits')
parser.add_argument('-i', nargs=1, required=True, help='obs id',type=str)
parser.add_argument('-o', nargs="+", help='order tracer flat')
parser.add_argument('-d', nargs=1, default=["/home/kawahara/hds/ana"],help='directory',type=str)

args = parser.parse_args()    
anadir=os.path.join(args.d[0],"o"+str(args.i[0]))

flat=[]
expflat=[]
comp=[]
bias=[]
expbias=[]
obs=[]
obsname=[]

#bias list
bB = open(os.path.join(anadir,'b.B.list'), 'w', encoding="utf-8")
bR = open(os.path.join(anadir,'b.R.list'), 'w', encoding="utf-8")

#bias H list
HB = open(os.path.join(anadir,'H.B.list'), 'w', encoding="utf-8")
HR = open(os.path.join(anadir,'H.R.list'), 'w', encoding="utf-8")

#comparison
compB = open(os.path.join(anadir,'comp.B.list'), 'w', encoding="utf-8")
compR = open(os.path.join(anadir,'comp.R.list'), 'w', encoding="utf-8")

#Order trace flat
otf = open(os.path.join(anadir,'otf.list'), 'w', encoding="utf-8")

#flat
fR = open(os.path.join(anadir,'f.R.list'), 'w', encoding="utf-8")
fB = open(os.path.join(anadir,'f.B.list'), 'w', encoding="utf-8")
fRoml = open(os.path.join(anadir,'f.Roml.list'), 'w', encoding="utf-8")
fBoml = open(os.path.join(anadir,'f.Boml.list'), 'w', encoding="utf-8")

#object
objR = open(os.path.join(anadir,'obj.R.list'), 'w', encoding="utf-8")
objB = open(os.path.join(anadir,'obj.B.list'), 'w', encoding="utf-8")

otfsw2=0
flatt=[]
flatname=[]
for i in range(0,len(args.f)):
    otfsw=0
    file=args.f[i]
    hduread=fits.open(file)
    name=hduread[0].header["Object"]
    slt=hduread[0].header["SLT-LEN"]
    if args.o:
        for j in range(0,len(args.o)):
            if file == args.o[j] and name == "FLAT":
                otfsw=1
                otfsw2=otfsw2+1
                print("ORDER TRACE FILE DETECTED.")
                print(("SLT-LEN=",slt))
                otf.write(str(file[7:])+"\n")
            
    if file[0:4]=="HDSA":
        if name != "COMPARISON" and name != "FLAT" and name != "BIAS":
            if np.mod(int(file[11]),2)==1:
                objR.write(str(file[7:])+"\n")            
            else:
                objB.write(str(file[7:])+"\n")
        if name == "FLAT" and otfsw == 0:
            if np.mod(int(file[11]),2)==1:
                fR.write(str(file[7:])+"\n")
                fRoml.write("H"+str(file[7:]).replace(".fits","oml.fits")+"\n")
            else:
                fB.write(str(file[7:])+"\n")
                fBoml.write("H"+str(file[7:]).replace(".fits","oml.fits")+"\n")
            flatt.append(slt)
            flatname.append(file)
        if name == "BIAS":
            if np.mod(int(file[11]),2)==1:
                bR.write(str(file[7:])+"\n")
                HR.write("H"+str(file[7:]).replace(".fits","o.fits")+"\n")
            else:
                bB.write(str(file[7:])+"\n")
                HB.write("H"+str(file[7:]).replace(".fits","o.fits")+"\n")
        if name == "COMPARISON":
            if np.mod(int(file[11]),2)==1:
                compR.write(str(file[7:])+"\n")
            else:
                compB.write(str(file[7:])+"\n")

if args.o:
    if otfsw2<len(args.o):
        print("Warning: SOME ORDER TRACE FILE WAS UNDETECTED !")        
else:
        print("Warning: YOU DID NOT SPECIFY ORDER TRACE FLAT. Is it OK ?")
flatname=np.array(flatname)
if min(flatt) < max(flatt):
    mask = (np.array(flatt)==min(flatt))
    print("########################################")
    print("Warning: THERE IS SHORT SLT-LEN FLAT FILE(S) THAN OTHERS.")
    print("ARE THESE ORDER TRACE FLAT ?")
    print((flatname[mask]))
    flatt=np.array(flatt)
    print(("SLT-LEN=",flatt[mask],"mm"))
    print("########################################")


#bias list
bB.close
bR.close
#bias H list
HB.close
HR.close
#comparison
compB.close
compR.close
#Order trace flat
otf.close
#flat
fR.close
fB.close
fRoml.close
fBoml.close
#object
objR.close
objB.close
