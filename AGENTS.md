# AGENTS.md — 3D Orbital Trajectory Animator

Project guide for AI coding assistants working on this repository.

---

## Project Overview

A single-page HTML portfolio site that demonstrates Keplerian orbit mechanics using Python-generated 3D animations. Targeted at astrodynamics/engineering job applications.

**Live site:** https://ajeet-krish.github.io/3D-Orbital-Trajectory-Animator/

---

## Repository Structure

```
├── docs/                    # GitHub Pages site
│   ├── index.html           # Single-page HTML portfolio (all content inline)
│   ├── custom.css           # Space-themed dark stylesheet
│   └── outputs/             # GIFs for the site (copied from project root)
├── src/
│   ├── orbital/             # Python package — importable orbital mechanics
│   │   ├── __init__.py      #   Clean re-exports
│   │   ├── core.py          #   compute_orbit(), draw_earth(), setup_3d_axes()
│   │   ├── animate.py       #   All animate_*() functions
│   │   ├── arrow3d.py       #   Arrow3D for velocity vectors
│   │   ├── config.py        #   orbits_config, apply_dark_theme()
│   │   ├── sweep.py         #   Parameter sweep (standalone runner module)
│   │   └── interactive.py   #   ipywidgets explorer (notebook-only)
│   └── orbit.ipynb          # Original notebook (kept for experimentation)
├── scripts/                 # Standalone GIF generators (import orbital)
│   ├── hohmann.py
│   ├── j2_precession.py
│   ├── ground_track.py
│   ├── leo.py
│   ├── molniya.py
│   └── multi_orbit.py
├── outputs/                 # Generated GIFs (gitignored)
├── pyproject.toml           # Dependencies & package config
├── uv.lock                  # Lockfile
├── .python-version          # Python version pin
├── AGENTS.md                # This file
└── README.md
```

---

## Key Files

### docs/index.html
Single ~800-line HTML file containing all 7 sections, navigation, hero, KaTeX math, Prism code blocks, scroll animations, scrollspy, and parallax starfield. No framework, no build step. All JavaScript is inline.

### docs/custom.css
~670 lines. Space-themed dark layout, CSS starfield with twinkling, sticky nav, responsive breakpoint at 900px, KaTeX styling, Prism Tomorrow Night code blocks, infographic orbit cards, scroll-triggered fade-in, scrollspy active link highlighting, parallax star layer.

### src/orbital/ package
Core orbital mechanics code organized into modules:
- **core.py** — Fundamental functions: `compute_orbit()`, `draw_earth()`, `setup_3d_axes()`, `annotate_orbital_elements()`
- **animate.py** — All animation functions: `animate_orbit()`, `animate_leo_with_velocity()`, `animate_multi_orbit()`, `animate_molniya()`
- **arrow3d.py** — `Arrow3D(FancyArrowPatch)` for 3D velocity vectors
- **config.py** — `orbits_config` list (4 orbit types), `apply_dark_theme()` for matplotlib rcParams
- **sweep.py** — Parameter sweep that generates `parameter_sweep.gif` (runs as `__main__`)
- **interactive.py** — ipywidgets explorer (for Jupyter, not used by site)

### scripts/ directory
Each script imports from `orbital` package and saves a GIF:
```bash
uv run python3 scripts/hohmann.py
```

---

## Build & Run Commands

```bash
# Install dependencies
uv sync
uv pip install -e .

# Regenerate a single GIF
uv run python3 scripts/hohmann.py

# Regenerate all GIFs
for script in scripts/*.py; do uv run python3 "$script"; done

# Copy regenerated GIFs to docs
cp outputs/*.gif docs/outputs/

# Run the notebook
uv run jupyter notebook src/orbit.ipynb

# Lint/type-check
uv run ruff check src/orbital/ scripts/
```

---

## Plot Style Canon

All plots follow a uniform dark theme defined in `src/orbital/config.py` (`apply_dark_theme()`) and `src/orbital/core.py` (`setup_3d_axes()`):

| Element | Value |
|---------|-------|
| Figure facecolor | `#1a1b26` |
| Axes facecolor | `#1a1b26` |
| Axes edgecolor | `#3b4261` |
| Labels color | `#f8f8f2` |
| Tick color | `#565f89` |
| 3D pane fill | `False` |
| 3D pane edge | `#3b4261` |
| Earth grid | `color="#ff79c6"`, `alpha=0.5` |
| Reference orbit | `color="#3b4261"`, `linewidth=0.6`, `alpha=0.4` |
| Satellite dot | `"o"`, `markersize=7-9`, `markeredgecolor="white"`, `markeredgewidth=0.5` |
| Trail | orbit color, `linewidth=2`, `alpha=0.6-0.9` |
| Title | `color="white"`, `fontsize=14`, `fontweight="bold"` |
| Legend | `loc="upper right"`, `fontsize=9`, `facecolor="#24253a"`, `edgecolor="#3b4261"` |
| Animation interval | `30` |
| Save writer | `"pillow"` |
| Save fps | `30` |

---

## Site Architecture

- **7 sections** in order: Theory → LEO → Hohmann → Molniya → Regimes → Sweep → Summary
- **Sticky top nav** with scrollspy (IntersectionObserver, rootMargin: `-40% 0px -55% 0px`)
- **Scroll-triggered fade-in** (IntersectionObserver, threshold: 0.08)
- **Parallax starfield**: CSS pseudo-element base + JS-generated layer with `translateY(scrollY * 0.08)`
- **2×2 infographic cards** with inline SVG orbit shapes
- **KaTeX** for math rendering (auto-render with `$$` display, `$` inline)
- **Prism.js** Tomorrow Night for Python syntax highlighting with copy-to-clipboard
- **GitHub Pages** publishes from `docs/` directory

---

## Content Guidelines

- **No em dashes** — they read as AI-generated
- **Conversational but technically precise** — accessible to casual readers, accurate for engineers
- **Solid title color** (`#e2e8f0`), no gradients
- **Collapsible `<details>` code blocks** show only key code, not all notebook cells
- **No ipywidgets section** in the HTML (dead in static rendering)
- **Footer links** use `[ GitHub Repo ]` format with brackets

---

## Common Tasks

### Add a new section
1. Write the `animate_*()` function in `src/orbital/animate.py`
2. Create a generator script in `scripts/`
3. Run the script to produce the GIF
4. Add a `<section id="new-section" class="section">` block in `docs/index.html` (before Summary)
5. Add a nav link in the `<div class="nav-entries">` block
6. Update section numbers for all subsequent sections

### Change section order
1. Move the `<section>` block in `docs/index.html`
2. Reorder nav links in `<div class="nav-entries">`
3. Update all `section-number` spans sequentially

### Regenerate all GIFs after code changes
```bash
uv run python3 scripts/leo.py
uv run python3 scripts/molniya.py
uv run python3 scripts/multi_orbit.py
uv run python3 scripts/hohmann.py
uv run python3 scripts/j2_precession.py
uv run python3 scripts/ground_track.py
uv run python3 src/orbital/sweep.py
cp outputs/*.gif docs/outputs/
```

### Deploy
Push to `main` branch. GitHub Pages auto-deploys from `docs/`.
