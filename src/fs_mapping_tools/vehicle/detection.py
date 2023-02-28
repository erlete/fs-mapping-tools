"""Container module for detection hardware representation classes.

This module contains all definitions of classes and utilities used to represent
both camera and lidar objects on the vehicle.

Authors:
    Paulo Sanchez (@erlete)
"""

from math import cos, sin
from typing import Any, List

import matplotlib
import matplotlib.pyplot as plt
from bidimensional import Coordinate
from bidimensional.polygons import Triangle

from ..track.cones import Cone, ConeArray


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
        self.__ready_to_detect = False

        self.position = position
        self.orientation = orientation
        self.focal_angle = focal_angle
        self.focal_length = focal_length

        self.__ready_to_detect = True
        self._set_detection_area()

    @property
    def position(self) -> Coordinate:
        """Get the position of the camera.

        Returns:
            Coordinate: position of the camera.
        """
        return self._position

    @position.setter
    def position(self, value: Coordinate) -> None:
        """Set the position of the camera.

        Args:
            value (Coordinate): new position of the camera.

        Raises:
            TypeError: if the value is not a Coordinate instance.
        """
        if not isinstance(value, Coordinate):
            raise TypeError("value must be a Coordinate instance.")

        self._position = value

        if self.__ready_to_detect:
            self._set_detection_area()

    @property
    def orientation(self) -> float:
        """Get the orientation of the camera.

        Returns:
            float: orientation of the camera.
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value: float) -> None:
        """Set the orientation of the camera.

        Args:
            value (float): new orientation of the camera.

        Raises:
            TypeError: if the value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError("value must be a float.")

        self._orientation = value

        if self.__ready_to_detect:
            self._set_detection_area()

    @property
    def focal_angle(self) -> float:
        """Get the focal angle of the camera.

        Returns:
            float: focal angle of the camera.
        """
        return self._focal_angle

    @focal_angle.setter
    def focal_angle(self, value: float) -> None:
        """Set the focal angle of the camera.

        Args:
            value (float): new focal angle of the camera.

        Raises:
            TypeError: if the value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError("value must be a float.")

        self._focal_angle = value

        if self.__ready_to_detect:
            self._set_detection_area()

    @property
    def focal_length(self) -> float:
        """Get the focal length of the camera.

        Returns:
            float: focal length of the camera.
        """
        return self._focal_length

    @focal_length.setter
    def focal_length(self, value: float) -> None:
        """Set the focal length of the camera.

        Args:
            value (float): new focal length of the camera.

        Raises:
            TypeError: if the value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError("value must be a float.")

        self._focal_length = value

        if self.__ready_to_detect:
            self._set_detection_area()

    @property
    def detected(self) -> List[ConeArray]:
        """Get the detected cone arrays.

        Returns:
            List[ConeArray]: detected cone arrays.
        """
        return self._detected

    def detect(self, *cone_arrays) -> None:
        """Detect cones inside provided cone arrays.

        This method is used to determine which cones of all provided arrays are
        located inside the detection range.

        Args:
            *cone_arrays (ConeArray, optional): the cone array(s) to detect
                cones from.

        Raises:
            TypeError: if any of the cone arrays is not a ConeArray type.
        """
        if not cone_arrays:
            self._detected = []
        else:
            if not any(isinstance(array, ConeArray) for array in cone_arrays):
                raise TypeError("all cone arrays must be ConeArray types")

            self._detected = [
                ConeArray(
                    *[
                        cone for cone in array
                        if cone in self
                    ]
                ) for array in cone_arrays
            ]

    def _set_detection_area(self) -> None:
        """Determine the detection area of the camera.

        This method determines the detection area of the camera, which is
        represented by a combination of triangles.
        """
        left_rot = self._orientation - self._focal_angle / 2
        right_rot = self._orientation + self._focal_angle / 2

        radius = self._position + Coordinate(
            cos(self._orientation) * self._focal_length,
            sin(self._orientation) * self._focal_length
        )
        left_boundary = self._position + Coordinate(
            cos(left_rot) * self._focal_length,
            sin(left_rot) * self._focal_length
        )
        right_boundary = self._position + Coordinate(
            cos(right_rot) * self._focal_length,
            sin(right_rot) * self._focal_length
        )

        self._detection_area = (
            Triangle(
                self._position,
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

        for triangle in self._detection_area:
            triangle.plot(ax=ax, annotate=False)

        self._position.plot(ax=ax, annotate=False)

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
            for triangle in self._detection_area
        )

    def __repr__(self) -> str:
        """Get the raw representation of the Camera instance.

        Returns:
            str: raw representation of the Camera instance.
        """
        return (
            f"Camera(x: {self._position.x}, y: {self._position.y}, "
            + f"orientation: {self._orientation}, "
            + f"focal_angle: {self._focal_angle}, "
            + f"focal_length: {self._focal_length})"
        )

    def __str__(self) -> str:
        """Get the string representation of the Camera instance.

        Returns:
            str: string representation of the Camera instance.
        """
        detected = "\n        ".join(repr(array) for array in self._detected)
        return f"""Camera(
    x: {self._position.x},
    y: {self._position.y},
    orientation: {self._orientation},
    focal_angle: {self._focal_angle},
    focal_length: {self._focal_length},
    detected: (
        {detected}
    )
)"""


class Lidar:
    """LIDAR representation class.

    This class represents a LIDAR element, yet to be implemented. The class is
    temporarily used as a placeholder for future implementations.
    """

    pass
