import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import paperstyle

# makes fig_bpt_2panel.pdf: the [OI] BPT diagram and the SL-measure histogram.
# reads the classification table and the luminosity table in notes/. run from the project root.

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
S = paperstyle.S2

b = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv').drop_duplicates('TARGETID')[['TARGETID', 'Physical_Size', 'log_L_radio']]
df = b.merge(lum, on='TARGETID')
df = df[df['log_L_radio'] > 24]
df = df[(df['sample'] == 'small') | (df['Physical_Size'] > 25)]
print('objects:', len(df))

xv = df['log_oi_ha'].values
yv = df['log_oiii_hb'].values
samp = df['sample'].values
cls = df['bpt_class'].values

def kewley(x):
    return 0.73 / (x + 0.59) + 1.33
def syliner(x):
    return 1.18 * x + 1.30

fig, (ax, ax2) = plt.subplots(1, 2, figsize=paperstyle.TWO_PANEL)

# ---- BPT ----
ax.set_xlim(-2.5, 0.9)
ax.set_ylim(-1.8, 2.3)
styles = {
    ('large', 'seyfert'): ('large Seyfert', dict(marker='o', facecolors='black', edgecolors='black', s=S['o'])),
    ('large', 'liner'):   ('large LINER', dict(marker='*', facecolors='black', edgecolors='black', s=S['*'])),
    ('small', 'seyfert'): ('small Seyfert', dict(marker='o', facecolors='none', edgecolors='#5B2C6F', s=S['o'])),
    ('small', 'liner'):   ('small LINER', dict(marker='*', facecolors='none', edgecolors='#5B2C6F', s=S['*'])),
}
for (s_name, c_name), (lab, st) in styles.items():
    sel = (samp == s_name) & (cls == c_name)
    ax.scatter(xv[sel], yv[sel], label=lab, **st)
sf_sel = (samp == 'small') & (cls == 'sf')
if sf_sel.any():
    ax.scatter(xv[sf_sel], yv[sf_sel], marker='^', facecolors='none', edgecolors='#5B2C6F', s=S['^'], label='small SF')

xk = np.linspace(-2.5, -0.63, 100)
ax.plot(xk, kewley(xk), 'k-')
xs = np.linspace(-1.12, 0.4, 50)
ax.plot(xs, syliner(xs), 'k--')

ax.set_xlabel(r'log [O I] 6300 / H$\alpha$', fontsize=paperstyle.LABEL2)
ax.set_ylabel(r'log [O III] 5007 / H$\beta$', fontsize=paperstyle.LABEL2)
ax.tick_params(labelsize=paperstyle.TICK2)

ax.text(-2.3, 1.9, 'Seyfert', fontsize=14)
ax.text(-0.05, 0.0, 'LINER', fontsize=14)
ax.text(-2.35, -1.2, 'star\nforming', fontsize=14)
ax.legend(loc='lower right', fontsize=9)

# ---- SL histogram ----
d = (df['log_oiii_hb'] - 1.18*df['log_oi_ha'] - 1.30) * np.cos(np.arctan(1.18))
lg = d[df['sample'] == 'large']
sm = d[df['sample'] == 'small']
print('histogram: large %d  small %d' % (len(lg), len(sm)))
bins = np.arange(-1.0, 1.4, 0.15)
ax2.hist(lg, bins=bins, weights=np.ones(len(lg))/len(lg), histtype='stepfilled',
         facecolor='0.8', edgecolor=LARGE_COLOR, linewidth=1.0, label='large (>25 kpc), n=%d' % len(lg))
ax2.hist(sm, bins=bins, weights=np.ones(len(sm))/len(sm), histtype='stepfilled',
         facecolor='none', edgecolor=SMALL_COLOR, hatch='\\\\\\\\', linewidth=1.0, label='small (10-15 kpc), n=%d' % len(sm))
ax2.axvline(0, color='k', ls='--')
ax2.set_xlabel('SL measure', fontsize=paperstyle.LABEL2)
ax2.set_ylabel('fraction of sample', fontsize=paperstyle.LABEL2)
ax2.tick_params(labelsize=paperstyle.TICK2)
ax2.legend(loc='upper left')

plt.tight_layout()

# SL arrow. pick a point on the S-L divide at x = xt, then put the head at x = xh on the line
# perpendicular to the divide. the perpendicular is taken as it appears on the page, so the
# slope is scaled by the ratio of the two axes' data-units-per-inch after the layout is fixed.
pos = ax.get_position()
w_in, h_in = fig.get_size_inches()
sx = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (pos.width * w_in)
sy = (ax.get_ylim()[1] - ax.get_ylim()[0]) / (pos.height * h_in)
xt = 0.35
yt = syliner(xt)
xh = 0.0
m2 = -1 / 1.18 * (sy / sx)**2
c2 = yt - xt*m2
yh = m2*xh + c2
arrow = mpatches.FancyArrowPatch((xt, yt), (xh, yh), mutation_scale=20, color='r')
ax.add_patch(arrow)
ax.annotate('SL', xy=(xt, yt), xytext=(6, -18), textcoords='offset points', color='tab:red', fontweight='bold',
            path_effects=[pe.withStroke(linewidth=3, foreground='white')], fontsize=14)
print('arrow from (%.2f, %.2f) to (%.2f, %.2f)' % (xt, yt, xh, yh))

plt.savefig('plots/fig_bpt_2panel.pdf')
plt.savefig('plots/fig_bpt_2panel.png', dpi=paperstyle.PNG_DPI)
print('saved plots/fig_bpt_2panel.pdf')
