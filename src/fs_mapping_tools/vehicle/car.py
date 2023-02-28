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


class CarStructure:
    """Car structure representation class.

    This class represent the static structure of the car, including all
    relevant physical properties that it might include.

    Attributes:
        back_to_wheel (float): distance from the car's back to the wheel's
            center [m].
        length (float): car length [m].
        max_acceleration (float): maximum acceleration [m/s^2].
        max_downsteering (float): maximum downsteering angle [rad].
        max_speed (float): maximum speed [m/s].
        max_steering (float): maximum steering angle [rad].
        min_speed (float): minimum speed [m/s].
        tread (float): distance between the wheels [m].
        wheel_base (float): distance between the front and back wheels [m].
        wheel_length (float): wheel length [m].
        wheel_width (float): wheel width [m].
        width (float): car width [m].
    """

    __DEFAULTS = {
        "back_to_wheel": 0.0,
        "length": 0.0,
        "max_acceleration": 0.0,
        "max_downsteering": 0.0,
        "max_speed": 0.0,
        "max_steering": 0.0,
        "min_speed": 0.0,
        "tread": 0.0,
        "wheel_base": 0.0,
        "wheel_length": 0.0,
        "wheel_width": 0.0,
        "width": 0.0
    }

    __TYPES = {
        "back_to_wheel": (int, float),
        "length": (int, float),
        "max_acceleration": (int, float),
        "max_downsteering": (int, float),
        "max_speed": (int, float),
        "max_steering": (int, float),
        "min_speed": (int, float),
        "tread": (int, float),
        "wheel_base": (int, float),
        "wheel_length": (int, float),
        "wheel_width": (int, float),
        "width": (int, float)
    }

    def __init__(self, **kwargs):
        """Initialize a CarStructure instance.

        Args:
            kwargs: dictionary of properties to be stored in the instance.
        """
        self._dictionary = self.__DEFAULTS.copy()
        self._dictionary.update(kwargs)

        # Method redirection:
        self.get = self._dictionary.get
        self.clear = self._dictionary.clear
        self.copy = self._dictionary.copy
        self.fromkeys = self._dictionary.fromkeys
        self.get = self._dictionary.get
        self.items = self._dictionary.items
        self.keys = self._dictionary.keys
        self.pop = self._dictionary.pop
        self.popitem = self._dictionary.popitem
        self.setdefault = self._dictionary.setdefault
        self.values = self._dictionary.values

    def __getattr__(self, name: str):
        """Get an attribute from the instance dictionary.

        Args:
            name (str): the name of the attribute.

        Returns:
            Any: the value of the attribute.
        """
        return self._dictionary.get(name)

    def __setattr__(self, name: str, value: Any):
        """Set an attribute in the instance dictionary.

        Args:
            name (str): the name of the attribute.
            value (Any): the value of the attribute.
        """
        # Recursion error avoidance:
        if name != "dictionary" and name not in self._dictionary.__dir__():

            # Invalid attribute checking:
            if name not in self._dictionary:
                raise AttributeError(
                    f"invalid attribute: \"{name}\". Possible values are: "
                    + ', '.join(
                        f"\"{key}\""
                        for key in self._dictionary.keys()
                    ) + '.'
                )

            # Invalid type checking:
            if not isinstance(value, self.__TYPES[name]):
                raise TypeError(
                    f"invalid type for attribute {name}."
                    f" Expected {self.__TYPES[name]}, got {type(value)}."
                )

            self._dictionary[name] = value

        else:
            self.__dict__[name] = value


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
