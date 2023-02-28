"""Container module for car representation classes.

This module contains all definitions of classes and utilities used to represent
a car object on track.

Authors:
    Paulo Sanchez (@erlete)
"""


from typing import Any, Dict, Optional

from bidimensional import Coordinate

from ..vehicle.detection import Camera, Lidar


class CarState:
    """Car state representation class.

    This class represent the state of the car at a given instant during the
    track run.

    Attributes:
        position (Coordinate): position of the car (x [m], y [m]).
        orientation (float): orientation of the car (front view) [rad].
        steering (float): steering of the front wheels of the car [rad].
        speed (float): speed of the car [m/s].
        acceleration (float): acceleration of the car [m/s^2].
        torque (float): torque of the engine [Nm].
    """

    def __init__(self, position: Coordinate, orientation: float,
                 steering: float, speed: float, acceleration: float,
                 torque: float) -> None:
        """Initialize a CarState instance.

        Args:
            position (Coordinate): position of the car (x [m], y [m]).
            orientation (float): orientation of the car (front view) [rad].
            steering (float): steering of the front wheels of the car [rad].
            speed (float): speed of the car [m/s].
            acceleration (float): acceleration of the car [m/s^2].
            torque (float): torque of the engine [Nm].
        """
        self.position = position
        self.orientation = orientation
        self.steering = steering
        self.speed = speed
        self.acceleration = acceleration
        self.torque = torque


class CarStructure:
    """Car structure representation class.

    This class represent the static structure of the car, including all
    relevant physical properties that it might include.

    Attributes:
        TODO
    """

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a CarStructure instance.

        Args:
            TODO
        """
        self.structure = kwargs


class Car:
    """Car representation class.

    This class represent the car element, which is composed of a structure
    (static properties, time-independent) and a state (dynamic properties,
    time-dependent). It also includes the detection hardware of the car, such
    as the camera and/or the lidar.

    Attributes:
        state (CarState): state of the car at a given instant.
        structure (CarStructure): structure of the car.
        camera (Camera, optional): camera of the car.
        lidar (Lidar, optional): lidar of the car.
    """

    def __init__(
        self, state: CarState, structure: CarStructure,
        camera: Optional[Camera] = None, lidar: Optional[Lidar] = None
    ) -> None:
        """Initialize a Car instance.

        Args:
            state (CarState): state of the car at a given instant.
            structure (CarStructure): structure of the car.
            camera (Camera, optional): camera of the car.
            lidar (Lidar, optional): lidar of the car.
        """
        self.state = state
        self.structure = structure
        self.camera = camera
        self.lidar = lidar
