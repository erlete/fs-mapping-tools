"""Container module for car representation classes.

This module contains all definitions of classes and utilities used to represent
a car object on track.

Authors:
    Paulo Sanchez (@erlete)
"""
from __future__ import annotations

from typing import Optional, Tuple, Union

import numpy as np
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
        weight (Union[int, float]): weight of the wheel [kg].
    """

    __slots__ = ("diameter", "width", "weight")

    def __init__(self, diameter: Union[int, float],
                 width: Union[int, float], weight: Union[int, float]) -> None:
        """Initialize a Wheel instance.

        Args:
            diameter (Union[int, float]): diameter of the wheel [m].
            width (Union[int, float]): width of the wheel [m].
            weight (Union[int, float]): weight of the wheel [kg].
        """
        self.diameter = diameter
        self.width = width
        self.weight = weight


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
        length (Union[int, float]): length of the car [m].
        width (Union[int, float]): width of the car [m].
        height (Union[int, float]): height of the car [m].
        engine (Engine): engine of the car.
        direction (Direction): direction of the car.
        front_to_axis (Optional[Union[int, float]], optional): distance between
            the front of the car and the front axis [m].
        rear_to_axis (Optional[Union[int, float]], optional): distance between
            the rear of the car and the rear axis [m].
        camera (Camera, optional): camera of the car.
        lidar (Lidar, optional): lidar of the car.
    """

    __slots__ = ("length", "width", "height", "engine", "direction",
                 "front_to_axis", "rear_to_axis", "camera", "lidar")

    def __init__(self, length: Union[int, float], width: Union[int, float],
                 height: Union[int, float],
                 engine: Engine, direction: Direction,
                 front_to_axis: Optional[Union[int, float]] = None,
                 rear_to_axis: Optional[Union[int, float]] = None,
                 camera: Optional[Camera] = None, lidar: Optional[Lidar] = None
                 ) -> None:
        """Initialize a CarStructure instance.

        Args:
            length (Union[int, float]): length of the car [m].
            width (Union[int, float]): width of the car [m].
            height (Union[int, float]): height of the car [m].
            engine (Engine): engine of the car.
            direction (Direction): direction of the car.
            front_to_axis (Optional[Union[int, float]], optional): distance
                between the front of the car and the front axis [m].
            rear_to_axis (Optional[Union[int, float]], optional): distance
                between the rear of the car and the rear axis [m].
            camera (Camera, optional): camera of the car.
            lidar (Lidar, optional): lidar of the car.
        """
        self.length = length
        self.width = width
        self.height = height
        self.engine = engine
        self.direction = direction
        self.front_to_axis = front_to_axis
        self.rear_to_axis = rear_to_axis
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

    @staticmethod
    def kmh_to_ms(speed: Union[int, float]) -> float:
        """Convert speed from km/h to m/s.

        Args:
            speed (Union[int, float]): speed in km/h.

        Returns:
            float: speed in m/s.
        """
        return speed / 3.6

    @staticmethod
    def ms_to_kmh(speed: Union[int, float]) -> float:
        """Convert speed from m/s to km/h.

        Args:
            speed (Union[int, float]): speed in m/s.

        Returns:
            float: speed in km/h.
        """
        return speed * 3.6

    @classmethod
    def fsuk_adsdv_camera(cls) -> Car:
        """Get a Car instance with FSUK (AI) ADS-DV specifications.

        Returns:
            Car: Car instance with FSUK (AI) ADS-DV specifications.
        """
        return cls(
            state=CarState(),
            structure=CarStructure(
                length=2.8146,
                width=1.430,
                height=0.664,
                engine=Engine(
                    speed=(0, cls.kmh_to_ms(50)),
                    acceleration=(0, 10),
                    torque=(0, 1000)
                ),
                direction=Direction(
                    front_axis=Axis(
                        left_wheel=Wheel(
                            diameter=0.513,
                            width=0.229,
                            weight=5.7
                        ),
                        right_wheel=Wheel(
                            diameter=0.513,
                            width=0.229,
                            weight=5.7
                        ),
                        steering_angle=np.deg2rad(27.2),
                        track=1.201
                    ),
                    rear_axis=Axis(
                        left_wheel=Wheel(
                            diameter=0.513,
                            width=0.229,
                            weight=5.7
                        ),
                        right_wheel=Wheel(
                            diameter=0.513,
                            width=0.229,
                            weight=5.7
                        ),
                        steering_angle=0,
                        track=1.201
                    ),
                    wheelbase=1.530
                ),
                camera=Camera(
                    fov=np.deg2rad(120),
                    detection_range=40
                ),
                front_to_axis=0.7209,
                rear_to_axis=0.5637
            )
        )
