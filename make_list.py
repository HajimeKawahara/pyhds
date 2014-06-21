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
raw = open('raw.list', 'wb')
f = open('f.list', 'wb')
b = open('b.list', 'wb')
ov = open('ov.list', 'wb')
nl = open('nl.list', 'wb')
a = open('a.list', 'wb')
flat = open('flat.list', 'wb')
bias = open('bias.list', 'wb')

for i in range(1,len(argvs)):
    file=argvs[i]
    hduread=fits.open(file)
    name=hduread[0].header["Object"]
    if file[0:4]=="HDSA":
        raw.write(str(file)+'[0]'+"\n")
        f.write("f"+str(file[7:])+"\n")
        b.write("b"+str(file[7:])+"\n")
        ov.write("ov"+str(file[7:])+"\n")
        nl.write("nl"+str(file[7:])+"\n")
        if name != "COMPARISON" and name != "FLAT" and name != "BIAS":
            a.write("a"+str(file[7:])+"\n")
        if name == "FLAT":
            flat.write("b"+str(file[7:])+"\n")
        if name == "BIAS":
            bias.write("nl"+str(file[7:])+"\n")

raw.close
f.close
b.close
ov.close
nl.close
a.close
flat.close
bias.close
