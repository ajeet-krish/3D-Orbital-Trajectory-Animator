import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from orbital.core import compute_orbit, draw_earth
from orbital.config import apply_dark_theme

apply_dark_theme()

n_frames = 120
n_pts = 200
advance_rate = 3
trail_len = 15

# Phase 1: eccentricity sweep 0.02 → 0.80
ecc_values = np.linspace(0.02, 0.80, 60)
# Phase 2: inclination sweep 0° → 90°
incl_values = np.linspace(0, 90, 60)

orbits = []
for e in ecc_values:
    pos, _, _ = compute_orbit(
        a=1.0, e=e, i=30.0, Omega=0, w=0, n_orbits=1, n_points=n_pts
    )
    orbits.append(pos)
for i_val in incl_values:
    pos, _, _ = compute_orbit(
        a=1.0, e=0.80, i=i_val, Omega=0, w=0, n_orbits=1, n_points=n_pts
    )
    orbits.append(pos)

# Global limits (from the farthest orbit)
all_max = max(p.max() for p in orbits) * 1.4

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

ax.set_xlim([-all_max, all_max])
ax.set_ylim([-all_max, all_max])
ax.set_zlim([-all_max, all_max])
ax.set_box_aspect([1, 1, 1])
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("#3b4261")
ax.yaxis.pane.set_edgecolor("#3b4261")
ax.zaxis.pane.set_edgecolor("#3b4261")
ax.tick_params(colors="#565f89")

draw_earth(ax, radius=1.0, color="#ff79c6", alpha=0.3)

# Neon glow: wide dim line behind the crisp orbit
(glow,) = ax.plot([], [], [], color="#8be9fd", linewidth=5, alpha=0.15)
(orbit_line,) = ax.plot([], [], [], color="#8be9fd", linewidth=2, alpha=0.9)
(trail,) = ax.plot([], [], [], color="#8be9fd", linewidth=1.8, alpha=0.6)
(sat,) = ax.plot(
    [], [], [],
    "o", color="#ffffff", markersize=8,
    markeredgecolor="#ff79c6", markeredgewidth=0.5,
)
param_label = ax.text2D(
    0.02, 0.93, "",
    transform=ax.transAxes, color="#ff79c6",
    fontsize=13, fontweight="bold",
)

sat_idx = 0


def init():
    glow.set_data([], [])
    glow.set_3d_properties([])
    orbit_line.set_data([], [])
    orbit_line.set_3d_properties([])
    trail.set_data([], [])
    trail.set_3d_properties([])
    sat.set_data([], [])
    sat.set_3d_properties([])
    param_label.set_text("")
    return glow, orbit_line, trail, sat, param_label


def update(frame):
    global sat_idx
    pos = orbits[frame]
    n = len(pos)

    glow.set_data(pos[:, 0], pos[:, 1])
    glow.set_3d_properties(pos[:, 2])
    orbit_line.set_data(pos[:, 0], pos[:, 1])
    orbit_line.set_3d_properties(pos[:, 2])

    sat_idx = (sat_idx + advance_rate) % n
    sat.set_data([pos[sat_idx, 0]], [pos[sat_idx, 1]])
    sat.set_3d_properties([pos[sat_idx, 2]])

    trail_start = (sat_idx - trail_len) % n
    if trail_start < sat_idx:
        trail_pts = pos[trail_start : sat_idx + 1]
    else:
        trail_pts = np.concatenate([pos[trail_start:], pos[: sat_idx + 1]])
    trail.set_data(trail_pts[:, 0], trail_pts[:, 1])
    trail.set_3d_properties(trail_pts[:, 2])

    if frame < 60:
        param_label.set_text(f"e = {ecc_values[frame]:.2f}")
    else:
        param_label.set_text(f"i = {incl_values[frame - 60]:.0f}°")

    return glow, orbit_line, trail, sat, param_label


anim = animation.FuncAnimation(
    fig, update, frames=n_frames,
    init_func=init,     interval=30,
    blit=False, repeat=True,
)
anim.save("outputs/parameter_sweep.gif", writer="pillow", fps=30)
plt.close()
