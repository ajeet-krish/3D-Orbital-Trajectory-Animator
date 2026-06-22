import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from .core import compute_orbit, draw_earth, setup_3d_axes
from .arrow3d import Arrow3D


def animate_orbit(fig, ax, pos, frame_skip=2, trail_length=40, interval=30):
    n_frames = len(pos)

    (sat_dot,) = ax.plot(
        [], [], [], "wo", markersize=8, markeredgecolor="white", markeredgewidth=0.5
    )
    (trail_line,) = ax.plot([], [], [], color="#8be9fd", linewidth=1.2, alpha=0.8)
    trail_scat = ax.scatter(
        [], [], [], c=[], cmap="plasma", alpha=0.5, s=8, vmin=0, vmax=1
    )

    n_trail = trail_length

    def setup_axes():
        ax.set_xlim(pos[:, 0].min() * 1.3, pos[:, 0].max() * 1.3)
        ax.set_ylim(pos[:, 1].min() * 1.3, pos[:, 1].max() * 1.3)
        ax.set_zlim(pos[:, 2].min() * 1.3, pos[:, 2].max() * 1.3)
        ax.set_box_aspect([1, 1, 1])
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor("#3b4261")
        ax.yaxis.pane.set_edgecolor("#3b4261")
        ax.zaxis.pane.set_edgecolor("#3b4261")

    setup_axes()

    def init():
        trail_line.set_data([], [])
        trail_line.set_3d_properties([])
        sat_dot.set_data([], [])
        sat_dot.set_3d_properties([])
        return trail_line, sat_dot

    def update(frame):
        i = frame * frame_skip
        if i >= n_frames:
            i = n_frames - 1

        sat_dot.set_data([pos[i, 0]], [pos[i, 1]])
        sat_dot.set_3d_properties([pos[i, 2]])

        start = max(0, i - n_trail)
        trail_pts = pos[start : i + 1]
        trail_line.set_data(trail_pts[:, 0], trail_pts[:, 1])
        trail_line.set_3d_properties(trail_pts[:, 2])

        trail_scat.set_offsets(trail_pts[:, :2])
        trail_scat.set_3d_properties(trail_pts[:, 2], "z")
        ages = np.linspace(0, 1, len(trail_pts))
        trail_scat.set_array(ages)

        return trail_line, sat_dot, trail_scat

    n_anim_frames = n_frames // frame_skip
    anim = animation.FuncAnimation(
        fig, update, frames=n_anim_frames,
        init_func=init, interval=interval,
        blit=False, repeat=True,
    )
    return anim


def animate_leo_with_velocity():
    pos, t, ke = compute_orbit(
        a=1.0, per=1.0, e=0.05, i=30.0, Omega=0.0, w=0.0, n_orbits=2, n_points=400
    )

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    setup_3d_axes(ax, pos)
    draw_earth(ax, radius=1.0, color="#ff79c6", alpha=0.5)
    ax.plot(
        pos[:, 0], pos[:, 1], pos[:, 2],
        color="#3b4261", linewidth=0.8, alpha=0.4, label="Full orbit",
    )
    ax.legend(loc="upper right", fontsize=9, facecolor="#24253a", edgecolor="#3b4261")
    ax.set_title("LEO — Animated", color="white", fontsize=14, fontweight="bold")

    (sat,) = ax.plot(
        [], [], [], "wo", markersize=8, markeredgecolor="white", markeredgewidth=1
    )
    (trail,) = ax.plot([], [], [], color="#8be9fd", linewidth=2, alpha=0.9)
    vel_arrow = Arrow3D(
        [0, 0], [0, 0], [0, 0],
        mutation_scale=15, lw=2, arrowstyle="-|>", color="#ff5555", visible=False,
    )
    ax.add_artist(vel_arrow)

    trail_len = 50
    dt = t[1] - t[0]

    def init():
        sat.set_data([], [])
        sat.set_3d_properties([])
        trail.set_data([], [])
        trail.set_3d_properties([])
        vel_arrow.set_visible(False)
        return sat, trail, vel_arrow

    def update(frame):
        sat.set_data([pos[frame, 0]], [pos[frame, 1]])
        sat.set_3d_properties([pos[frame, 2]])

        start = max(0, frame - trail_len)
        trail.set_data(pos[start : frame + 1, 0], pos[start : frame + 1, 1])
        trail.set_3d_properties(pos[start : frame + 1, 2])

        if frame > 1:
            v = (pos[frame] - pos[frame - 1]) / dt
            v_norm = v / (np.linalg.norm(v) + 1e-12)
            arrow_scale = 0.3
            tip = pos[frame] + v_norm * arrow_scale
            vel_arrow.set_positions(pos[frame], tip)
            vel_arrow.set_visible(True)
        else:
            vel_arrow.set_visible(False)

        return sat, trail, vel_arrow

    anim = animation.FuncAnimation(
        fig, update, frames=len(pos),
        init_func=init, interval=30,
        blit=False, repeat=True,
    )
    return anim


