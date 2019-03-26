# pyhds

This code is a python helper for hdsql (HDS on Subaru).

https://www.naoj.org/Observing/Instruments/HDS/hdsql-e.html

## Requirements

- python3
- astropy
- specmatch-emp

## Codes

- hdsspec : hds to specmatch-emp
- read_ws : compiling and plotting spectra.
- make_list: generating lists uo be used in hdsql


# Tutorial of HDS analysis 

Use [hdsql](https://www.naoj.org/Observing/Instruments/HDS/hdsql.html). 

- Raw data directory -> HDS/data/o?????
- Analysis directory -> HDS/ana/o?????

- [Formal tutorial of hdsql](https://www.naoj.org/Observing/Instruments/HDS/hdsql.html)

For examples, we assume the Blue part = B　(even number).

## 0. Confirmation

~/hds/data/o18152b> show_header.py -f HD*.fits -t OBJECT H_I2CELL H_I2POS SLT-LEN SLT-WID WAV-MIN WAV-MAX EXPTIME -r

## 1. make_list.py in pyhds generates the lists to be used in hdsql

```
cougar ~/hds/data/o18152b> python ../../pyhds/make_list.py -f HD*.fits -i 18152b

cougar ~/hds/ana/o18152b> ls

H.B.list  b.B.list  comp.B.list  f.B.list     f.R.list	   obj.B.list  otf.list
H.R.list  b.R.list  comp.R.list  f.Boml.list  f.Roml.list  obj.R.list
```

Edit them with checking the results from the confirmation.

- bias (Blue):
H.B
b.B

- comparison:
comp.B

- flat:
f.B
f.Boml

- object:
obj.B.list

------------------------------------------
Execute cl.
At /home/kawahara/hds

```
xgterm
```

On xgterm

```
cl
```

input /home/kawahara/hds to "directory". On iraf, 

```
imred
eche
cd ana/o????
```

## 2. Generate H+++++.fits from bias using hdsql

Here is an example of epar hdsql.

```
======================================================    
inid    =                    Input frame ID
(indirec= /data/o05129/HDSA000) directory of Input data

(batch  =                   yes) Batch Mode?
(inlist =                   b.B.list) Input file list for batch-mode
(overw  =                  yes) Force to overwrite existing images?

(oversca=                  yes) Overscan?
(biassub=                   no) BIAS / Dark Subtraction?
(maskbad=                   no) Mask Bad Pixels?
(linear =                   no) Linearity Correction?
(cosmicr=                   no) Cosmicray-event rejection?
(scatter=                   no) Scattered light subtraction?
(xtalk  =                   no) CCD Amp Cross-Talk Subtraction?
(flat   =                   no) Flat fielding?
(apall  =                   no) Extract spectra with apall?
===========================================================
```

Follow the [tutorial](https://www.naoj.org/Observing/Instruments/HDS/hdsql.html) from here. The following lists are some tips.

- Input Bias2x2B[0] in mkbadmask
- (mb_refe  =    Mask2x1B.fits[0]) Bad Pix Mask frame?
- (ap_refe  =    ApI2a2x1B )

## apall

- in apall, delete by "d", specify good positions by "m"
- "w, [jktb]"
- back to wide view: "w a" 
- apply all orders: push "a"
- setting the upper limit of the error bar after pushing "a" :upper
- setting the lower limit of the error bar after pushing "a" :lower

## simple Blaze function

How to generate sBlazeB (simple Blaze function).

```
imarith FlatI2a2x1B / FlatI2a2x1B.nm FlatFlatI2a2x1B
apall FlatFlatI2a2x1B BlazeB
refs BlazeB
dispcor BlazeB sBlazeB
```




