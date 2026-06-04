# 3D Orbital Trajectory Animator

[![Python](https://img.shields.io/badge/Python-3.14-blue)](#)
[![PyAstronomy](https://img.shields.io/badge/PyAstronomy-0.25-orange)](#)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3D-orange)](#)

Interactive 3D visualization and animation of Keplerian orbits using the two-body solution, built with Python. 

## Demo

![Multi-Orbit](outputs/multi_orbit.gif)
  *Four orbit regimes simultaneously: LEO, GEO, Polar, Molniya*

![Molniya Orbit](outputs/molniya.gif)
  *Highly elliptical Molniya orbit (e=0.74, i=63.4°), apogee dwell over northern hemisphere*

![LEO Animated](outputs/leo_animated.gif)
  *Low Earth Orbit with velocity vector and comet trail*

## Engineering Concepts

| Concept | Description |
|---------|-------------|
| Two-Body Problem | Analytical solution via Kepler's equation |
| Keplerian Elements | Semi-major axis, eccentricity, inclination, RAAN, argument of periapsis |
| Critical Inclination | Molniya orbit at 63.4° eliminates apsidal precession |
| Apogee Dwell | Satellite slows near apogee (Kepler's second law) |
| Vis-Viva Equation | $v^2 = \mu(2/r - 1/a)$ - velocity at any orbital radius |
| Orbit Regimes | LEO, GEO, Polar, and Molniya - each with distinct mission profiles |

## Features

- **3D visualization** with wireframe Earth, coordinate axes, and orbital element annotations
- **Animated satellite motion** with fading comet trail and real-time velocity vector
- **Multiple orbit types**: overlay LEO, GEO, Polar, and Molniya orbits simultaneously
- **Interactive parameter explorer**: tweak $a$, $e$, $i$, $\Omega$, $\omega$ in real time (Jupyter only)
- **GIF export**: high-quality animations ready for portfolio embedding
- **Quarto-ready notebook**: standalone HTML with table of contents, code folding, and syntax highlighting

## How It Works

The notebook uses PyAstronomy's `KeplerEllipse` class to solve Kepler's equation and generate position vectors. Matplotlib's `FuncAnimation` iterates through the position array frame-by-frame, with `PillowWriter` exporting the result as a GIF.

```python
ke = pyasl.KeplerEllipse(a=1.0, per=1.0, e=0.74, i=63.4, Omega=0.0, w=270.0)
pos = ke.xyzPos(np.linspace(0, 4, 400))
```

## Getting Started

### Prerequisites

- Python ≥ 3.14
- uv (recommended) or pip

### Installation

```bash
uv sync
```

### Running the Notebook

```bash
uv run jupyter notebook orbit.ipynb
```

Or with Quarto:

```bash
quarto render orbit.ipynb
```

## Project Structure

```
├── orbit.ipynb           # Main notebook (20 cells + YAML frontmatter)
├── orbit.css             # Custom theme for Quarto HTML output
├── outputs/              # Generated animation GIFs
│   ├── leo_animated.gif
│   ├── molniya.gif
│   └── multi_orbit.gif
├── pyproject.toml        # Dependencies & project config
├── uv.lock               # Lockfile
├── .python-version       # Python version pin
└── README.md
```

## Notebook Contents

| Cells | Content |
|-------|---------|
| 0 | YAML frontmatter (Quarto config: TOC, code-fold, dark theme) |
| 1-5 | Setup: imports, Dracula rcParams, Earth wireframe, orbit computation, animation factory |
| 6-9 | LEO orbit: static annotated plot → animation + GIF display |
| 10-13 | Multi-orbit comparison: LEO, GEO, Polar, Molniya → animation + GIF display |
| 14-16 | Molniya deep dive: critical inclination, apogee dwell → animation + GIF display |
| 17-18 | Interactive parameter explorer (ipywidgets — Jupyter only) |
| 19 | Summary & references |

## References

- [PyAstronomy Documentation](https://pyastronomy.readthedocs.io/)
- Vallado, D. A. — *Fundamentals of Astrodynamics and Applications*
- Bate, R. R., Mueller, D. D., & White, J. E. — *Fundamentals of Astrodynamics*
- [Matplotlib 3D Animation](https://matplotlib.org/stable/gallery/index.html#animation)
