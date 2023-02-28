"""Interactive simulation for camera detection.

This script contains an interactive simulation for the camera detection
capabilities, granting the user the ability to explore the interaction of the
camera position, orientation, focal angle and distance.

Attributes:
    MODES (Dict[str, float]): dictionary containing all possible parameters to
        modify.
    BOUNDARIES (Dict[str, Tuple[float, float]]): dictionary containing the
        boundaries for each parameter.
    INCREMENT (float): increment to apply to each parameter.
    PLOT_REFRESH_RATE (float): time to wait between each plot refresh.

Authors:
    Paulo Sanchez (@erlete)
"""


import json
from math import pi
from typing import Dict, Tuple

import matplotlib
import matplotlib.pyplot as plt
from bidimensional import Coordinate

from fs_mapping_tools.track.cones import Cone, ConeArray
from fs_mapping_tools.vehicle.camera import Camera

MODES: Dict[str, float] = {
    "x": 0.0,
    "y": 0.0,
    "orientation": 0.0,
    "angle": pi / 2,
    "distance": 1.0
}

BOUNDARIES: Dict[str, Tuple[float, float]] = {
    "x": (-100.0, 100.0),
    "y": (-100.0, 100.0),
    "orientation": (0.0, 2 * pi),
    "angle": (pi / 10, (3 / 4) * pi),
    "distance": (1.0, 10.0)
}

INCREMENT: float = 0.1
PLOT_REFRESH_RATE: float = 0.01

mode = "orientation"


def on_press(event: matplotlib.backend_bases.Event) -> None:
    """Handle key press events.

    Args:
        event (matplotlib.backend_bases.Event): event to handle.
    """
    global mode

    # Exit:
    if event.key == "escape":
        exit()

    # Mode selection:
    if event.key == 'x':
        mode = 'x'

    elif event.key == 'y':
        mode = 'y'

    elif event.key == 'o':
        mode = "orientation"

    elif event.key == 'a':
        mode = "angle"

    elif event.key == 'd':
        mode = "distance"

    # Parameter modification:
    if event.key == "up":
        if (
            BOUNDARIES[mode][0]
            <= MODES[mode] + INCREMENT
            <= BOUNDARIES[mode][1]
        ):
            MODES[mode] += INCREMENT

    elif event.key == "down":
        if (
            BOUNDARIES[mode][0]
            <= MODES[mode] - INCREMENT
            <= BOUNDARIES[mode][1]
        ):
            MODES[mode] -= INCREMENT


# Data reading:
with open(
    "tests/modular/vehicle/camera/interactive_sim.json",
    mode='r',
    encoding="utf-8"
) as f:
    data = json.load(f)

line_1 = ConeArray(*[
    Cone(Coordinate(x_, y_), "blue")
    for x_, y_ in zip(data["line_1"]["x"], data["line_1"]["y"])
])

line_2 = ConeArray(*[
    Cone(Coordinate(x_, y_), "yellow")
    for x_, y_ in zip(data["line_2"]["x"], data["line_2"]["y"])
])

# Simulation loop:
while True:
    plt.cla()
    plt.gcf().canvas.mpl_connect("key_press_event", on_press)

    camera = Camera(
        Coordinate(MODES["x"], MODES["y"]),
        orientation=MODES["orientation"],
        focal_angle=MODES["angle"],
        focal_length=MODES["distance"]
    )

    line_1.plot()
    line_2.plot()
    camera.plot()

    camera.detect(line_1, line_2)
    for array in camera.detected:
        for cone in array.cones:
            cone.position.plot(color="green")

    plt.xlim(
        camera.position.x - (camera.focal_length + 5),
        camera.position.x + (camera.focal_length + 5)
    )
    plt.ylim(
        camera.position.y - (camera.focal_length + 5),
        camera.position.y + (camera.focal_length + 5)
    )
    plt.grid(True)
    plt.axis("equal")
    plt.pause(PLOT_REFRESH_RATE)
