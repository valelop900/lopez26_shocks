import io
import requests
import numpy as np
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import paperstyle

# makes fig_examples.pdf: one small and one large source, VLASS contours on Legacy Survey r band.
# reads data/catalog_*.csv and fetches the cutouts from legacysurvey.org. run from the project root.

small = pd.read_csv('data/catalog_small.csv')
large = pd.read_csv('data/catalog_large.csv')
cat = pd.concat([small, large], ignore_index=True)

ids = [39633349756585024, 39627842677376414]
size = 120   # pixels, 0.262"/pix, so 31 arcsec

def cutout(ra, dec, layer):
    url = ('https://www.legacysurvey.org/viewer/fits-cutout?ra=%.6f&dec=%.6f&layer=%s&pixscale=0.262&size=%d'
           % (ra, dec, layer, size))
    r = requests.get(url, timeout=120)
    return fits.open(io.BytesIO(r.content))[0].data

fig, axes = plt.subplots(1, 2, figsize=paperstyle.TWO_PANEL)
for ax, tid in zip(axes, ids):
    row = cat[cat['TARGETID'] == tid].iloc[0]
    opt = cutout(row['RA'], row['DEC'], 'ls-dr9')
    rad = cutout(row['RA'], row['DEC'], 'vlass1.2')
    if opt.ndim == 3:
        opt = opt[1]          # r band
    rad = np.squeeze(rad)
    noise = 1.4826 * np.nanmedian(np.abs(rad - np.nanmedian(rad)))
    ax.imshow(np.arcsinh(opt / np.nanstd(opt)), origin='lower', cmap='gray_r')
    ax.contour(rad, levels=noise * np.array([3, 6, 12, 24, 48]), colors='red', linewidths=1.0)
    ax.set_title('%s  z=%.3f  %.0f kpc' % ({'small': 'small (10-15 kpc)', 'large': 'large (>25 kpc)'}[row['sample']], row['Z'], row['Physical_Size']), fontsize=paperstyle.LABEL2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.plot([8, 8 + 10/0.262], [8, 8], 'k-', lw=2)
    ax.text(8, 12, '10"', fontsize=paperstyle.TICK2)

plt.tight_layout()
plt.savefig('plots/fig_examples.pdf')
plt.savefig('plots/fig_examples.png', dpi=paperstyle.PNG_DPI)
print('saved plots/fig_examples.pdf')
