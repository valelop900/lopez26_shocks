import glob, os
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

indir = "data/vlass_cutouts_small"
outdir = "plots/vlass_qc_small"
os.makedirs(outdir, exist_ok=True)

files = sorted(glob.glob(os.path.join(indir, "*.fits")))
print(len(files), "fits files")

for f in files:
    try:
        hdu = fits.open(f)[0]
        data = np.squeeze(hdu.data)  # VLASS cubes have extra axes
        # robust scaling: clip at 1st/99.5th percentile
        lo, hi = np.nanpercentile(data, [1, 99.5])
        plt.figure(figsize=(4, 4))
        plt.imshow(data, origin="lower", vmin=lo, vmax=hi, cmap="gray")
        ny, nx = data.shape
        plt.plot(nx/2, ny/2, "r+", ms=15, mew=1.5)  # mark center
        name = os.path.basename(f).split("_VLASS")[0]
        plt.title(name, fontsize=7)
        plt.axis("off")
        plt.tight_layout()
        out = os.path.join(outdir, os.path.basename(f).replace(".fits", ".png"))
        plt.savefig(out, dpi=100)
        plt.close()
    except Exception as e:
        print("FAILED:", os.path.basename(f), e)

print("done, PNGs in", outdir)
