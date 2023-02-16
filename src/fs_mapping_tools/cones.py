from .config import CONES
from bidimensional import Coordinate
from matplotlib import pyplot as plt


class Cone:

    def __init__(self, pose: Coordinate, type: str) -> None:
        self.pose = pose
        self.type = type

    @property
    def x(self) -> float:
        return self.pose.x

    @property
    def y(self) -> float:
        return self.pose.y

    @property
    def pose(self) -> Coordinate:
        return self._pose

    @pose.setter
    def pose(self, pose: Coordinate) -> None:
        if not isinstance(pose, Coordinate):
            raise TypeError("pose must be a Coordinate")

        self._pose = pose

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("value must be a string")

        elif value not in CONES:
            raise ValueError(
                f"value must be one of the following types: "
                f"{CONES.values()}"
            )

        self._type = value

    def plot(self, ax=plt.gca(), detail=True) -> None:
        ax.plot(
            self.pose.x, self.pose.y,
            color=CONES[self.type]["colors"]["base"],
            marker='o', ms=CONES[self.type]["size"]["base"]
        )

        if detail:
            ax.plot(
                self.pose.x, self.pose.y,
                color=CONES[self.type]["colors"]["strip_low"],
                marker='o', ms=CONES[self.type]["size"]["strip_low"]
            )
            ax.plot(
                self.pose.x, self.pose.y,
                color=CONES[self.type]["colors"]["mid"],
                marker='o', ms=CONES[self.type]["size"]["mid"]
            )
            ax.plot(
                self.pose.x, self.pose.y,
                color=CONES[self.type]["colors"]["strip_high"],
                marker='o', ms=CONES[self.type]["size"]["strip_high"]
            )
            ax.plot(
                self.pose.x, self.pose.y,
                color=CONES[self.type]["colors"]["top"],
                marker='o', ms=CONES[self.type]["size"]["top"]
            )
            ax.plot(
                self.pose.x, self.pose.y,
                color="#ffffff",
                marker='o', ms=CONES[self.type]["size"]["top"] / 2
            )

    def __str__(self) -> str:
        return f"Cone({self.pose.x}, {self.pose.y}, {self.type})"

    def __repr__(self) -> str:
        return self.__str__()
