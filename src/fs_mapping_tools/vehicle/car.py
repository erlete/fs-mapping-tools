"""Container module for car representation classes.

This module contains all definitions of classes and utilities used to represent
a car object on track.

Authors:
    Paulo Sanchez (@erlete)
"""
from __future__ import annotations

from math import cos, pi, sin
from typing import Optional, Tuple, Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from bidimensional import Coordinate, Segment
from bidimensional.polygons import Polygon

from ..vehicle.detection import Camera, Lidar


class State:
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
        "position",
        "orientation",
        "steering",
        "speed",
        "acceleration",
        "torque",
    )

    def __init__(
        self,
        position: Optional[Coordinate] = None,
        orientation: Union[int, float] = 0,
        steering: Union[int, float] = 0,
        speed: Union[int, float] = 0,
        acceleration: Union[int, float] = 0,
        torque: Union[int, float] = 0,
    ) -> None:
        """Initialize a State instance.

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
        self.position = position if position is not None else Coordinate(0, 0)
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

    STYLES = {
        "style": "-",
        "color": "black",
        "linewidth": 1,
        "alpha": .75
    }

    def __init__(
        self,
        diameter: Union[int, float],
        width: Union[int, float],
        weight: Union[int, float],
    ) -> None:
        """Initialize a Wheel instance.

        Args:
            diameter (Union[int, float]): diameter of the wheel [m].
            width (Union[int, float]): width of the wheel [m].
            weight (Union[int, float]): weight of the wheel [kg].
        """
        self.diameter = diameter
        self.width = width
        self.weight = weight

    def plot(self, state: State, center: Coordinate,
             max_steering: float, ax: matplotlib.axes.Axes = None,
             **kwargs) -> None:
        """Plot the wheel.

        Args:
            state (State): state of the car.
            center (Coordinate): center of the wheel.
            max_steering (float): maximum steering angle of the direction.
            ax (matplotlib.axes.Axes, optional): ax to plot on. Defaults to
                None. If None, plt.gca() is used.
            **kwargs: keyword arguments for matplotlib.pyplot.plot.
        """
        self.STYLES.update(kwargs)

        orientation = state.orientation
        steering = (
            state.steering if abs(state.steering) < max_steering
            else max_steering
        )
        ax = ax if ax is not None else plt.gca()

        wheel = Polygon(
            Coordinate(
                cos(orientation + steering) * (self.diameter / 2),
                sin(orientation + steering) * (self.diameter / 2)
            ) + center + Coordinate(
                cos(orientation + (pi / 2) + steering) * (self.width / 2),
                sin(orientation + (pi / 2) + steering) * (self.width / 2)
            ),
            -Coordinate(
                cos(orientation + steering) * (self.diameter / 2),
                sin(orientation + steering) * (self.diameter / 2)
            ) + center + Coordinate(
                cos(orientation + (pi / 2) + steering) * (self.width / 2),
                sin(orientation + (pi / 2) + steering) * (self.width / 2)
            ),
            -Coordinate(
                cos(orientation + steering) * (self.diameter / 2),
                sin(orientation + steering) * (self.diameter / 2)
            ) + center - Coordinate(
                cos(orientation + (pi / 2) + steering) * (self.width / 2),
                sin(orientation + (pi / 2) + steering) * (self.width / 2)
            ),
            Coordinate(
                cos(orientation + steering) * (self.diameter / 2),
                sin(orientation + steering) * (self.diameter / 2)
            ) + center - Coordinate(
                cos(orientation + (pi / 2) + steering) * (self.width / 2),
                sin(orientation + (pi / 2) + steering) * (self.width / 2)
            )
        )

        wheel.plot(ax=ax, annotate=False, **kwargs)


class Axis:
    """Direction axis representation class.

    This class represent a direction axis of the car. It includes the wheels
    that are attached to the axis, the distance between them  and the steering
    angle.

    Attributes:
        left_wheel (Wheel): left wheel of the axis.
        right_wheel (Wheel): right wheel of the axis.
        max_steering (Union[int, float]): steering angle of the axis [rad].
        track (Union[int, float]): distance between the wheels of the axis [m].
    """

    __slots__ = ("left_wheel", "right_wheel", "max_steering", "track")

    def __init__(
        self,
        left_wheel: Wheel,
        right_wheel: Wheel,
        max_steering: Union[int, float],
        track: Union[int, float],
    ) -> None:
        """Initialize an Axis instance.

        Args:
            left_wheel (Wheel): left wheel of the axis.
            right_wheel (Wheel): right wheel of the axis.
            max_steering (Union[int, float]): steering angle of the axis [rad].
            track (Union[int, float]): distance between the wheels of the axis
                [m].
        """
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.max_steering = max_steering
        self.track = track

    def plot(self, state: State, center: Coordinate,
             ax: matplotlib.axes.Axes = None, **kwargs) -> None:
        """Plot the axis.

        Args:
            state (State): state of the car.
            center (Coordinate): center of the axis.
            ax (matplotlib.axes.Axes, optional): ax to plot on. Defaults to
                None. If None, plt.gca() is used.
            **kwargs: keyword arguments for matplotlib.pyplot.plot.
        """
        ax = ax if ax is not None else plt.gca()

        main_axis = Segment(
            Coordinate(
                cos(state.orientation + pi / 2) * (self.track / 2),
                sin(state.orientation + pi / 2) * (self.track / 2)
            ) + center,
            -Coordinate(
                cos(state.orientation + pi / 2) * (self.track / 2),
                sin(state.orientation + pi / 2) * (self.track / 2)
            ) + center
        )

        self.left_wheel.plot(state, main_axis.a, self.max_steering,
                             ax=ax, **kwargs)
        self.right_wheel.plot(state, main_axis.b, self.max_steering,
                              ax=ax, **kwargs)

        main_axis.plot(ax=ax, **kwargs)


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

    def __init__(
        self, front_axis: Axis, rear_axis: Axis, wheelbase: Union[int, float]
    ) -> None:
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

    def plot(self,
             state: State, ax: matplotlib.axes.Axes = None, **kwargs
             ) -> None:
        """Plot the direction system.

        Args:
            state (State): state of the car.
            ax (matplotlib.axes.Axes, optional): ax to plot on. Defaults to
                None. If None, plt.gca() is used.
            **kwargs: keyword arguments for matplotlib.pyplot.plot.
        """
        ax = ax if ax is not None else plt.gca()

        main_axis = Segment(
            Coordinate(
                cos(state.orientation) * self.wheelbase / 2,
                sin(state.orientation) * self.wheelbase / 2
            ) + state.position,
            -Coordinate(
                cos(state.orientation) * self.wheelbase / 2,
                sin(state.orientation) * self.wheelbase / 2
            ) + state.position
        )

        self.front_axis.plot(state, main_axis.a, ax=ax, **kwargs)
        self.rear_axis.plot(state, main_axis.b, ax=ax, **kwargs)

        main_axis.plot(ax=ax, **kwargs)


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
        torque: Tuple[Union[int, float], Union[int, float]],
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


class Structure:
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

    __slots__ = (
        "length",
        "width",
        "height",
        "engine",
        "direction",
        "front_to_axis",
        "rear_to_axis",
        "camera",
        "lidar",
    )

    def __init__(
        self,
        length: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        engine: Engine,
        direction: Direction,
        front_to_axis: Optional[Union[int, float]] = None,
        rear_to_axis: Optional[Union[int, float]] = None,
        camera: Optional[Camera] = None,
        lidar: Optional[Lidar] = None,
    ) -> None:
        """Initialize a Structure instance.

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

    def plot(self,
             state: State, ax: matplotlib.axes.Axes = None, **kwargs
             ) -> None:
        """Plot the axis.

        Args:
            state (State): state of the car.
            ax (matplotlib.axes.Axes, optional): ax to plot on. Defaults to
                None. If None, plt.gca() is used.
            **kwargs: keyword arguments for matplotlib.pyplot.plot.
        """
        ax = ax if ax is not None else plt.gca()

        self.camera.plot(ax=ax, **kwargs)
        self.direction.plot(state, ax=ax, **kwargs)


