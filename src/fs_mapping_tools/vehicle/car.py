"""Container module for car representation classes.

This module contains all definitions of classes and utilities used to represent
a car object on track.

Authors:
    Paulo Sanchez (@erlete)
"""

from typing import Optional, Tuple, Union

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

    def __init__(self, position: Optional[Coordinate] = None,
                 orientation: Optional[Union[int, float]] = 0,
                 steering: Optional[Union[int, float]] = 0,
                 speed: Optional[Union[int, float]] = 0,
                 acceleration: Optional[Union[int, float]] = 0,
                 torque: Optional[Union[int, float]] = 0) -> None:
        """Initialize a CarState instance.

        Args:
            position (Coordinate, optional): position of the car (x [m],
                y [m]). Defaults to None. If None, the position will be set to
                Coordinate(0, 0).
            orientation (int | float, optional): orientation of the car (front
                view) [rad]. Defaults to 0.
            steering (int | float, optional): steering of the front wheels of
                the car [rad]. Defaults to 0.
            speed (int | float, optional): speed of the car [m/s]. Defaults
                to 0.
            acceleration (int | float, optional): acceleration of the car
                [m/s^2]. Defaults to 0.
            torque (int | float, optional): torque of the engine [Nm]. Defaults
                to 0.
        """
        if position is not None:
            self.position = position
        else:
            self.position = Coordinate(0, 0)
        self.orientation = orientation
        self.steering = steering
        self.speed = speed
        self.acceleration = acceleration
        self.torque = torque


class Wheel:
    """Wheel representation class.

    This class represent a wheel of the car. It includes the diameter and the
    width of the wheel.

    Attributes:
        diameter (Union[int, float]): diameter of the wheel [m].
        width (Union[int, float]): width of the wheel [m].
    """

    __slots__ = ("diameter", "width")

    def __init__(self, diameter: Union[int, float],
                 width: Union[int, float]) -> None:
        """Initialize a Wheel instance.

        Args:
            diameter (Union[int, float]): diameter of the wheel [m].
            width (Union[int, float]): width of the wheel [m].
        """
        self.diameter = diameter
        self.width = width


class Axis:
    """Direction axis representation class.

    This class represent a direction axis of the car. It includes the wheels
    that are attached to the axis, the distance between them  and the steering
    angle.

    Attributes:
        left_wheel (Wheel): left wheel of the axis.
        right_wheel (Wheel): right wheel of the axis.
        steering_angle (Union[int, float]): steering angle of the axis [rad].
        track (Union[int, float]): distance between the wheels of the axis [m].
    """

    __slots__ = ("left_wheel", "right_wheel", "steering_angle", "track")

    def __init__(self, left_wheel: Wheel, right_wheel: Wheel,
                 steering_angle: Union[int, float],
                 track: Union[int, float]) -> None:
        """Initialize an Axis instance.

        Args:
            left_wheel (Wheel): left wheel of the axis.
            right_wheel (Wheel): right wheel of the axis.
            steering_angle (Union[int, float]): steering angle of the axis
                [rad].
            track (Union[int, float]): distance between the wheels of the axis
                [m].
        """
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.steering_angle = steering_angle
        self.track = track


class Direction:
    """Direction system representation class.

    This class represent the direction system of the car. It includes the front
    and rear axis of the car and the distance between them.

    Attributes:
        front_axis (Axis): front axis of the car.
        rear_axis (Axis): rear axis of the car.
        wheelbase (Union[int, float]): distance between the front and rear axis
            of the car [m].
    """

    __slots__ = ("front_axis", "rear_axis", "wheelbase")

    def __init__(self, front_axis: Axis, rear_axis: Axis,
                 wheelbase: Union[int, float]) -> None:
        """Initialize a Direction instance.

        Args:
            front_axis (Axis): front axis of the car.
            rear_axis (Axis): rear axis of the car.
            wheelbase (Union[int, float]): distance between the front and rear
                axis of the car [m].
        """
        self.front_axis = front_axis
        self.rear_axis = rear_axis
        self.wheelbase = wheelbase


class Engine:
    """Engine representation class.

    This class represent the engine of the car. It includes valid value ranges
    for the acceleration, speed and torque of the car.

    Attributes:
        speed (Tuple[Union[int, float], Union[int, float]]): valid speed range
            of the car [m/s].
        acceleration (Tuple[Union[int, float], Union[int, float]]): valid
            acceleration range of the car [m/s^2].
        torque (Tuple[Union[int, float], Union[int, float]]): valid torque
            range of the car [Nm].
    """

    __slots__ = ("acceleration", "speed", "torque")

    def __init__(
        self,
        speed: Tuple[Union[int, float], Union[int, float]],
        acceleration: Tuple[Union[int, float], Union[int, float]],
        torque: Tuple[Union[int, float], Union[int, float]]
    ) -> None:
        """Initialize an Engine instance.

        Attributes:
            speed (Tuple[Union[int, float], Union[int, float]]): valid speed
                range of the car [m/s].
            acceleration (Tuple[Union[int, float], Union[int, float]]): valid
                acceleration range of the car [m/s^2].
            torque (Tuple[Union[int, float], Union[int, float]]): valid torque
                range of the car [Nm].
        """
        self.speed = speed
        self.acceleration = acceleration
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
