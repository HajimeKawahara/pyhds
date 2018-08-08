from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

def read_hds_ecf(fitsfile,wavlim=None):
    ###scombine H31064omlcs_ecfwzr H31064omlcs_ecfwzr_c combine=sum group=images
    hdu = fits.open(fitsfile)
    header=hdu[0].header
    name=header["OBJECT"]
    print("OBJECT=",name)

    #    print("MJD",header["MJD"])
    #    print("JD",float(header["MJD"])+2400000.5)
    #    print("RA",header["RA"])
    #    print("DEC",header["DEC"])
    wcs = WCS(header)
    index = np.arange(header['NAXIS1'])
    wav,ar=wcs.all_pix2world(index,0,0)
    data=hdu[0].data
    if wavlim:
        ind=np.searchsorted(wav,wavlim)
        print(ind)
        return wav[ind[0]:ind[1]],data[ind[0]:ind[1]]
    else:
        return wav,data,header


def read_hds2d(fitsecf,blazedf,wavlim=None):
    import os

    fitsecf_combined=fitsecf.replace(".fits","_c.fits")
    blazedf_combined=blazedf.replace(".fits","_c.fits")

    if not os.path.isfile(fitsecf_combined):
        from pyraf import iraf
        iraf.scombine(input=fitsecf,output=fitsecf_combined,combine="sum",group="images")
    if not os.path.isfile(blazedf_combined):
        from pyraf import iraf
        iraf.scombine(input=blazedf,output=blazedf_combined,combine="sum",group="images")

    wav,data,header=read_hds_ecf(fitsecf_combined)#,wavlim=[5140,5200])
    bwav,bdata,header_blaze=read_hds_ecf(blazedf_combined)#,wavlim=[5140,5200])

    normspec=data/bdata
    
    if wavlim:
        ind=np.searchsorted(wav,wavlim)
        return wav[ind[0]:ind[1]], normspec[ind[0]:ind[1]], np.sqrt(data)[ind[0]:ind[1]], header
    else:
        return wav, normspec, np.sqrt(data), header

def normclipspec(normspec,crits=3.0,n=3):    

    mask=(normspec>0.0)
    for i in range(n):
        std=np.std(normspec[mask])
        upmask=(normspec<np.median(normspec[mask])+crits*std)
        mask=upmask*mask
    normspec=normspec/np.median(normspec[mask])

    return normspec, mask

def medclipspec(normspec,crit=3, n=10):    
    from scipy.signal import medfilt
    
    mf=medfilt(normspec,kernel_size=31)
    con=normspec-mf
    mask=con<crit*np.std(con) #only upper
    for i in range(n):
        mask=con<crit*np.std(con[mask]) #only upper

    return normspec, mask


def in_specmatch(w,s,serr,mask=None):
    from specmatchemp import spectrum
    from specmatchemp.spectrum import Spectrum
    if mask is None:
        return Spectrum(w, s, serr, mask=mask)
    else:
        return Spectrum(w, s, serr)


def read_nhds2d(filelist,blazedf,wavlim=[5140,5200]):
    specall=[]
    maskall=[]
    specsnall=[]
    headerall=[]
    wavcheck=0.0
    for fitsecf in filelist:
        print(fitsecf)
        wav,spec,specsn,header=read_hds2d(fitsecf,blazedf,wavlim=wavlim)
        spec,mask=medclipspec(spec)
        if len(filelist)==1:
            return wav, spec, mask, specsn, [header]
        
        spec[~mask]=None
        specsn[~mask]=None
        
        specall.append(spec)
        maskall.append(mask)
        specsnall.append(specsn)
        headerall.append(header)
        if wavcheck != 0.0 and wav[0] != wavcheck:
            print("Inconsistent wavelength!")
            sys.exit()
        wavcheck=wav[0]
    
    spec=np.nanmean(specall,axis=0)
    specsn=np.sqrt(np.nansum(np.array(specsnall)**2,axis=0))
    mask = (spec==spec)
    return wav, spec, mask, specsn, headerall

if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description='Read/Convert ecf(wr)_c (scombined spectrum) file to ...')
#    parser.add_argument('-f', nargs=1, required=True, help='ecf')
#    args = parser.parse_args()
    
#    fitslist=["/home/kawahara/hds/ana/o18113/H31062omlcs_ecfw.fits",
#              "/home/kawahara/hds/ana/o18113/H31064omlcs_ecfw.fits"]
    fitslist=["/home/kawahara/hds/ana/o18113/H31086omlcs_ecfw.fits"]

    blazedf="/home/kawahara/hds/ana/o18113/sBlazeB.fits"    
    #    wav,spec,specsn=read_hds2d(fitslist[0],blazedf,wavlim=[5140,5200])    
    #    spec,mask=normclipspec(spec)
    wav,spec,mask,specsn = read_nhds2d(fitslist,blazedf,wavlim=[5140,5200])

    fig=plt.figure()
    plt.plot(wav,spec,".")
 #   Sp=in_specmatch(wav,spec,specsn,mask)    
    plt.plot(wav[mask],spec[mask],".")
    plt.show()
