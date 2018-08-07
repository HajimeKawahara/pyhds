import numpy as np
import pandas as pd
import pylab
import specmatchemp.library
import specmatchemp.plots as smplot
import matplotlib.pyplot as plt
from specmatchemp.specmatch import SpecMatch
import read_hds as rh
 
def oncpaint(event):
    fac=100.0
    xL=(wav[-1]-wav[0])/fac
    yL=spec[-1]-spec[0]
    r2=(wav-event.xdata)**2/xL**2 + (spec-event.ydata)**2/yL**2
    ind=np.argmin(r2)

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
#    parser = argparse.ArgumentParser(description='Read/Convert ecf(wr)_c (scombined spectrum) file to ...')
#    parser.add_argument('-f', nargs=1, required=True, help='ecf')
#    args = parser.parse_args()
    
#    fitslist=["/home/kawahara/hds/ana/o18113/H31062omlcs_ecfw.fits",
#              "/home/kawahara/hds/ana/o18113/H31064omlcs_ecfw.fits"]
    #data region
    wavlimin=[5130,5210]

    fitslist=["/home/kawahara/hds/ana/o18113/H31086omlcs_ecfw.fits"]
    blazedf="/home/kawahara/hds/ana/o18113/sBlazeB.fits"    
    wav,spec,mask,specsn = rh.read_nhds2d(fitslist,blazedf,wavlim=wavlimin)

    #MASKING
    msk=True
    if msk:
        mask=np.load(fitslist[0]+".mask.npy")
    fig=plt.figure()
    plt.plot(wav,spec,".",color="gray")
    plt.plot(wav[mask],spec[mask],".",color="red")
    plt.title("put x for mask, c for unmask.")
    if not msk:
        cid = fig.canvas.mpl_connect('key_press_event', oncpaint)
    plt.show()
    if not msk:
        np.save(fitslist[0]+".mask",mask)

    #INITIALIZATION
    #fit region
    wavlim=[5140,5200]
    lib = specmatchemp.library.read_hdf(wavlim=wavlim)
    #SHIFTING
    G_spectrum=rh.in_specmatch(wav[mask],spec[mask],specsn[mask])
    sm_G = SpecMatch(G_spectrum, lib)
    sm_G.shift()

    #######PLOT shift#####
    fig = plt.figure(figsize=(10,5))
    sm_G.target_unshifted.plot(normalize=True, plt_kw={'color':'forestgreen'}, text='Target (unshifted)')
    sm_G.target.plot(offset=0.5, plt_kw={'color':'royalblue'}, text='Target (shifted): HD190406')
    sm_G.shift_ref.plot(offset=1, plt_kw={'color':'firebrick'}, text='Reference: '+sm_G.shift_ref.name)
    plt.xlim(5160,5200)
    plt.ylim(0,2.2)
    plt.show()

    #FIT
    sm_G.match(wavlim=(5140,5200))
    sm_G.lincomb()

    print('Derived Parameters: ')
    print(sm_G.results)

    print('Teff: {0:.0f}, Radius: {1:.2f}, [Fe/H]: {2:.2f}'.format(
            sm_G.results['Teff'], sm_G.results['radius'], sm_G.results['feh']))
    fig2 = plt.figure(figsize=(12,6))
    sm_G.plot_lincomb()
    plt.show()

