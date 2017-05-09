#!/usr/bin/python
from astropy.io import fits
import numpy as np
#import sys
#argvs = sys.argv
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

otf = open('otf.list', 'wb')
raw = open('raw.list', 'wb')
f = open('f.list', 'wb')
b = open('b.list', 'wb')
ov = open('ov.list', 'wb')
nl = open('nl.list', 'wb')
a = open('a.list', 'wb')
asl = open('as.list', 'wb')
s = open('s.list', 'wb')
w = open('w.list', 'wb')
p = open('p.list', 'wb')
v = open('v.list', 'wb')
q = open('q.list', 'wb')

fobj = open('f.obj.list', 'wb')
bobj = open('b.obj.list', 'wb')
fcomp = open('f.comp.list', 'wb')
acomp = open('a.comp.list', 'wb')

flat = open('flat.list', 'wb')
bias = open('bias.list', 'wb')

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
                print "ORDER TRACE FILE DETECTED."
                print "SLT-LEN=",slt
                otf.write("b"+str(file[7:])+"\n")
            
    if file[0:4]=="HDSA":
        raw.write(str(file)+'[0]'+"\n")
        f.write("f"+str(file[7:])+"\n")
        b.write("b"+str(file[7:])+"\n")
        ov.write("ov"+str(file[7:])+"\n")
        nl.write("nl"+str(file[7:])+"\n")
        print "all",name,file[7:]
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
            print name,file[7:]
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
        print "Warning: SOME ORDER TRACE FILE WAS UNDETECTED !"        
else:
        print "Warning: YOU DID NOT SPECIFY ORDER TRACE FLAT. Is it OK ?"
flatname=np.array(flatname)
if min(flatt) < max(flatt):
    mask = (np.array(flatt)==min(flatt))
    print "########################################"
    print "Warning: THERE IS SHORT SLT-LEN FLAT FILE(S) THAN OTHERS."
    print "ARE THESE ORDER TRACE FLAT ?"
    print flatname[mask]
    flatt=np.array(flatt)
    print "SLT-LEN=",flatt[mask],"mm"
    print "########################################"

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
