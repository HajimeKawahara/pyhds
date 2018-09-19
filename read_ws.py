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
    parser.add_argument('-d', nargs=1, default=["/home/kawahara/hds/ana/spectra"],help='directory',type=str)
    parser.add_argument('-f', nargs=1, default=["npzste.list"], help='npzlist',type=str)

    args = parser.parse_args()

    os.chdir(args.d[0])

    lis=np.loadtxt(args.f[0],dtype="str")
    fig=plt.figure(figsize=(7,14))
    dic={}
    
    of=0.0
    ax=fig.add_subplot(1,1,1)
    j=0
    for i in lis[::-1]:
        name=i.replace(".ws.npz","").replace("KIC","")
        data=np.load(i)
        w=data["arr_0"][0][0]
        s=data["arr_0"][0][1]
        model=data["arr_0"][0][2]
        dic[name]=data["arr_0"][1]        
        ax.text(w[0]-3.0,of+1.0,name+" ",horizontalalignment="right",verticalalignment="center",color="gray")
        if j==0:
            ax.plot(w,model+of+0.5,color="green",lw=1,alpha=0.7,label="model")
            ax.plot(w,s+of,color="black",lw=1,label="data")
        else:
            ax.plot(w,s+of,color="black",lw=1)
            ax.plot(w,model+of+0.5,color="green",lw=1,alpha=0.7)
        j=j+1
        of=of+1.5
    df=pd.DataFrame(dic).transpose()
    plt.xlabel("Wavelength [angstrom]")
    plt.legend(loc="lower right")
    print(df)
    plt.yticks([])
    #plt.show()
    plt.savefig(args.f[0].replace(".list","")+".pdf",bbox_inches="tight", pad_inches=0.0)
    #df.to_csv("hdsemp.csv",sep="|")
    #df.to_csv("hdsempSLC.csv")

    #SAVE
#    savefile=os.path.join(name+".ws")
#    np.savez(savefile,[np.array([w,s,ss]),sm_G.results,header])
