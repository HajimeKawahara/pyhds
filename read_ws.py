import numpy as np
import pylab
import matplotlib.pyplot as plt
import argparse
import os
import sys
from time import sleep
import pandas as pd

def read_wsres_pd(wslist):
    # READ specmatch_emp results and Convert them to pandas DataFrame.
    lis=np.loadtxt(wslist,dtype="str")
    dic={}
    for i in lis[::-1]:
        name=i.replace(".ws.npz","").replace("KIC","")
        data=np.load(i)
        dic[name]=data["arr_0"][1]        
    df=pd.DataFrame(dic).transpose()
    
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='specmatch_emp fit of HDS spectrum')
    parser.add_argument('-f', nargs=1, help='ws file',type=str)

    args = parser.parse_args()
    data=np.load(args.f[0], allow_pickle=True)
    print(args.f[0])
    print(data["arr_0"][0])

    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)

    dic={}
    w=data["arr_0"][0][0]
    s=data["arr_0"][0][1]
    model=data["arr_0"][0][2]
    ax.plot(w,s,color="black",lw=1)
    ax.plot(w,model,color="red",lw=3,alpha=0.4)
    plt.xlabel("Wavelength [angstrom]")
    plt.show()
