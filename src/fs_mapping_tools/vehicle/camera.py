"""Container module for camera representation classes.

This module contains all definitions of classes and utilities used to represent
a camera object on track.

Authors:
    Paulo Sanchez (@erlete)
"""

from math import cos, pi, sin
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
from bidimensional import Coordinate
from bidimensional.polygons import Triangle

from ..track.cones import Cone


class Camera:
    """Camera representation class.

    This class represents a camera element, with a specific position,
    orientation, focal angle and lenght. It is used to represent the onboard
    camera that provides with track elements' detection.

    Attributes:
        position (Coordinate): position of the center of the camera.
        orientation (float): orientation of the camera lens.
        focal_angle (float): focal angle of the camera lens.
        focal_length (float): focal distance of the camera lens.
    """

    def __init__(self, position: Coordinate, orientation: float,
                 focal_angle: float, focal_length: float):
        """Initialize a Camera instance.

        Args:
            position (Coordinate): position of the center of the camera.
            orientation (float): orientation of the camera lens.
            focal_angle (float): focal angle of the camera lens.
            focal_length (float): focal distance of the camera lens.
        """
        self.position = position
        self.orientation = orientation
        self.focal_angle = focal_angle
        self.focal_length = focal_length
        self.set_detection_area()

    def set_detection_area(self) -> None:
        """Determine the detection area of the camera.

        This method determines the detection area of the camera, which is
        represented by a combination of triangles.
        """
        left_rot = self.orientation - self.focal_angle / 2
        right_rot = self.orientation + self.focal_angle / 2

        radius = self.position + Coordinate(
            cos(self.orientation) * self.focal_length,
            sin(self.orientation) * self.focal_length
        )
        left_boundary = self.position + Coordinate(
            cos(left_rot) * self.focal_length,
            sin(left_rot) * self.focal_length
        )
        right_boundary = self.position + Coordinate(
            cos(right_rot) * self.focal_length,
            sin(right_rot) * self.focal_length
        )

        self.detection_area = (
            Triangle(
                self.position,
                left_boundary,
                right_boundary
            ), Triangle(
                left_boundary,
                right_boundary,
                radius
            )
        )

    def plot(self, ax: matplotlib.axes.Axes = None) -> None:
        """Plot the camera and detection range.

        Args:
            ax (matplotlib.axes.Axes, optional): ax to plot the figure in.
                Defaults to `plt.gca()` if None is passed as value.
        """
        ax = ax if ax is not None else plt.gca()

        for triangle in self.detection_area:
            triangle.plot(ax=ax, annotate=False)

        self.position.plot(ax=ax, annotate=False)

    def __contains__(self, element: Any):
        """Determine whether an element is within the detection area.

        Args:
            element (Any): the element to be checked.

        Returns:
            bool: True if the element is within the detection area, False
                otherwise.

        Raises:
            TypeError: if the element is not a Coordinate or Cone instance.
        """
        if not isinstance(element, Cone):
            raise TypeError("element must be a Cone instance.")

        return any(
            element.position in triangle
            for triangle in self.detection_area
        )
