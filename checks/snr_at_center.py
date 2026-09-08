import glob, os
import numpy as np
from astropy.io import fits

files = sorted(glob.glob("data/vlass_cutouts_small/*.fits"))
for f in files:
    data = np.squeeze(fits.open(f)[0].data)
    ny, nx = data.shape
    box = data[ny//2-5:ny//2+6, nx//2-5:nx//2+6]
    med = np.nanmedian(data)
    sig = np.nanstd(data[np.abs(data - med) < 5*np.nanstd(data)])
    snr = (np.nanmax(box) - med) / sig
    print(os.path.basename(f).split("_VLASS")[0], round(snr, 1))
