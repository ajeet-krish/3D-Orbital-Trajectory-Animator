import numpy as np
from PyAstronomy import pyasl


def compute_orbit(
    a=1.0, per=1.0, e=0.0, Omega=0.0, i=0.0, w=0.0, n_orbits=2, n_points=300
):
    ke = pyasl.KeplerEllipse(a=a, per=per, e=e, Omega=Omega, i=i, w=w)
    t = np.linspace(0, n_orbits * per, n_points)
    pos = ke.xyzPos(t)
    return pos, t, ke


def draw_earth(ax, radius=1.0, color="#ff79c6", linewidth=0.6, alpha=0.6):
    n_theta = 20
    n_phi = 20
    theta = np.linspace(0, 2 * np.pi, n_theta)
    phi = np.linspace(-np.pi / 2, np.pi / 2, n_phi)

    for i in range(0, n_phi, 3):
        x = radius * np.cos(phi[i]) * np.cos(theta)
        y = radius * np.cos(phi[i]) * np.sin(theta)
        z = radius * np.sin(phi[i]) * np.ones_like(theta)
        ax.plot(x, y, z, color=color, linewidth=linewidth, alpha=alpha)

    for i in range(0, n_theta, 3):
        x = radius * np.cos(phi) * np.cos(theta[i])
        y = radius * np.cos(phi) * np.sin(theta[i])
        z = radius * np.sin(phi)
        ax.plot(x, y, z, color=color, linewidth=linewidth, alpha=alpha)


def setup_3d_axes(ax, pos):
    limit = pos[:, :3].max() * 1.4
    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    ax.set_box_aspect([1, 1, 1])
    ax.set_facecolor("#1a1b26")
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


def annotate_orbital_elements(ax, pos, ke):
    limit = pos[:, :3].max() * 1.4

    if hasattr(ke, "i"):
        i_deg = ke.i
        i_rad = np.radians(i_deg)
        arc_theta = np.linspace(0, i_rad, 30)
        arc_r = pos.max() * 0.35
        arc_x = arc_r * np.sin(arc_theta)
        arc_z = arc_r * np.cos(arc_theta)
        ax.plot(
            arc_x, np.zeros_like(arc_x), arc_z,
            "--", color="#ff79c6", linewidth=1.5, alpha=0.7,
        )
        ax.text(
            arc_x[-1] * 1.1, 0, arc_z[-1] * 1.1,
            f"$i = {i_deg:.0f}^\\circ$", color="#ff79c6", fontsize=9,
        )

    nn = 50
    node_line = np.linspace(-limit, limit, nn)
    ax.plot(
        node_line, np.zeros(nn), np.zeros(nn),
        color="#ff79c6", linewidth=0.8, linestyle=":", alpha=0.5,
    )
    ax.text(limit * 0.5, 0, 0, r"$\Omega$", color="#ff79c6", fontsize=9)

    ax.scatter(
        0, 0, 0,
        c="#8be9fd", s=80, marker="o",
        edgecolors="#50fa7b", linewidth=1.5, zorder=10, label="Earth",
    )