class Car:
    """Car representation class.

    This class represent the car element, which is composed of a structure
    (static properties, time-independent) and a state (dynamic properties,
    time-dependent).

    Attributes:
        state (State): state of the car at a given instant.
        structure (Structure): structure of the car.
    """

    __slots__ = ("state", "structure")

    def __init__(self, state: State, structure: Structure) -> None:
        """Initialize a Car instance.

        Args:
            state (State): state of the car at a given instant.
            structure (Structure): structure of the car.
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

    def plot(self, ax: matplotlib.axes.Axes = None, **kwargs) -> None:
        """Plot the car.

        This method is used to plot the whole car model, taking into account
        most (or all) of its dynamic and static properties.

        Args:
            ax (matplotlib.axes.Axes, optional): ax to plot on. Defaults to
                None. If None, plt.gca() is used.
            **kwargs: keyword arguments for matplotlib.pyplot.plot.
        """
        ax = ax if ax is not None else plt.gca()

        self.structure.plot(self.state, ax=ax, **kwargs)

    @classmethod
    def fsuk_adsdv_camera(cls) -> Car:
        """Get a Car instance with FSUK (AI) ADS-DV specifications.

        Reference: https://www.imeche.org/docs/default-source/1-oscar/formula-student/2019/fs-ai/ads-dv-dimensions-and-locations-v0-1.pdf?sfvrsn=2  # noqa: ignore

        Returns:
            Car: Car instance with FSUK (AI) ADS-DV specifications.
        """
        return cls(
            state=State(),
            structure=Structure(
                length=2.8146,
                width=1.430,
                height=0.664,
                engine=Engine(  # Actually, the vehicle has got two engines.
                    speed=(0, cls.kmh_to_ms(50)),  # Fictional.
                    acceleration=(0, 10),  # Fictional.
                    torque=(0, 1000)  # Fictional.
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
                        max_steering=np.deg2rad(27.2),
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
                        max_steering=0,
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
