import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

files = {
    "plots/talk_cutout_confined.png": ("data/vlass_cutouts_small/VLASS3.2SE J074900.10+351823.1_VLASS3.2.se.T19t10.J074837+353000.06.2048.v1.I.iter3.image.pbcor.tt0.subim.fits", 30),
    "plots/talk_cutout_escaped.png": ("data/vlass_cutouts_small/VLASS3.2SE J130749.00+471016.4_VLASS3.2.se.T22t14.J130847+473000.06.2048.v1.I.iter3.image.pbcor.tt0.subim.fits", 90),
}

for out, (f, box) in files.items():
    img = np.squeeze(fits.getdata(f))
    cy, cx = img.shape[0] // 2, img.shape[1] // 2
    cy = cy + 10   # shift crop up/down to recenter the diagonal source
    cx = cx + 10
    img = img[cy-box:cy+box, cx-box:cx+box]

    noise = np.nanstd(img)
    vmin = 1.5 * noise
    vmax = np.nanmax(img) * 0.9

    plt.figure(figsize=(6, 6))
    plt.imshow(img, origin="lower", cmap="gray_r", vmin=vmin, vmax=vmax,
               interpolation="gaussian")
    plt.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(out, dpi=200)
    plt.close()