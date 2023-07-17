"""Simulation for car plotting.

This script contains a simple simulation of the car plotting procedure and
allows visualization of the real plotted model.

Attributes:
    CAR (Car): the car model used for the simulation.
    ANGULAR_VALUES (np.ndarray): sequence of angular values that both
        orientation and steering parameters will take.

Authors:
    Paulo Sanchez (@erlete)
"""

from math import pi
from time import perf_counter as pc

import matplotlib.pyplot as plt
import numpy as np

from fs_mapping_tools import Car

CAR: Car = Car.fsuk_adsdv_camera()
ANGULAR_VALUES: np.ndarray = np.arange(0, pi / 2, 0.05)

times = []
for i in ANGULAR_VALUES:
    # Orientation and steering settings:
    CAR.state.orientation = 0
    CAR.state.steering = 0
    CAR.structure.camera.orientation = 0

    CAR.state.orientation += i
    CAR.state.steering += i
    CAR.structure.camera.orientation += i

    # Plot settings:
    plt.gcf().canvas.mpl_connect(
        "key_press_event",
        lambda event: exit(0) if event.key == "escape" else None
    )

    # Global view:
    plt.subplot(1, 2, 1)
    plt.cla()

    cron = pc()
    CAR.plot(color="black", linestyle="solid", ms=0)
    result = pc() - cron
    times.append(result)

    plt.grid(True)
    plt.axis("equal")

    # Local view:
    plt.subplot(1, 2, 2)
    plt.cla()

    CAR.plot(color="black", linestyle="solid", ms=0)

    plt.grid(True)
    plt.axis("equal")
    plt.xlim(
        CAR.state.position.x - CAR.structure.direction.wheelbase * 1.5,
        CAR.state.position.x + CAR.structure.direction.wheelbase * 1.5
    )
    plt.ylim(
        CAR.state.position.y - CAR.structure.direction.wheelbase * 1.5,
        CAR.state.position.y + CAR.structure.direction.wheelbase * 1.5
    )

    plt.pause(0.01)

# Statistics summary:
print(f"""Plotting statistics:

MAX: {max(times)}s.
MIN: {min(times)}s.
AVG: {sum(times) / len(times)}s.
""")

# Timing visualization:
plt.close("all")
plt.cla()
plt.plot(ANGULAR_VALUES, times, ".-")
plt.grid(True)
plt.axis("auto")
plt.show()
