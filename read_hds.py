from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
from pyraf import iraf

def read_hdf_ecf(fitsfile):
    ###scombine H31064omlcs_ecfwzr H31064omlcs_ecfwzr_c combine=sum group=images
    hdu = fits.open(fitsfile)
    print(hdu.info())

    header=hdu[0].header    
    wcs = WCS(header)
    index = np.arange(header['NAXIS1'])
    wav,ar=wcs.all_pix2world(index,0,0)
    print(wav)
    data=hdu[0].data
    print(np.shape(wav),np.shape(data))
    fig=plt.figure()
    plt.plot(wav,data)
    plt.show()
    hdu.close()
    
if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description='Read/Convert ecf(wr)_c (scombined spectrum) file to ...')
#    parser.add_argument('-f', nargs=1, required=True, help='ecf')
#    args = parser.parse_args()

    fitsecf="/home/kawahara/hds/ana/o18113/H31064omlcs_ecfwzr_c.fits"
    fitsecf_combined=fitsecf.replace(".fits","_c.fits")
    iraf.scombine(input=fitsecf,output=fitsecf_combined,combine="sum",group="images")
    read_hdf_ecf(fitsecf_combined)
