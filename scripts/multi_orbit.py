"""Generate multi-orbit comparison GIF using the orbital package."""

import matplotlib.pyplot as plt
from orbital.core import compute_orbit
from orbital.animate import animate_multi_orbit
from orbital.config import apply_dark_theme, orbits_config

apply_dark_theme()

orbit_data = {}
for cfg in orbits_config:
    pos, _, _ = compute_orbit(
        a=cfg["a"], e=cfg["e"], i=cfg["i"],
        Omega=cfg["Omega"], w=cfg["w"],
        n_orbits=2, n_points=400,
    )
    orbit_data[cfg["label"]] = pos

ani = animate_multi_orbit(orbit_data, n_frames=200, interval=30)
ani.save("outputs/multi_orbit.gif", writer="pillow", fps=30)
plt.close()
print("saved outputs/multi_orbit.gif")
