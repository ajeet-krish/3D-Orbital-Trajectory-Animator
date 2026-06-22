"""Ground track projection: satellite sub-point mapped onto Earth surface."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from orbital.core import compute_orbit
from orbital.config import apply_dark_theme, orbits_config

apply_dark_theme()

Omega_earth = 360.0

def eci_to_ground(pos, dt):
    n = len(pos)
    lat = np.degrees(np.arcsin(pos[:, 2] / np.linalg.norm(pos, axis=1)))
    lon = np.degrees(np.arctan2(pos[:, 1], pos[:, 0]))
    earth_rotation = np.cumsum(np.full(n, dt * Omega_earth))
    lon = (lon - earth_rotation + 180) % 360 - 180
    return lat, lon

fig = plt.figure(figsize=(12, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1])

ax_map = fig.add_subplot(gs[0])
ax_map.set_facecolor("#0d1321")
ax_map.set_xlim(-180, 180)
ax_map.set_ylim(-90, 90)
ax_map.set_xlabel("Longitude", color="#565f89")
ax_map.set_ylabel("Latitude", color="#565f89")
ax_map.tick_params(colors="#565f89")
ax_map.set_title("Ground Tracks (one orbit, Earth rotation)", color="white", fontsize=14, fontweight="bold")
ax_map.grid(True, color="#1e3248", linewidth=0.5)

ax_3d = fig.add_subplot(gs[1], projection="3d")
limit = 1.8
ax_3d.set_xlim([-limit, limit])
ax_3d.set_ylim([-limit, limit])
ax_3d.set_zlim([-limit, limit])
ax_3d.set_box_aspect([1, 1, 1])
ax_3d.set_facecolor("#1a1b26")
ax_3d.set_xlabel("X (Earth Radii)", color="#565f89")
ax_3d.set_ylabel("Y (Earth Radii)", color="#565f89")
ax_3d.set_zlabel("Z (Earth Radii)", color="#565f89")
ax_3d.xaxis.pane.fill = False
ax_3d.yaxis.pane.fill = False
ax_3d.zaxis.pane.fill = False
ax_3d.xaxis.pane.set_edgecolor("#3b4261")
ax_3d.yaxis.pane.set_edgecolor("#3b4261")
ax_3d.zaxis.pane.set_edgecolor("#3b4261")
ax_3d.tick_params(colors="#565f89")
ax_3d.set_title("3D View", color="white", fontsize=14, fontweight="bold")

colors = {"LEO": "#67e8f9", "GEO": "#4ade80", "Molniya": "#fb923c"}
select_configs = [c for c in orbits_config if c["label"] in colors]

orbit_data = {}
for cfg in select_configs:
    pos, t, _ = compute_orbit(
        a=cfg["a"], e=cfg["e"], i=cfg["i"],
        Omega=cfg["Omega"], w=cfg["w"],
        n_orbits=1, n_points=300,
    )
    dt = t[1] - t[0]
    lat, lon = eci_to_ground(pos, dt)
    orbit_data[cfg["label"]] = dict(pos=pos, lat=lat, lon=lon, color=cfg["color"])
    ax_map.plot(lon, lat, color=cfg["color"], linewidth=1.2, alpha=0.6, label=cfg["label"])

ax_map.legend(loc="upper right", fontsize=9, facecolor="#24253a", edgecolor="#3b4261")

n_frames = 200

dots_map = {}
trails_map = {}
dots_3d = {}
trails_3d = {}

for label, data in orbit_data.items():
    n_pts = len(data["pos"])
    step = max(1, n_pts // n_frames)
    data["pos_sampled"] = data["pos"][::step][:n_frames]
    data["lat_sampled"] = data["lat"][::step][:n_frames]
    data["lon_sampled"] = data["lon"][::step][:n_frames]

    dot_m, = ax_map.plot([], [], "o", color=data["color"], markersize=5)
    trail_m, = ax_map.plot([], [], color=data["color"], linewidth=1, alpha=0.5)
    dots_map[label] = dot_m
    trails_map[label] = trail_m

    dot_3d, = ax_3d.plot([], [], [], "o", color=data["color"], markersize=7,
                         markeredgecolor="white", markeredgewidth=0.5)
    trail_3d, = ax_3d.plot([], [], [], color=data["color"], linewidth=1.5, alpha=0.7)
    dots_3d[label] = dot_3d
    trails_3d[label] = trail_3d

    ax_3d.plot(data["pos"][:, 0], data["pos"][:, 1], data["pos"][:, 2],
               color=data["color"], linewidth=0.6, alpha=0.4)

trail_len = 30

def init():
    for d in list(dots_map.values()) + list(trails_map.values()) + list(dots_3d.values()) + list(trails_3d.values()):
        if hasattr(d, 'set_data'):
            d.set_data([], [])
            if hasattr(d, 'set_3d_properties'):
                d.set_3d_properties([])
    return list(dots_map.values()) + list(trails_map.values()) + list(dots_3d.values()) + list(trails_3d.values())

def update(frame):
    artists = []
    for label in orbit_data:
        data = orbit_data[label]
        i = min(frame, len(data["lat_sampled"]) - 1)

        dots_map[label].set_data([data["lon_sampled"][i]], [data["lat_sampled"][i]])
        start = max(0, i - trail_len)
        trails_map[label].set_data(data["lon_sampled"][start:i+1], data["lat_sampled"][start:i+1])
        artists.extend([dots_map[label], trails_map[label]])

        dots_3d[label].set_data([data["pos_sampled"][i, 0]], [data["pos_sampled"][i, 1]])
        dots_3d[label].set_3d_properties([data["pos_sampled"][i, 2]])
        trails_3d[label].set_data(data["pos_sampled"][start:i+1, 0], data["pos_sampled"][start:i+1, 1])
        trails_3d[label].set_3d_properties(data["pos_sampled"][start:i+1, 2])
        artists.extend([dots_3d[label], trails_3d[label]])

    return artists

anim = animation.FuncAnimation(fig, update, frames=n_frames,
                                init_func=init, interval=30, blit=False, repeat=True)
anim.save("outputs/ground_track.gif", writer="pillow", fps=30)
plt.close()
print("saved outputs/ground_track.gif")
