import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Polygon, Arc, Circle

# gas cloud: grid of atoms on the right side of both panels
gx, gy = np.meshgrid(np.arange(4.6, 10.0, 0.55), np.arange(1.0, 5.6, 0.55))
ax_x = gx.ravel()
ax_y = gy.ravel()

# photons in fixed lanes, absorbed at the cloud's front face
lanes = np.arange(1.4, 5.4, 0.4)
phot_start = np.linspace(-4, 0.8, len(lanes))
wall = 6.0

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5))

for a, title in [(a1, 'SHINE ON IT: photons'), (a2, 'CRASH INTO IT: jet-driven shock')]:
    a.set_xlim(-0.3, 10.5)
    a.set_ylim(0, 6.8)
    a.set_xticks([])
    a.set_yticks([])
    a.set_title(title, fontsize=15, fontweight='bold')
    # black hole with a small glowing disk, same in both panels
    a.add_patch(Circle((0.9, 3.3), 0.45, color='black', zorder=5))
    a.add_patch(Circle((0.9, 3.3), 0.75, color='orange', alpha=0.5, zorder=4))
    a.text(0.9, 4.6, 'black hole\n+ hot disk', fontsize=10, ha='center')

atoms1 = a1.scatter(ax_x, ax_y, s=55, c='lightgray', edgecolors='gray', linewidths=0.5)
atoms2 = a2.scatter(ax_x, ax_y, s=55, c='lightgray', edgecolors='gray', linewidths=0.5)
phots = a1.scatter([], [], s=70, c='goldenrod', marker='>', zorder=6)

# the jet: a wedge that grows out of the black hole, plus a bow front at its tip
jet = Polygon([[0.9, 3.2], [0.9, 3.4], [1.0, 3.4], [1.0, 3.2]],
              color='#E67E22', zorder=6)
a2.add_patch(jet)
bow = Arc((1.0, 3.3), 1.6, 3.4, theta1=-75, theta2=75, lw=3,
          color='#5B2C6F', zorder=7)
a2.add_patch(bow)

lab1 = a1.text(7.3, 6.2, '', fontsize=12, ha='center', color='dimgray', fontweight='bold')
lab2 = a2.text(5.6, 6.2, '', fontsize=12, ha='center', color='#5B2C6F', fontweight='bold')

def update(i):
    t = min(i, 34) * 0.28

    # left: photons fly out of the disk, die at the cloud's front face
    px = phot_start + t * 1.4
    alive = px < wall
    phots.set_offsets(np.column_stack([px[alive], lanes[alive]]))
    lit1 = (ax_x < wall) & (t * 1.4 > ax_x - 4.0)
    atoms1.set_color(np.where(lit1, 'gold', 'lightgray'))

    # right: jet tip advances, bow front rides at the tip, gas behind it glows
    tip = min(1.0 + t * 0.95, 9.8)
    half = 0.10 + 0.09 * (tip - 1.0)      # jet widens as it grows
    jet.set_xy([[0.9, 3.3 - 0.1], [0.9, 3.3 + 0.1],
                [tip, 3.3 + half], [tip, 3.3 - half]])
    bow.set_center((tip, 3.3))
    bow.width = 1.2 + 0.25 * tip
    bow.height = 2.2 + 0.55 * tip
    atoms2.set_color(np.where(ax_x < tip, '#B266D9', 'lightgray'))

    if i >= 34:
        lab1.set_text('photons stop at the outer layer')
        lab2.set_text('the jet shocks ALL the gas')
    return atoms1, atoms2, phots, jet, bow, lab1, lab2

anim = FuncAnimation(fig, update, frames=34 + 25, interval=100)
anim.save('plots/energize_gas.gif', writer=PillowWriter(fps=10))
print('saved plots/energize_gas.gif')