#!/usr/bin/env python
from astropy.io import fits
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Make lists for HDS analysis')
parser.add_argument('-f', nargs="+", required=True, help='HDSA fits')
parser.add_argument('-o', nargs="+", help='order tracer flat')
args = parser.parse_args()    

flat=[]
expflat=[]
comp=[]
bias=[]
expbias=[]
obs=[]
obsname=[]

otf = open('otf.list', 'w', encoding="utf-8")
raw = open('raw.list', 'w', encoding="utf-8")
f = open('f.list', 'w', encoding="utf-8")
b = open('b.list', 'w', encoding="utf-8")
ov = open('ov.list', 'w', encoding="utf-8")
nl = open('nl.list', 'w', encoding="utf-8")
a = open('a.list', 'w', encoding="utf-8")
asl = open('as.list', 'w', encoding="utf-8")
s = open('s.list', 'w', encoding="utf-8")
w = open('w.list', 'w', encoding="utf-8")
p = open('p.list', 'w', encoding="utf-8")
v = open('v.list', 'w', encoding="utf-8")
q = open('q.list', 'w', encoding="utf-8")

fobj = open('f.obj.list', 'w', encoding="utf-8")
bobj = open('b.obj.list', 'w', encoding="utf-8")
fcomp = open('f.comp.list', 'w', encoding="utf-8")
acomp = open('a.comp.list', 'w', encoding="utf-8")

flat = open('flat.list', 'w', encoding="utf-8")
bias = open('bias.list', 'w', encoding="utf-8")

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
                otf.write("b"+str(file[7:])+"\n")
            
    if file[0:4]=="HDSA":
        raw.write(str(file)+'[0]'+"\n")
        f.write("f"+str(file[7:])+"\n")
        b.write("b"+str(file[7:])+"\n")
        ov.write("ov"+str(file[7:])+"\n")
        nl.write("nl"+str(file[7:])+"\n")
        print(("all",name,file[7:]))
        if name != "COMPARISON" and name != "FLAT" and name != "BIAS":
            a.write("a"+str(file[7:])+"\n")
            s.write("s"+str(file[7:])+"\n")
            w.write("w"+str(file[7:])+"\n")
            asl.write("as"+str(file[7:])+"\n")
            p.write("p"+str(file[7:])+"\n")
            v.write("v"+str(file[7:])+"\n")
            q.write("q"+str(file[7:])+"\n")

            fobj.write("f"+str(file[7:])+"\n")
            bobj.write("b"+str(file[7:])+"\n")
        if name == "FLAT" and otfsw == 0:
            print((name,file[7:]))
            flat.write("b"+str(file[7:])+"\n")
            flatt.append(slt)
            flatname.append(file)
        if name == "BIAS":
            bias.write("nl"+str(file[7:])+"\n")
        if name == "COMPARISON":
            fcomp.write("f"+str(file[7:])+"\n")
            acomp.write("a"+str(file[7:])+"\n")

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

raw.close
f.close
b.close
ov.close
nl.close
a.close
asl.close
p.close
s.close
w.close
q.close
v.close
fobj.close
flat.close
bias.close
fcomp.close
acomp.close
