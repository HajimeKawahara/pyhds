import pandas as pd
import argparse
import os
import numpy as np
parser = argparse.ArgumentParser(description='')
parser.add_argument('-f',nargs=1,default=["log20180905.txt"], help="logfile")
parser.add_argument('-o',nargs=1,default=["KELT-7"], help="object name")

args = parser.parse_args()

lfile=args.f[0]

dat=pd.read_csv(lfile,delimiter=",")
print(dat["OBJECT"])
mask=dat["OBJECT"]==args.o[0]
print(dat["pc"])

totp=np.sum(dat["pc"][mask].values)
print("Total counts=",totp)
print("Total SN=",np.sqrt(totp))
