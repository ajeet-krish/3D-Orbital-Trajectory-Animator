"""Hohmann transfer animation: spacecraft moving between two circular orbits."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from orbital.core import compute_orbit, draw_earth, setup_3d_axes
from orbital.config import apply_dark_theme

apply_dark_theme()

r1 = 1.1
r2 = 2.5
a_transfer = (r1 + r2) / 2
e_transfer = (r2 - r1) / (r2 + r1)

pos_a, _, _ = compute_orbit(a=r1, e=0.0, i=30.0, n_orbits=1, n_points=120)
pos_t, _, _ = compute_orbit(a=a_transfer, e=e_transfer, i=30.0, w=0.0, n_orbits=1, n_points=200)
pos_b, _, _ = compute_orbit(a=r2, e=0.0, i=30.0, n_orbits=1, n_points=120)

all_pos = np.vstack([pos_a, pos_t, pos_b])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
setup_3d_axes(ax, all_pos)
draw_earth(ax, radius=1.0, color="#ff79c6", alpha=0.5)

ax.plot(pos_a[:, 0], pos_a[:, 1], pos_a[:, 2],
        color="#67e8f9", linewidth=0.8, alpha=0.4, label="Initial orbit")
ax.plot(pos_t[:, 0], pos_t[:, 1], pos_t[:, 2],
        color="#fb923c", linewidth=0.8, alpha=0.4, label="Transfer orbit")
ax.plot(pos_b[:, 0], pos_b[:, 1], pos_b[:, 2],
        color="#4ade80", linewidth=0.8, alpha=0.4, label="Target orbit")
ax.legend(loc="upper right", fontsize=9, facecolor="#24253a", edgecolor="#3b4261")
ax.set_title("Hohmann Transfer", color="white", fontsize=14, fontweight="bold")

(sc,) = ax.plot([], [], [], "o", color="white", markersize=8,
                markeredgecolor="white", markeredgewidth=0.5)
(trail,) = ax.plot([], [], [], color="#ffffff", linewidth=2, alpha=0.7)
burn_label = ax.text2D(0.5, 0.85, "", transform=ax.transAxes,
                       color="#f87171", fontsize=11, ha="center", fontweight="bold",
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="#24253a",
                                 edgecolor="#f87171", linewidth=0.5))

n_a = len(pos_a)
n_t = len(pos_t)
half_a = n_a // 2

path = np.vstack([pos_a[:half_a], pos_t, pos_b[:half_a]])
n_total = len(path)
trail_len = 60

burn1_frame = half_a
burn2_frame = half_a + n_t - 1

burn1_marker = ax.scatter([], [], [], color="#f87171", s=120, marker="*", zorder=20)

def init():
    sc.set_data([], [])
    sc.set_3d_properties([])
    trail.set_data([], [])
    trail.set_3d_properties([])
    burn_label.set_text("")
    return sc, trail, burn_label

def update(frame):
    sc.set_data([path[frame, 0]], [path[frame, 1]])
    sc.set_3d_properties([path[frame, 2]])

    start = max(0, frame - trail_len)
    trail.set_data(path[start:frame+1, 0], path[start:frame+1, 1])
    trail.set_3d_properties(path[start:frame+1, 2])

    if frame == burn1_frame:
        burn_label.set_text("Burn 1 (perigee) — enter transfer")
        burn1_marker.set_offsets([[path[frame, 0], path[frame, 1]]])
        burn1_marker.set_3d_properties([path[frame, 2]], "z")
        burn1_marker.set_visible(True)
    elif frame == burn2_frame:
        burn_label.set_text("Burn 2 (apogee) — circularize")
        burn1_marker.set_offsets([[path[frame, 0], path[frame, 1]]])
        burn1_marker.set_3d_properties([path[frame, 2]], "z")
        burn1_marker.set_visible(True)
    elif frame < burn1_frame:
        burn_label.set_text("Coasting in initial orbit")
        burn1_marker.set_visible(False)
    elif frame > burn1_frame and frame < burn2_frame:
        burn_label.set_text("Coasting on transfer ellipse")
        burn1_marker.set_visible(False)
    else:
        burn_label.set_text("Target orbit achieved")
        burn1_marker.set_visible(False)

    return sc, trail, burn_label

anim = animation.FuncAnimation(fig, update, frames=n_total,
                                init_func=init, interval=30, blit=False, repeat=True)
anim.save("outputs/hohmann.gif", writer="pillow", fps=30)
plt.close()
print("saved outputs/hohmann.gif")
