import numpy as np
import pandas as pd
import pylab
import specmatchemp.library
import specmatchemp.plots as smplot
import matplotlib.pyplot as plt
from specmatchemp.specmatch import SpecMatch
import read_hds as rh
import argparse
import os
import sys
from time import sleep
from scipy.interpolate import interp1d

def oncpaint(event):
    fac=100.0
    xL=(wav[-1]-wav[0])/fac
    yL=spec[-1]-spec[0]
    r2=(wav-event.xdata)**2/xL**2 + (spec-event.ydata)**2/yL**2
    ind=np.nanargmin(r2)
    #    if event.button==1:
    if event.key=='x':
        mask[ind]=False
        plt.title("MASK="+str(ind))
        plt.plot([wav[ind]],[spec[ind]],".",color="gray")

    #    elif event.button==3:
    elif event.key=='d':
        mask[ind]=True
        plt.title("UNMASK="+str(ind))
        plt.plot([wav[ind]],[spec[ind]],".",color="red")

    fig.canvas.draw()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='specmatch_emp fit of HDS spectrum')
    parser.add_argument('-d', nargs=1,help='directory',type=str)
    parser.add_argument('-i', nargs=1,  help='obs id',type=str)
    parser.add_argument('-f', nargs="+", required=True, help='frame id(s)',type=str)
    parser.add_argument('-e', nargs=1, default=["omlcs_ecfwr"], help='file type',type=str)
    parser.add_argument('-b', nargs=1, default=["sBlazeB.fits"], help='blazed function',type=str)
    parser.add_argument('-w', nargs=2, default=[5140,5200], help='wavelength [AA] lower upper',type=float)
    parser.add_argument('-c', help='for clean 1d spectrum', action='store_true')

    args = parser.parse_args()
    if args.d:
        os.chdir(args.d[0])
    print("Extension=",args.e[0][-4:])
    if (args.e[0][-4:] != "ecfw" and args.e[0][-3:] != "ecw" and args.e[0][-4:] != "ecwc") and len(args.f) > 1:
        print(args.e[0][-4:])
        print("Use ecfw/ecw for the file type (-e) because you need to combine the spectra.")
        sys.exit("STOP")
    fitslist=[]
    for i in args.f:
        if args.i:
            fitslist.append(os.path.join("o"+str(args.i[0]),"H"+str(i)+str(args.e[0])+".fits"))
        else:
            fitslist.append(i)
            
            #data region
    #5000-5800
    #wavlimd=5140
    #wavlimu=5200
    wavlimd=args.w[0]
    wavlimu=args.w[1]

    wavlim=[wavlimd,wavlimu]
    wavlimin=[wavlimd-10,wavlimu+11]#[5130,5211]
    wavtag="AA"+str(int(wavlimd))+"_"+str(int(wavlimu))


    if args.c:
        wav,spec,header=rh.read_hds_ecf(fitslist[0],wavlim=wavlimin)
        spec,mask=rh.medclipspec(spec)
        specsn=np.ones(len(spec))#np.sqrt(spec)
    else:
        blazedf=os.path.join("o"+str(args.i[0]),str(args.b[0]))
        print("blaze function=",blazedf)
        wav,spec,mask,specsn,header = rh.read_nhds2d(fitslist,blazedf,wavlim=wavlimin)
    print(np.sum(spec[mask]))

    #NAME CHECK
    name=None
    print(np.shape(header))
    for ih in header:
        try:
            if name == None or name == ih["OBJECT"]:
                print("OBJECT=",ih["OBJECT"])
            else:
                print("OBJECT=",ih["OBJECT"])
                print("MISMATCH OBJECTS. OK? waiting 3 sec.")
                sleep(10)
            name=ih["OBJECT"]
        except:
            name="UNKNOWN"

        
    #MASKING
    maskfile=os.path.join(fitslist[0]+wavtag+".mask.npy")
    msk=os.path.isfile(maskfile)
    if msk:
        print("load maskfile.")
        mask=np.load(maskfile)
    
    fig=plt.figure()
    plt.plot(wav,spec,".",color="gray")
    plt.plot(wav[mask],spec[mask],".",color="red")
    plt.title("put x for mask, d for unmask.")
    cid = fig.canvas.mpl_connect('key_press_event', oncpaint)
    plt.show()
    np.save(fitslist[0]+".mask",mask)
    
    #INITIALIZATION
    #fit region
    lib = specmatchemp.library.read_hdf(wavlim=wavlim)
    #SHIFTING
    print(wav[mask])
    G_spectrum=rh.in_specmatch(wav[mask],spec[mask],specsn[mask])
    
    sm_G = SpecMatch(G_spectrum, lib)
    sm_G.shift()

    print(len(sm_G.target_unshifted.w))
    print(len(sm_G.target.w))
    print(sm_G.__dict__)
    
    #######PLOT shift#####
    fig = plt.figure(figsize=(10,5))
    sm_G.target_unshifted.plot(normalize=True, plt_kw={'color':'forestgreen'}, text='Target (unshifted)')
    sm_G.target.plot(offset=0.5, plt_kw={'color':'royalblue'}, text='Target (shifted): HD190406')
    sm_G.shift_ref.plot(offset=1, plt_kw={'color':'firebrick'}, text='Reference: '+sm_G.shift_ref.name)
    plt.xlim(wavlimd,wavlimu)
    plt.ylim(0,2.2)
    plt.show()

    #FIT

    sm_G.match(wavlim=(wavlimd,wavlimu))
    sm_G.lincomb()

    print('Derived Parameters: ')
    print(sm_G.results)

    print('Teff: {0:.0f}, Radius: {1:.2f}, [Fe/H]: {2:.2f}'.format(
            sm_G.results['Teff'], sm_G.results['radius'], sm_G.results['feh']))
    fig2 = plt.figure(figsize=(12,6))
    sm_G.plot_lincomb()
    plt.show()

    w=sm_G.lincomb_matches[0].target.w #wavelength
    s=sm_G.lincomb_matches[0].target.s #spectrum
    ss=sm_G.lincomb_matches[0].modified.s #fit curve
    
    #SAVE
    savefile=os.path.join(name+".ws")
    np.savez(savefile,[np.array([w,s,ss]),sm_G.results,header])

    ##RV
    margin=10.0 #AA
    w0=w[0] + margin
    w1=w[-1] - margin
    f = interp1d(w, ss)

    wavuse=wav[mask]
    specuse=spec[mask]
    maskwav=(wavuse>w0)*(wavuse<w1)
    wavuse=wavuse[maskwav]
    specuse=specuse[maskwav]

    c=299792.458
    vmax=100.0 #km/s
    nsearch=2000
    vpcsearch=np.linspace(-vmax/c,vmax/c,nsearch)
    cc=[]
    for vpc in vpcsearch:
        cc.append(np.sum(f(wavuse*(1.0+vpc))*specuse))
    cc=np.array(cc)
    maxind=np.argmax(cc)
    rv = -vpcsearch[maxind]*c
    print("RV=",rv,"km/s")

    f = open("rv.txt", 'a')
    f.write(name+","+str(rv)+"\n")
    f.close()

    fig=plt.figure()
    plt.plot(vpcsearch*c,cc)
    plt.plot([rv],[cc[maxind]],"o")
    plt.xlabel("RV [km/s]")
    plt.ylabel("CCF")
    plt.title(name)
    plt.show()

    
