import numpy as np
import matplotlib.pyplot as plt
import smart
import glob

trnst_fls = glob.glob('../smart_outputs/trop*/*trnst')

trops = []
o2s = []
ratios = []

for trnst_fl in trnst_fls:
    name = trnst_fl.split('/')[-2]
    trop = float('0.' + name.split('_')[2])
    o2 = float('0.' + name.split('_')[5])
    trnst = smart.readsmart.Trnst(trnst_fl)
    flux = trnst.tdepth * 1e6
    wl = trnst.lam

    P_band_inds = wl < 1.268
    Q_band_inds = (wl > 1.268) & (wl < 1.270)
    R_band_inds = wl > 1.268

    P_band_sum = sum(flux[P_band_inds])
    Q_band_sum = sum(flux[Q_band_inds])
    R_band_sum = sum(flux[R_band_inds])

    ratio = Q_band_sum / (P_band_sum + R_band_sum)

    trops.append(trop)
    o2s.append(o2)
    ratios.append(ratio)
    del trnst

plt.figure()
plt.scatter(o2s, trops, c=ratios)
plt.colorbar()
plt.savefig('test.pdf')

