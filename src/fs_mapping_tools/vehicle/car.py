"""Container module for car representation classes.

This module contains all definitions of classes and utilities used to represent
a car object on track.

Authors:
    Paulo Sanchez (@erlete)
"""


from typing import Any, Optional, Tuple, Union

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

    __slots__ = (
        "position", "orientation", "steering", "speed", "acceleration",
        "torque"
    )

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


class Wheel:

    __slots__ = ("diameter", "width")

    def __init__(self, diameter: Union[int, float],
                 width: Union[int, float]) -> None:
        self.diameter = diameter
        self.width = width


class Axis:

    __slots__ = ("left_wheel", "right_wheel", "steering_angle", "track")

    def __init__(self, left_wheel: Wheel, right_wheel: Wheel,
                 steering_angle: Union[int, float],
                 track: Union[int, float]) -> None:
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.steering_angle = steering_angle
        self.track = track


class Direction:

    __slots__ = ("front_axis", "rear_axis", "wheelbase")

    def __init__(self, front_axis: Axis, rear_axis: Axis,
                 wheelbase: Union[int, float]) -> None:
        self.front_axis = front_axis
        self.rear_axis = rear_axis
        self.wheelbase = wheelbase


class Engine:

    __slots__ = ("acceleration", "speed", "torque")

    def __init__(
        self,
        acceleration: Tuple[Union[int, float], Union[int, float]],
        speed: Tuple[Union[int, float], Union[int, float]],
        torque: Tuple[Union[int, float], Union[int, float]]
    ) -> None:
        self.acceleration = acceleration
        self.speed = speed
        self.torque = torque


class CarStructure:
    """Car structure representation class.

    This class represent the static structure of the car, including all
    relevant physical properties that it might include. It also includes the
    detection hardware of the car, such as the camera and/or the lidar.

    Attributes:
        engine (Engine): engine of the car.
        direction (Direction): direction of the car.
        camera (Camera, optional): camera of the car.
        lidar (Lidar, optional): lidar of the car.
    """

    __slots__ = ("engine", "direction", "camera", "lidar")

    def __init__(self, engine: Engine, direction: Direction,
                 camera: Optional[Camera] = None, lidar: Optional[Lidar] = None
                 ) -> None:
        """Initialize a CarStructure instance.

        Args:
            engine (Engine): engine of the car.
            direction (Direction): direction of the car.
            camera (Camera, optional): camera of the car.
            lidar (Lidar, optional): lidar of the car.
        """
        self.engine = engine
        self.direction = direction
        self.camera = camera
        self.lidar = lidar


class Car:
    """Car representation class.

    This class represent the car element, which is composed of a structure
    (static properties, time-independent) and a state (dynamic properties,
    time-dependent).

    Attributes:
        state (CarState): state of the car at a given instant.
        structure (CarStructure): structure of the car.
    """

    __slots__ = ("state", "structure")

    def __init__(self, state: CarState, structure: CarStructure) -> None:
        """Initialize a Car instance.

        Args:
            state (CarState): state of the car at a given instant.
            structure (CarStructure): structure of the car.
        """
        self.state = state
        self.structure = structure
