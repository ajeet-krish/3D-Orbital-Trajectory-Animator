"""Generate LEO animated GIF using the orbital package."""

import matplotlib.pyplot as plt
from orbital.animate import animate_leo_with_velocity
from orbital.config import apply_dark_theme

apply_dark_theme()

ani = animate_leo_with_velocity()
ani.save("outputs/leo_animated.gif", writer="pillow", fps=30)
plt.close()
print("saved outputs/leo_animated.gif")
