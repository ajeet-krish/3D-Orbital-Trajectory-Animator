"""J2 precession time-lapse: orbital plane rotation due to Earth's bulge."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from orbital.core import compute_orbit, draw_earth
from orbital.config import apply_dark_theme

apply_dark_theme()

n_orbits = 20
frames_per_orbit = 30
total_frames = n_orbits * frames_per_orbit

e = 0.74
i_normal = 30.0
a = 1.0
w = 270.0

Omega_drift_total = 90.0

fig = plt.figure(figsize=(12, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])

limit = 1.9

def style_3d_ax(ax):
    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    ax.set_box_aspect([1, 1, 1])
    ax.set_facecolor("#1a1b26")
    ax.set_xlabel("X (Earth Radii)", color="#565f89")
    ax.set_ylabel("Y (Earth Radii)", color="#565f89")
    ax.set_zlabel("Z (Earth Radii)", color="#565f89")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("#3b4261")
    ax.yaxis.pane.set_edgecolor("#3b4261")
    ax.zaxis.pane.set_edgecolor("#3b4261")
    ax.tick_params(colors="#565f89")

ax1 = fig.add_subplot(gs[0], projection="3d")
style_3d_ax(ax1)
ax1.set_title("RAAN Precession", color="white", fontsize=14, fontweight="bold")
draw_earth(ax1, radius=1.0, color="#ff79c6", alpha=0.3)

ax2 = fig.add_subplot(gs[1], projection="3d")
style_3d_ax(ax2)
ax2.set_title("Apsidal Precession\n(i=30° → drifting)", color="white", fontsize=14, fontweight="bold")
draw_earth(ax2, radius=1.0, color="#ff79c6", alpha=0.3)

orbits_left = []
orbits_right_i30 = []

for k in range(n_orbits):
    Omega_k = k * Omega_drift_total / n_orbits
    w_k = k * 30.0 / n_orbits

    pos_left, _, _ = compute_orbit(a=1.0, e=0.1, i=60.0, Omega=Omega_k, w=0, n_orbits=1, n_points=100)
    orbits_left.append(pos_left)

    pos_right_i30, _, _ = compute_orbit(a=a, e=e, i=i_normal, Omega=0, w=w + w_k, n_orbits=1, n_points=100)
    orbits_right_i30.append(pos_right_i30)

sat1, = ax1.plot([], [], [], "o", color="#67e8f9", markersize=7,
                 markeredgecolor="white", markeredgewidth=0.5)
sat2, = ax2.plot([], [], [], "o", color="#f87171", markersize=7,
                 markeredgecolor="white", markeredgewidth=0.5)

for k in range(n_orbits):
    ax1.plot(orbits_left[k][:, 0], orbits_left[k][:, 1], orbits_left[k][:, 2],
             color="#67e8f9", linewidth=0.8, alpha=0.25)
    ax2.plot(orbits_right_i30[k][:, 0], orbits_right_i30[k][:, 1], orbits_right_i30[k][:, 2],
             color="#f87171", linewidth=0.8, alpha=0.25)

(hl_left,) = ax1.plot([], [], [], color="#67e8f9", linewidth=2, alpha=0.9)
(hl_right,) = ax2.plot([], [], [], color="#f87171", linewidth=2, alpha=0.9)

frame_per_orbit = total_frames // n_orbits

def init():
    sat1.set_data([], [])
    sat1.set_3d_properties([])
    sat2.set_data([], [])
    sat2.set_3d_properties([])
    hl_left.set_data([], [])
    hl_left.set_3d_properties([])
    hl_right.set_data([], [])
    hl_right.set_3d_properties([])
    return sat1, sat2, hl_left, hl_right

def update(frame):
    orbit_idx = frame // frame_per_orbit
    sub_frame = frame % frame_per_orbit

    if orbit_idx >= n_orbits:
        return sat1, sat2, hl_left, hl_right

    pos_l = orbits_left[orbit_idx]
    pos_r = orbits_right_i30[orbit_idx]

    hl_left.set_data(pos_l[:, 0], pos_l[:, 1])
    hl_left.set_3d_properties(pos_l[:, 2])
    hl_right.set_data(pos_r[:, 0], pos_r[:, 1])
    hl_right.set_3d_properties(pos_r[:, 2])

    pt_idx = min(sub_frame * 3, len(pos_l) - 1)
    sat1.set_data([pos_l[pt_idx, 0]], [pos_l[pt_idx, 1]])
    sat1.set_3d_properties([pos_l[pt_idx, 2]])
    sat2.set_data([pos_r[pt_idx, 0]], [pos_r[pt_idx, 1]])
    sat2.set_3d_properties([pos_r[pt_idx, 2]])

    return sat1, sat2, hl_left, hl_right

anim = animation.FuncAnimation(fig, update, frames=total_frames,
                                init_func=init, interval=30, blit=False, repeat=True)
anim.save("outputs/j2_precession.gif", writer="pillow", fps=30)
plt.close()
print("saved outputs/j2_precession.gif")
