"""Generate Molniya animated GIF using the orbital package."""

import matplotlib.pyplot as plt
from orbital.animate import animate_molniya
from orbital.config import apply_dark_theme

apply_dark_theme()

ani = animate_molniya()
ani.save("outputs/molniya.gif", writer="pillow", fps=30)
plt.close()
print("saved outputs/molniya.gif")
