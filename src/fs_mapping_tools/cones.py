"""Cone representation classes.

Author:
    Paulo Sanchez (@erlete)
"""

import matplotlib
from bidimensional import Coordinate
from matplotlib import pyplot as plt

from .config import CONES


class Cone:
    """Cone representation class.

    This class represents a Formula Student cone. It supports any of the four
    types of cones defined in the FS rules: yellow, orange, orange-big and
    blue. It also supports plotting the cone in a `matplotlib` figure.

    Attributes:
        x (float): x coordinate of the cone.
        y (float): y coordinate of the cone.
        position (Coordinate): coordinate representing the cone's position.
        type (str): type of cone. Must be one of the following: "yellow",
            "orange", "orange-big" or "blue".
    """

    def __init__(self, position: Coordinate, type: str) -> None:
        """Initialize a cone instance.

        Args:
            position (Coordinate): coordinate representing the cone's
                position.
            type (str): type of cone. Must be one of the following: "yellow",
                "orange", "orange-big" or "blue".
        """
        self.position = position
        self.type = type

    @property
    def x(self) -> float:
        """Get the x coordinate of the cone.

        Returns:
            float: x coordinate of the cone.
        """
        return self.position.x

    @property
    def y(self) -> float:
        """Get the y coordinate of the cone.

        Returns:
            float: y coordinate of the cone.
        """
        return self.position.y

    @property
    def position(self) -> Coordinate:
        """Get the coordinate representing the cone's position.

        Returns:
            Coordinate: coordinate representing the cone's position.
        """
        return self._position

    @position.setter
    def position(self, position: Coordinate) -> None:
        """Set the coordinate representing the cone's position.

        Args:
            position (Coordinate): coordinate representing the cone's
                position.

        Raises:
            TypeError: if `position` is not a `Coordinate` instance.
        """
        if not isinstance(position, Coordinate):
            raise TypeError("position must be a Coordinate")

        self._position = position

    @property
    def type(self) -> str:
        """Get the type of cone.

        Returns:
            str: type of cone.
        """
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """Set the type of cone.

        Args:
            value (str): type of cone. Must be one of the following: "yellow",
                "orange", "orange-big" or "blue".

        Raises:
            TypeError: if `value` is not a string.
            ValueError: if `value` is not one of the allowed cone types.
        """
        if not isinstance(value, str):
            raise TypeError("value must be a string")

        elif value not in CONES:
            raise ValueError(
                f"value must be one of the following types: "
                f"{CONES.values()}"
            )

        self._type = value

    def plot(self, ax: matplotlib.axes.Axes = plt.gca(),
             detail: bool = False) -> None:
        """Plot the cone in a `matplotlib` figure.

        Args:
            ax (matplotlib.axes.Axes, optional): the ax to plot the cone in.
                Defaults to plt.gca().
            detail (bool, optional): whether to plot all the details of the
                cone (can affect performance). Defaults to False.
        """
        ax.plot(
            self.position.x, self.position.y,
            color=CONES[self.type]["colors"]["base"],
            marker='o', ms=CONES[self.type]["size"]["base"]
        )

        if detail:
            ax.plot(
                self.position.x, self.position.y,
                color=CONES[self.type]["colors"]["strip_low"],
                marker='o', ms=CONES[self.type]["size"]["strip_low"]
            )
            ax.plot(
                self.position.x, self.position.y,
                color=CONES[self.type]["colors"]["mid"],
                marker='o', ms=CONES[self.type]["size"]["mid"]
            )
            ax.plot(
                self.position.x, self.position.y,
                color=CONES[self.type]["colors"]["strip_high"],
                marker='o', ms=CONES[self.type]["size"]["strip_high"]
            )
            ax.plot(
                self.position.x, self.position.y,
                color=CONES[self.type]["colors"]["top"],
                marker='o', ms=CONES[self.type]["size"]["top"]
            )
            ax.plot(
                self.position.x, self.position.y,
                color="#ffffff",
                marker='o', ms=CONES[self.type]["size"]["top"] / 2
            )

    def __repr__(self) -> str:
        """Get the raw representation of the cone.

        Returns:
            str: raw representation of the cone.
        """
        return f"Cone({self.position.x}, {self.position.y}, {self.type})"

    def __str__(self) -> str:
        """Get the string representation of the cone.

        Returns:
            str: string representation of the cone.
        """
        return f"Cone({self.position.x}, {self.position.y}, {self.type})"
