# 3D Orbital Trajectory Animator

[![Python](https://img.shields.io/badge/Python-3.14-blue)](#)
[![PyAstronomy](https://img.shields.io/badge/PyAstronomy-0.25-orange)](#)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3D-orange)](#)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://ajeet-krish.github.io/3D-Orbital-Trajectory-Animator/)

3D Keplerian orbit visualizations and animations using the two-body solution. Covers LEO, GEO, Polar, Molniya, Hohmann transfers, J2 precession, and ground track projection.

**Live site:** https://ajeet-krish.github.io/3D-Orbital-Trajectory-Animator/

---

## Animations

| GIF | What it shows |
|-----|---------------|
| ![multi_orbit](outputs/multi_orbit.gif) | Four orbit regimes animated together: LEO, GEO, Polar, Molniya |
| ![hohmann](outputs/hohmann.gif) | Two-burn Hohmann transfer between circular orbits |
| ![leo_animated](outputs/leo_animated.gif) | LEO with velocity vector and fading trail |
| ![molniya](outputs/molniya.gif) | Molniya orbit (e=0.74, i=63.4°) with apogee dwell |
| ![j2_precession](outputs/j2_precession.gif) | RAAN precession and apsidal precession side by side |
| ![ground_track](outputs/ground_track.gif) | Ground tracks projected onto a 2D map with 3D view |
| ![parameter_sweep](outputs/parameter_sweep.gif) | Eccentricity and inclination sweep |

## Project Structure

```
├── docs/                    # GitHub Pages site
│   ├── index.html           # Single-page portfolio (custom HTML)
│   ├── custom.css           # Space-themed dark stylesheet
│   └── outputs/             # GIFs for the site (copied from project root)
├── src/
│   ├── orbital/             # Python package — core orbital mechanics
│   │   ├── core.py          #   compute_orbit(), draw_earth(), setup_3d_axes()
│   │   ├── animate.py       #   All animate_*() functions
│   │   ├── arrow3d.py       #   Arrow3D for velocity vectors
│   │   ├── config.py        #   orbits_config, apply_dark_theme()
│   │   ├── sweep.py         #   Parameter sweep (standalone runner)
│   │   └── interactive.py   #   ipywidgets explorer (notebook use)
│   └── orbit.ipynb          # Original notebook (kept for experimentation)
├── scripts/                 # Standalone GIF generators (import orbital)
│   ├── hohmann.py
│   ├── j2_precession.py
│   ├── ground_track.py
│   ├── leo.py
│   ├── molniya.py
│   └── multi_orbit.py
├── outputs/                 # Generated GIFs
├── pyproject.toml           # Dependencies & package config
├── uv.lock                  # Lockfile
├── .python-version          # Python version
├── AGENTS.md                # Project guide for AI coding assistants
└── README.md
```

## How It Works

The `orbital` package provides:

- **`core.py`** — `compute_orbit()` wraps `PyAstronomy.KeplerEllipse` to solve Kepler's equation and return 3D position arrays. `draw_earth()` plots a wireframe Earth. `setup_3d_axes()` creates consistent dark-themed 3D axes.
- **`animate.py`** — `FuncAnimation`-based animation functions that iterate through position arrays frame by frame, drawing satellite dots and fading trails.
- **`config.py`** — Shared orbit configurations and matplotlib dark theme.

Each script in `scripts/` imports from the package, calls the relevant function, and saves a GIF via `PillowWriter`.

## Getting Started

### Prerequisites

- Python >= 3.14
- uv (recommended) or pip

### Installation

```bash
uv sync
uv pip install -e .
```

### Regenerate a GIF

```bash
uv run python3 scripts/hohmann.py
```

### Regenerate All GIFs

```bash
for script in scripts/*.py; do uv run python3 "$script"; done
```

### Run the Notebook

```bash
uv run jupyter notebook src/orbit.ipynb
```

## Package API

```python
from orbital.core import compute_orbit, draw_earth, setup_3d_axes
from orbital.animate import animate_leo_with_velocity, animate_molniya
from orbital.config import orbits_config, apply_dark_theme

apply_dark_theme()
pos, t, ke = compute_orbit(a=1.0, e=0.74, i=63.4, Omega=0.0, w=270.0)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
setup_3d_axes(ax, pos)
draw_earth(ax)
ax.plot(pos[:, 0], pos[:, 1], pos[:, 2], color="#8be9fd", linewidth=1.5)
plt.show()
```

## Engineering Concepts Covered

| Concept | Section | Description |
|---------|---------|-------------|
| Two-Body Problem | Theory | Newton's law → Kepler's equation → conic sections |
| Keplerian Elements | Theory | a, e, i, Omega, w, nu — full orbit parameterization |
| Vis-Viva Equation | Theory | v^2 = mu(2/r - 1/a) — velocity at any radius |
| Critical Inclination | Molniya | i = 63.4° eliminates J2 apsidal drift |
| Apogee Dwell | Molniya | Kepler's second law → slow motion at apogee |
| Hohmann Transfer | Hohmann | Fuel-optimal two-burn orbit raising |
| J2 Precession | Molniya | RAAN drift and apsidal precession from Earth's bulge |
| Ground Tracks | Regimes | Latitude/longitude mapping with Earth rotation |
| Orbit Regimes | Regimes | LEO, GEO, Polar, Molniya — mission-specific design |

## References

- [PyAstronomy Documentation](https://pyastronomy.readthedocs.io/)
- Vallado, D. A. — *Fundamentals of Astrodynamics and Applications*
- Bate, R. R., Mueller, D. D., & White, J. E. — *Fundamentals of Astrodynamics*
