#!/usr/bin/python
from astropy.io import fits
from optparse import OptionParser, OptionValueError
import sys
import glob
import os

argvs = sys.argv

usage = '%prog [Args] [Options]\nDetailed options -h or --help'
version = 0.1
parser = OptionParser(usage=usage, version=version)
parser.add_option('-c', '--chead',action = 'store',type = 'str',dest = 'chead', 
                  help = 'Set head character')
parser.add_option('-t', '--type',action = 'store',type = 'str',dest = 'type', 
                  help = 'Set type')
parser.add_option('-u', '--un number',action = 'store_const',const=1,dest = 'nonnm', 
                  help = 'rm both non-number and number files')
parser.set_defaults(
    type="ALL",
    nonnm=0,
    )
options, args = parser.parse_args()
ch = str(options.chead)
ty = str(options.type)
nm = int(options.nonnm)

if nm==0:
    print("====================================")
    print(("rm "+ch+'(number).fits for the '+ty+" type."))
    print("====================================")
elif nm==1:
    print("====================================")
    print(("rm "+ch+'*.fits for the '+ty+" type."))
    print("====================================")

files = glob.glob(ch+"*.fits")
for file in files:
    hduread=fits.open(file)
    name=hduread[0].header["Object"]
    if name == ty or ty == "ALL":
        q=file[len(ch):len(ch)+1]
        if q.isdigit() or nm == 1:
            print(("rm "+file))        
            os.remove(file)
