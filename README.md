# pyhds

This code is a python helper for hdsql (HDS on Subaru).

https://www.naoj.org/Observing/Instruments/HDS/hdsql-e.html

## Requirements

- python3
- astropy
- specmatch-emp

##

- hdsspec : hds to specmatch-emp
- read_ws : compiling and plotting spectra.


### How to make sBlaze.fits (simple Blaze) on iraf

-imarith FlatI2a2x1B / FlatI2a2x1B.nm FlatFlatI2a2x1B
-apall FlatFlatI2a2x1B BlazeB
-refs BlazeB
-dispcor BlazeB sBlazeB