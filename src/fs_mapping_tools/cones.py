"""Cone representation classes.

Author:
    Paulo Sanchez (@erlete)
"""

from typing import Tuple

import matplotlib
import numpy as np
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
                "value must be one of the following types: "
                + ', '.join(f"\"{key}\"" for key in list(CONES.keys())[:-1])
                + f" or \"{list(CONES.keys())[-1]}\""
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

    def __eq__(self, other: object) -> bool:
        """Check if two cones are equal.

        Args:
            other (object): the other cone to compare with.

        Returns:
            bool: whether the two cones are equal.
        """
        if not isinstance(other, Cone):
            raise TypeError("can only compare Cone instances")

        return self.position == other.position and self.type == other.type

    def __ne__(self, other: object) -> bool:
        """Check if two cones are not equal.

        Args:
            other (object): the other cone to compare with.

        Returns:
            bool: whether the two cones are not equal.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Get the hash of the cone.

        Returns:
            int: hash of the cone.
        """
        return hash((self.position, self.type))

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


class ConeArray:
    """Cone array representation class.

    This class is used to represent an ordered group of cones. It supports any
    of the four types of cones defined in the FS rules: "yellow", "orange",
    "orange-big" and "blue", but all cones must be of the same type.

    Attributes:
        cones (Tuple[Cone]): tuple of cones in the array.
        type (str): type of cones in the array. Must be one of the following:
            "yellow", "orange", "orange-big" or "blue".
    """

    def __init__(self, *cones: Cone) -> None:
        """Initialize a cone array instance.

        Args:
            cones (Cone): cones in the array. Must be of the same type.
        """
        self.cones = cones

    @property
    def cones(self) -> Tuple[Cone, ...]:
        """Get the cones in the array.

        Returns:
            Tuple[Cone, ...]: tuple of cones in the array.
        """
        return self._cones

    @cones.setter
    def cones(self, cones: Tuple[Cone]) -> None:
        """Set the cones in the array.

        Args:
            cones (Tuple[Cone]): tuple of cones in the array. Must be of the
                same type.

        Raises:
            TypeError: if `cones` is not an iterable sequence.
            TypeError: if any element in `cones` is not a `Cone` instance.
            ValueError: if `cones` is not of the same type.
        """
        if not isinstance(cones, (tuple, list, set, np.ndarray)):
            raise TypeError("cones must be an iterable sequence")

        if not all(isinstance(cone, Cone) for cone in cones):
            raise TypeError(
                "all elements in the iterable sequence must be Cone instances"
            )

        if len(set(cone.type for cone in cones)) > 1:
            raise ValueError("all cones must be of the same type")

        self._cones = cones

    @property
    def type(self) -> str:
        """Get the type of cones in the array.

        Returns:
            str: type of cones in the array.
        """
        return self.cones[0].type
