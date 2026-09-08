import glob, os
import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

indir = "data/vlass_cutouts_small"
outdir = "plots/vlass_qc_v3"
os.makedirs(outdir, exist_ok=True)
files = sorted(glob.glob(os.path.join(indir, "*.fits")))
print(len(files), "files")

for f in files:
    data = np.squeeze(fits.open(f)[0].data)
    med = np.nanmedian(data)
    sig = np.nanstd(data[np.abs(data - med) < 5*np.nanstd(data)])
    vmin, vmax = med, med + 20*sig
    ny, nx = data.shape
    cx, cy = nx/2, ny/2
    gap = 0.03*nx
    length = 0.07*nx
    plt.figure(figsize=(4,4))
    plt.imshow(data, origin="lower", vmin=vmin, vmax=vmax, cmap="gray")
    plt.plot([cx-gap-length, cx-gap], [cy, cy], "r-", lw=1.2)
    plt.plot([cx+gap, cx+gap+length], [cy, cy], "r-", lw=1.2)
    plt.plot([cx, cx], [cy-gap-length, cy-gap], "r-", lw=1.2)
    plt.plot([cx, cx], [cy+gap, cy+gap+length], "r-", lw=1.2)
    plt.title(os.path.basename(f).split("_VLASS")[0], fontsize=7)
    plt.axis("off"); plt.tight_layout()
    plt.savefig(os.path.join(outdir, os.path.basename(f).replace(".fits",".png")), dpi=100)
    plt.close()
print("done ->", outdir)
