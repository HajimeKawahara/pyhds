from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
from astroquery.atomic import AtomicLineList
from astropy import units as u

def read_hds_ecf(fitsfile,wavlim=None):
    print(wavlim)
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
        return wav[ind[0]:ind[1]],data[ind[0]:ind[1]],header
    else:
        return wav,data,header


def read_hds2d(fitsecf,blazedf,wavlim=None):
    import os

    fitsecf_combined=fitsecf.replace(".fits","_c.fits")
    blazedf_combined=blazedf.replace(".fits","_c.fits")

    if not os.path.isfile(fitsecf_combined):
        from pyraf import iraf
        iraf.scombine(input=fitsecf,output=fitsecf_combined,combine="sum",group="images")

    wav,data,header=read_hds_ecf(fitsecf_combined)#,wavlim=[5140,5200])
        
    try: 
        if not os.path.isfile(blazedf_combined):
            from pyraf import iraf
            iraf.scombine(input=blazedf,output=blazedf_combined,combine="sum",group="images")
        bwav,bdata,header_blaze=read_hds_ecf(blazedf_combined)#,wavlim=[5140,5200])
        normspec=data/bdata
    except:
        normspec=data ###TEST####
    
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
    parser = argparse.ArgumentParser(description='show hds spectrum file')
    parser.add_argument('-f', nargs="+", default=["/home/kawahara/hds/ana/o18113/H31086omlcs_ecfw.fits"], help='hds file')
    parser.add_argument('-b', nargs=1, default=["/home/kawahara/hds/ana/o18113/sBlazeB.fits"], help='blaze file')
    parser.add_argument('-r', nargs=1, default=[27.8639], help='RV [km/s]',type=float)
#    parser.add_argument('-l', nargs=1, default=[27.8639], help='RV [km/s]',type=float)
    parser.add_argument('-w', nargs=2, default=[5140.0,5200.0], help='wavelength range [nm]',type=float)
    parser.add_argument('-l', help='Show metal lines', action='store_true')

    parser.add_argument('-e', nargs="+", default=["Mg I","Ca I"], help='element',type=str)
    parser.add_argument('-m', nargs=1, default=[2], help='display format',type=int)
    parser.add_argument('-c', help='for clean 1d spectrum', action='store_true')

    args = parser.parse_args()    
    form=args.m[0]
    c=299792.458
    rv=args.r[0]

    fitslist=args.f
    blazedf=args.b[0]
    wavlim=args.w #angstrom
    print(wavlim)
    if args.c:
        wav,spec,header=read_hds_ecf(fitslist[0])
        spec,mask=medclipspec(spec)
        specsn=np.sqrt(spec)
    else:
        wav,spec,mask,specsn,header = read_nhds2d(fitslist,blazedf,wavlim=wavlim)

    print(header[0])
    try:
        object_name=header[0]["OBJECT"]
    except:
        object_name="UNKNOWN"
    fig=plt.figure(figsize=(10,3))
    ax=fig.add_subplot(111)
    plt.plot(wav[mask],spec[mask],color="gray")
    plt.xlabel("wavelength [$\\AA$]")
    plt.title(object_name)#+" :RV = "+str(rv)+" km/s")
    maxv=np.max(spec[mask])
    minv=np.min(spec[mask])                    
    diff=(maxv-minv)
    if form==1:
        minv=minv-diff
    elif form==2:
        minv=minv-diff/4
    #LINES
    if args.l:
        wavelength_range = (wavlim[0] * u.angstrom, wavlim[1] * u.angstrom)
        elelist=args.e
        i=0
        for ele in elelist:
            try:
                linelist=AtomicLineList.query_object(wavelength_range, wavelength_type='air', wavelength_accuracy=20, element_spectrum=ele)
                for l in linelist['LAMBDA AIR ANG']:
                    try:
                        plt.axvline(np.float(l)*(1.0-rv/c),color="C"+str(i),ls="dotted")
                        if form==1:
                            ax.text(l*(1.0-rv/c),diff*0.0+minv," "+ele+"\n "+str(l)+"$\\AA$",color="C"+str(i),rotation="vertical",verticalalignment="bottom")
                        elif form==2:
                            ax.text(l*(1.0-rv/c),diff*0.0+minv," "+ele,color="C"+str(i),rotation="vertical",verticalalignment="bottom")
                    
                    except:
                        print("Ignore ",ele,l)
            except:
                print("Failed for the element ",ele)        
            i=i+1
    ###########################
    plt.ylim(np.max([minv,0.0]),maxv)
    plt.savefig(object_name+"_spec.pdf",bbox_inches="tight", pad_inches=0.0)    
    plt.savefig(object_name+"_spec.png",bbox_inches="tight", pad_inches=0.0)    
    plt.show()
#                plt.axvline(np.float(ll)*(1.0-rv/c),color="red",ls="dotted")
#                ax.text(l*(1.0-rv/c),diff*0.0+minv," "+ele+" "+str(l),color="red")
