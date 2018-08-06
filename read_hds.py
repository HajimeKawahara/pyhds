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
    wcs = WCS(header)
    index = np.arange(header['NAXIS1'])
    wav,ar=wcs.all_pix2world(index,0,0)
    data=hdu[0].data
    if wavlim:
        ind=np.searchsorted(wav,wavlim)
        print(ind)
        return wav[ind[0]:ind[1]],data[ind[0]:ind[1]]
    else:
        return wav,data


def read_hdf_unblazed(fitsecf,blazedf,wavlim=None):
    import os

    fitsecf_combined=fitsecf.replace(".fits","_c.fits")
    blazedf_combined=blazedf.replace(".fits","_c.fits")

#    if ~os.path.exists(fitsecf_combined):
#        from pyraf import iraf
#        iraf.scombine(input=fitsecf,output=fitsecf_combined,combine="sum",group="images")
#    if ~os.path.exists(blazedf_combined):
#        from pyraf import iraf
#        iraf.scombine(input=blazedf,output=blazedf_combined,combine="sum",group="images")

    wav,data=read_hds_ecf(fitsecf_combined)#,wavlim=[5140,5200])
    bwav,bdata=read_hds_ecf(blazedf_combined)#,wavlim=[5140,5200])

    normspec=data/bdata
    
    if wavlim:
        ind=np.searchsorted(wav,wavlim)
        return wav[ind[0]:ind[1]], normspec[ind[0]:ind[1]], np.sqrt(data)[ind[0]:ind[1]]
    else:
        return wav, normspec, np.sqrt(data)

def normclipspec(normspec,crits=3.0,n=3):    

    mask=(normspec>0.0)
    for i in range(n):
        std=np.std(normspec[mask])
        upmask=(normspec<np.median(normspec[mask])+crits*std)
        mask=upmask*mask
    normspec=normspec/np.median(normspec[mask])

    return normspec, mask
    


    

    
if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description='Read/Convert ecf(wr)_c (scombined spectrum) file to ...')
#    parser.add_argument('-f', nargs=1, required=True, help='ecf')
#    args = parser.parse_args()
    
    fitsecf="/home/kawahara/hds/ana/o18113/H31064omlcs_ecfwr.fits"
    blazedf="/home/kawahara/hds/ana/o18113/sBlazeB.fits"

    wav,spec,specsn=read_hdf_unblazed(fitsecf,blazedf,wavlim=[5140,5200])
    spec,mask=normclipspec(spec)
    
    fig=plt.figure()
    plt.plot(wav[mask],spec[mask],".")
    plt.show()
