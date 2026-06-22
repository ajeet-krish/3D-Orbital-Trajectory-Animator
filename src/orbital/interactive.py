import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

from .core import compute_orbit, draw_earth


def interactive_orbit(a, e, i, Omega, w):
    pos, _, _ = compute_orbit(a=a, e=e, i=i, Omega=Omega, w=w, n_orbits=2, n_points=300)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    limit = max(pos.max() * 1.4, 1.5)
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

    draw_earth(ax, radius=1.0, color="#ff79c6", alpha=0.4)

    ax.plot(pos[:, 0], pos[:, 1], pos[:, 2], color="#8be9fd", linewidth=2, alpha=0.9)
    ax.scatter(
        pos[0, 0], pos[0, 1], pos[0, 2],
        c="white", s=30, marker="o", label="Start",
    )

    ax.set_title(
        f"Orbit: a={a:.2f}, e={e:.2f}, i={i:.0f}°",
        color="white", fontsize=13, fontweight="bold",
    )
    plt.tight_layout()
    plt.show()


def make_explorer():
    a_slider = widgets.FloatSlider(
        value=1.0, min=0.8, max=2.0, step=0.05,
        description="a (semi-major)", style={"description_width": "initial"},
        layout=widgets.Layout(width="400px"),
    )
    e_slider = widgets.FloatSlider(
        value=0.3, min=0.0, max=0.9, step=0.01,
        description="e (eccentricity)", style={"description_width": "initial"},
        layout=widgets.Layout(width="400px"),
    )
    i_slider = widgets.FloatSlider(
        value=30, min=0, max=180, step=1,
        description="i (inclination)", style={"description_width": "initial"},
        layout=widgets.Layout(width="400px"),
    )
    Omega_slider = widgets.FloatSlider(
        value=0, min=0, max=360, step=5,
        description="Ω (RAAN)", style={"description_width": "initial"},
        layout=widgets.Layout(width="400px"),
    )
    w_slider = widgets.FloatSlider(
        value=0, min=0, max=360, step=5,
        description="ω (arg. periapsis)", style={"description_width": "initial"},
        layout=widgets.Layout(width="400px"),
    )

    ui = widgets.VBox([
        widgets.HBox([a_slider, e_slider]),
        widgets.HBox([i_slider, Omega_slider]),
        widgets.HBox([w_slider]),
    ])

    out = widgets.interactive_output(
        interactive_orbit,
        {"a": a_slider, "e": e_slider, "i": i_slider, "Omega": Omega_slider, "w": w_slider},
    )
    display(ui, out)
