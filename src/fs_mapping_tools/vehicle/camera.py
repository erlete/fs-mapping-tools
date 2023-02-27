"""Container module for camera representation classes.

This module contains all definitions of classes and utilities used to represent
a camera object on track.

Authors:
    Paulo Sanchez (@erlete)
"""


from bidimensional import Coordinate


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
