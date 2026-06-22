import matplotlib.pyplot as plt

orbits_config = [
    dict(label="LEO",    a=1.1, e=0.02, i=30.0,  Omega=0, w=0,   color="#8be9fd"),
    dict(label="GEO",    a=1.0, e=0.00, i=0.0,   Omega=0, w=0,   color="#a6e22e"),
    dict(label="Polar",  a=1.1, e=0.01, i=90.0,  Omega=0, w=0,   color="#ff5555"),
    dict(label="Molniya",a=1.0, e=0.74, i=63.4,  Omega=0, w=270, color="#ffb86c"),
]

def apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor": "#1a1b26",
        "axes.facecolor": "#1a1b26",
        "axes.edgecolor": "#3b4261",
        "axes.labelcolor": "#f8f8f2",
        "text.color": "#f8f8f2",
        "xtick.color": "#565f89",
        "ytick.color": "#565f89",
        "legend.facecolor": "#24253a",
        "legend.edgecolor": "#3b4261",
    })
