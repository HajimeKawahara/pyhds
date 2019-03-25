# HDS analysis 

- Raw data directory -> HDS/data/o?????
- Analysis directory -> HDS/ana/o?????

- 現在はPYHDSとhdsqlを併用

# tutorial

- [Formal tutorial of hdsql](https://www.naoj.org/Observing/Instruments/HDS/hdsql.html)

Blue = B　(偶数)を例に説明する

## 0.確認

~/hds/data/o18152b> show_header.py -f HD*.fits -t OBJECT H_I2CELL H_I2POS SLT-LEN SLT-WID WAV-MIN WAV-MAX EXPTIME -r

## 1. リストをつくるのはある程度pyhdsでできる。

```
cougar ~/hds/data/o18152b> python ../../pyhds/make_list.py -f HD*.fits -i 18152b

cougar ~/hds/ana/o18152b> ls

H.B.list  b.B.list  comp.B.list  f.B.list     f.R.list	   obj.B.list  otf.list
H.R.list  b.R.list  comp.R.list  f.Boml.list  f.Roml.list  obj.R.list
```

これを確認と見比べて必要なものだけ編集

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
clの起動
/home/kawahara/hdsで

```
xgterm
```

xgterm上で

```
cl
```

directoryに/home/kawahara/hdsを入力（戻れないから注意）

```
imred
eche
cd ana/o????
```

## 2.まずhdsqlをもちいてバッチでバイアスからH+++++.fitsなんとかを作成する

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

そこからは[チュートリアル](https://www.naoj.org/Observing/Instruments/HDS/hdsql.html)通りだがいくつか注意

- mkbadmaskのinputは Bias2x2B[0] を入力
- (mb_refe  =    Mask2x1B.fits[0]) Bad Pix Mask frame?
- (ap_refe  =    ApI2a2x1B )

## apall

- apallのときにdでだめなの消して、mでいいところを指定
- "w, [jktb]"
- back to wide view: "w a" 
- apply all orders: push "a"
- setting the upper limit of the error bar after pushing "a" :upper
- setting the lower limit of the error bar after pushing "a" :lower

## Blaze

sBlazeBのつくりかた

```
imarith FlatI2a2x1B / FlatI2a2x1B.nm FlatFlatI2a2x1B
apall FlatFlatI2a2x1B BlazeB
refs BlazeB
dispcor BlazeB sBlazeB
```