def animate_multi_orbit(orbit_data, n_frames=200, interval=30):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")

    limit = 1.8
    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel("X (Earth Radii)")
    ax.set_ylabel("Y (Earth Radii)")
    ax.set_zlabel("Z (Earth Radii)")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("#3b4261")
    ax.yaxis.pane.set_edgecolor("#3b4261")
    ax.zaxis.pane.set_edgecolor("#3b4261")
    ax.tick_params(colors="#565f89")
    ax.set_title(
        "Multi-Orbit Animation — All Regimes",
        color="white", fontsize=14, fontweight="bold",
    )

    draw_earth(ax, radius=1.0, color="#ff79c6", alpha=0.4)

    colors = ["#8be9fd", "#a6e22e", "#ff5555", "#ffb86c"]
    dots = {}
    trails = {}

    for idx, (label, pos) in enumerate(orbit_data.items()):
        n_pts = len(pos)
        step = max(1, n_pts // n_frames)
        pos_sampled = pos[::step][:n_frames]

        (dot,) = ax.plot(
            [], [], [],
            "o", color=colors[idx], markersize=7,
            markeredgecolor="white", markeredgewidth=0.5, label=label,
        )
        (trail,) = ax.plot([], [], [], color=colors[idx], linewidth=1.2, alpha=0.6)
        dots[label] = dict(dot=dot, pos=pos_sampled)
        trails[label] = trail

    ax.legend(loc="upper right", fontsize=9, facecolor="#24253a", edgecolor="#3b4261")

    def update(frame):
        artists = []
        for label, d in dots.items():
            i = min(frame, len(d["pos"]) - 1)
            d["dot"].set_data([d["pos"][i, 0]], [d["pos"][i, 1]])
            d["dot"].set_3d_properties([d["pos"][i, 2]])

            trail_len = 30
            start = max(0, i - trail_len)
            trails[label].set_data(
                d["pos"][start : i + 1, 0], d["pos"][start : i + 1, 1]
            )
            trails[label].set_3d_properties(d["pos"][start : i + 1, 2])
            artists.extend([d["dot"], trails[label]])
        return artists

    anim = animation.FuncAnimation(
        fig, update, frames=n_frames,
        interval=interval, blit=False, repeat=True,
    )
    return anim


def animate_molniya():
    pos, t, ke = compute_orbit(
        a=1.0, per=1.0, e=0.74, i=63.4,
        Omega=0.0, w=270.0, n_orbits=1, n_points=400,
    )

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    limit = 1.9
    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel("X (Earth Radii)")
    ax.set_ylabel("Y (Earth Radii)")
    ax.set_zlabel("Z (Earth Radii)")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("#3b4261")
    ax.yaxis.pane.set_edgecolor("#3b4261")
    ax.zaxis.pane.set_edgecolor("#3b4261")
    ax.tick_params(colors="#565f89")
    ax.set_title(
        "Molniya Orbit — $e=0.74,\\; i=63.4^\\circ$",
        color="white", fontsize=14, fontweight="bold",
    )
    ax.text2D(
        0.97, 0.95,
        "Apogee dwell over northern hemisphere",
        transform=ax.transAxes, color="#ffb86c",
        fontsize=10, style="italic", ha="right", va="top",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="#24253a", edgecolor="#ffb86c", linewidth=0.5,
        ),
    )

    draw_earth(ax, radius=1.0, color="#ff79c6", alpha=0.5)

    (dark_line,) = ax.plot(
        pos[:, 0], pos[:, 1], pos[:, 2],
        color="#3b4261", linewidth=0.6, alpha=0.4,
    )

    (sat,) = ax.plot(
        [], [], [],
        "o", color="#ffb86c", markersize=9,
        markeredgecolor="white", markeredgewidth=0.5,
    )

    (trail,) = ax.plot([], [], [], color="#ffb86c", linewidth=2, alpha=0.85)

    trail_len = 60

    def init():
        sat.set_data([], [])
        sat.set_3d_properties([])
        trail.set_data([], [])
        trail.set_3d_properties([])
        return sat, trail

    def update(frame):
        sat.set_data([pos[frame, 0]], [pos[frame, 1]])
        sat.set_3d_properties([pos[frame, 2]])

        start = max(0, frame - trail_len)
        trail.set_data(pos[start : frame + 1, 0], pos[start : frame + 1, 1])
        trail.set_3d_properties(pos[start : frame + 1, 2])
        return sat, trail

    anim = animation.FuncAnimation(
        fig, update, frames=len(pos),
        init_func=init, interval=30,
        blit=False, repeat=True,
    )
    return anim
