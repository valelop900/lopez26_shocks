import glob, os
import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

indir = "data/vlass_cutouts_small"
outdir = "plots/vlass_qc_v2"
os.makedirs(outdir, exist_ok=True)

files = sorted(glob.glob(os.path.join(indir, "*.fits")))
print(len(files), "files")

for f in files:
    try:
        data = np.squeeze(fits.open(f)[0].data)
        med = np.nanmedian(data)
        # robust noise estimate
        sig = np.nanstd(data[np.abs(data - med) < 5*np.nanstd(data)])
        # background = med, top of scale = med + 20 sigma so real sources pop, noise stays dark
        vmin, vmax = med, med + 20*sig
        plt.figure(figsize=(4,4))
        plt.imshow(data, origin="lower", vmin=vmin, vmax=vmax, cmap="gray")
        ny, nx = data.shape
        plt.plot(nx/2, ny/2, "r+", ms=15, mew=1.5)
        plt.title(os.path.basename(f).split("_VLASS")[0], fontsize=7)
        plt.axis("off"); plt.tight_layout()
        plt.savefig(os.path.join(outdir, os.path.basename(f).replace(".fits",".png")), dpi=100)
        plt.close()
    except Exception as e:
        print("FAIL", os.path.basename(f), e)
print("done ->", outdir)
