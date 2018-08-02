#!/usr/bin/python
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import sys

argvs = sys.argv
file=argvs[1]
print(file)
hduread=fits.open(file)
name=hduread[0].header["Object"]
obs=hduread[0].header["Observer"]

print(name)
print(obs)

dat=hduread[0].data

print((dat.shape))

fig=plt.figure()
ax = fig.add_subplot(111,aspect=1.0)
bar=plt.imshow(dat,interpolation='nearest',vmin=1000,vmax=2500)
plt.colorbar(bar)
plt.show()


