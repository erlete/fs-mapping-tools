"""Container module for detection hardware representation classes.

This module contains all definitions of classes and utilities used to represent
both camera and lidar objects on the vehicle.

Authors:
    Paulo Sanchez (@erlete)
"""

from math import cos, sin
from typing import Any, List, Optional, Union

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
        orientation (float): orientation of the camera.
        fov (float): field of view of the camera.
        detection_range (float): detection range of the camera.
    """

    __slots__ = (
        "_position", "_orientation", "_fov", "_detection_range",
        "_detected", "_detection_area", "__ready_to_detect"
    )

    def __init__(self, position: Optional[Coordinate] = None,
                 orientation: Union[int, float] = 0,
                 fov: Union[int, float] = 0,
                 detection_range: Union[int, float] = 0) -> None:
        """Initialize a Camera instance.

        Args:
            position (Coordinate): position of the center of the camera.
                Defaults to None. If None, the position will be set to
                Coordinate(0, 0).
            orientation (int | float, optional): orientation of the camera.
                Defaults to 0.
            fov (int | float, optional): field of view of the camera. Defaults
                to 0.
            detection_range (int | float, optional): detection range of the
                camera. Defaults to 0.
        """
        self.__ready_to_detect = False

        self.position = position if position is not None else Coordinate(0, 0)
        self.orientation = orientation
        self.fov = fov
        self.detection_range = detection_range

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
    def orientation(self, value: Union[int, float]) -> None:
        """Set the orientation of the camera.

        Args:
            value (int | float): new orientation of the camera.

        Raises:
            TypeError: if the value is not an int or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("value must be an int or float.")

        self._orientation = float(value)

        if self.__ready_to_detect:
            self._set_detection_area()

    @property
    def fov(self) -> float:
        """field of viewfocal angle of the camera.

        Returns:
            float: field of view of the camera.
        """
        return self._fov

    @fov.setter
    def fov(self, value: Union[int, float]) -> None:
        """Set the field of view of the camera.

        Args:
            value (int | float): new field of view of the camera.

        Raises:
            TypeError: if the value is not an int or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("value must be an int or float.")

        self._fov = float(value)

        if self.__ready_to_detect:
            self._set_detection_area()

    @property
    def detection_range(self) -> float:
        """Get the detection range of the camera.

        Returns:
            float: detection range of the camera.
        """
        return self._detection_range

    @detection_range.setter
    def detection_range(self, value: Union[int, float]) -> None:
        """Set the detection range of the camera.

        Args:
            value (int | float): new detection range of the camera.

        Raises:
            TypeError: if the value is not an int or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("value must be an int or float.")

        self._detection_range = float(value)

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
        left_rot = self._orientation - self._fov / 2
        right_rot = self._orientation + self._fov / 2

        radius = self._position + Coordinate(
            cos(self._orientation) * self._detection_range,
            sin(self._orientation) * self._detection_range
        )
        left_boundary = self._position + Coordinate(
            cos(left_rot) * self._detection_range,
            sin(left_rot) * self._detection_range
        )
        right_boundary = self._position + Coordinate(
            cos(right_rot) * self._detection_range,
            sin(right_rot) * self._detection_range
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

    def plot(self, ax: matplotlib.axes.Axes = None, **kwargs) -> None:
        """Plot the camera and detection range.

        Args:
            ax (matplotlib.axes.Axes, optional): ax to plot on. Defaults to
                None. If None, plt.gca() is used.
            **kwargs: keyword arguments for matplotlib.pyplot.plot.
        """
        ax = ax if ax is not None else plt.gca()

        for triangle in self._detection_area:
            triangle.plot(ax=ax, annotate=False, **kwargs)

        self._position.plot(ax=ax, annotate=False, **kwargs)

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
            + f"fov: {self._fov}, "
            + f"detection_range: {self._detection_range})"
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
    fov: {self._fov},
    detection_range: {self._detection_range},
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
