import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

f = "data/vlass_cutouts_small/VLASS3.2SE J130749.00+471016.4_VLASS3.2.se.T22t14.J130847+473000.06.2048.v1.I.iter3.image.pbcor.tt0.subim.fits"
img = np.squeeze(fits.getdata(f))
vmax = np.nanpercentile(img, 99.8)

plt.figure(figsize=(8, 8))
plt.imshow(img, origin="lower", cmap="gray_r", vmin=0, vmax=vmax)
plt.axis("off")
plt.savefig("plots/talk_mystery.png", dpi=200, bbox_inches="tight", pad_inches=0)