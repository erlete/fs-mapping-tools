"""Testing suites for the cones module.

Author:
    Paulo Sanchez (@erlete)
"""

import pytest
from bidimensional import Coordinate

from fs_mapping_tools import Cone, ConeArray


class TestCone:
    """Testing suite for the Cone class."""

    ZERO = Coordinate(0, 0)

    def test_instance(self) -> None:
        """Test class instantiation."""
        with pytest.raises(TypeError):
            # Incorrect `position` data type:
            Cone(1, "yellow")
            # Incorrect `type` data type:
            Cone(self.ZERO, ["yellow"])

        with pytest.raises(ValueError):
            # Incorrect `type` value:
            Cone(self.ZERO, "yellowish")

        # Valid `position` and `type` values:
        Cone(self.ZERO, "yellow")
        Cone(self.ZERO, "blue")
        Cone(self.ZERO, "orange")
        Cone(self.ZERO, "orange-big")

    def test_access(self) -> None:
        """Test class attributes."""
        c1 = Cone(self.ZERO, "yellow")
        c2 = Cone(self.ZERO, "blue")
        c3 = Cone(self.ZERO, "orange")
        c4 = Cone(self.ZERO, "orange-big")

        # Test `x` and `y` attributes:
        assert c1.x == c2.x == c3.x == c4.x == 0
        assert c1.y == c2.y == c3.y == c4.y == 0

        # Test `position` attribute:
        assert c1.position == c2.position == c3.position == c4.position \
            == self.ZERO

        # Test `type` attribute:
        assert c1.type == "yellow"
        assert c2.type == "blue"
        assert c3.type == "orange"
        assert c4.type == "orange-big"

    def test_eq(self) -> None:
        """Test class equality."""
        c1 = Cone(self.ZERO, "yellow")
        c2 = Cone(self.ZERO, "blue")
        c3 = Cone(self.ZERO, "orange")
        c4 = Cone(self.ZERO, "orange-big")

        assert c1 == c1
        assert c2 == c2
        assert c3 == c3
        assert c4 == c4

    def test_ne(self) -> None:
        """Test class inequality."""
        c1 = Cone(self.ZERO, "yellow")
        c2 = Cone(self.ZERO, "blue")
        c3 = Cone(self.ZERO, "orange")
        c4 = Cone(self.ZERO, "orange-big")

        assert c1 != c2
        assert c1 != c3
        assert c1 != c4
        assert c2 != c3
        assert c2 != c4
        assert c3 != c4

    def test_plot(self) -> None:
        """Test plot method."""
        c1 = Cone(self.ZERO, "yellow")
        c2 = Cone(self.ZERO, "blue")
        c3 = Cone(self.ZERO, "orange")
        c4 = Cone(self.ZERO, "orange-big")

        # Detail off:
        c1.plot(detail=False)
        c2.plot(detail=False)
        c3.plot(detail=False)
        c4.plot(detail=False)

        # Detail on:
        c1.plot(detail=True)
        c2.plot(detail=True)
        c3.plot(detail=True)
        c4.plot(detail=True)


class TestConeArray:
    """Testing suite for the ConeArray class."""

    ZERO = Coordinate(0, 0)
    C1 = Cone(Coordinate(0, 0), "yellow")
    C2 = Cone(Coordinate(0, 0), "blue")
    C3 = Cone(Coordinate(0, 0), "orange")
    C4 = Cone(Coordinate(0, 0), "orange-big")

    def test_instance(self) -> None:
        """Test class instantiation."""
        # Empty initialization:
        ConeArray()

        # Single initialization:
        ConeArray(self.C1)

        # Multiple initialization:
        ConeArray(self.C1, self.C1)

    def test_access(self) -> None:
        """Test class attributes."""
        ca1 = ConeArray(self.C1)
        ca2 = ConeArray(self.C2)
        ca3 = ConeArray(self.C3)
        ca4 = ConeArray(self.C4)

        # Test `cones` attribute:
        assert ca1.cones == [self.C1]
        assert ca2.cones == [self.C2]
        assert ca3.cones == [self.C3]
        assert ca4.cones == [self.C4]

        # Test `type` attribute:
        assert ca1.type == "yellow"
        assert ca2.type == "blue"
        assert ca3.type == "orange"
        assert ca4.type == "orange-big"

    def test_append(self) -> None:
        """Test appending method."""
        ca = ConeArray(self.C1)

        # Invalid `cone` data type:
        with pytest.raises(TypeError):
            ca.append(1)
            ca.append("str")
            ca.append([1, 2])
            ca.append([self.C1, self.C2])

        # Invalid `type` value:
        with pytest.raises(ValueError):
            ca.append(self.C2)
            ca.append(self.C3)
            ca.append(self.C4)

    def test_extend(self) -> None:
        """Test extending method."""
        ca = ConeArray(self.C1)

        # Invalid `cone` data type:
        with pytest.raises(TypeError):
            ca.extend([1])
            ca.extend(["str"])
            ca.extend([1, 2])
            ca.extend(self.C1)

        # Invalid `type` value:
        with pytest.raises(ValueError):
            ca.extend([self.C2])
            ca.extend([self.C3])
            ca.extend([self.C4])

    def test_eq(self) -> None:
        """Test class equality."""
        ca1 = ConeArray(self.C1)
        ca2 = ConeArray(self.C2)
        ca3 = ConeArray(self.C3)
        ca4 = ConeArray(self.C4)

        assert ca1 == ca1
        assert ca2 == ca2
        assert ca3 == ca3
        assert ca4 == ca4

    def test_ne(self) -> None:
        """Test class inequality."""
        ca1 = ConeArray(self.C1)
        ca2 = ConeArray(self.C2)
        ca3 = ConeArray(self.C3)
        ca4 = ConeArray(self.C4)

        assert ca1 != ca2
        assert ca1 != ca3
        assert ca1 != ca4
        assert ca2 != ca3
        assert ca2 != ca4
        assert ca3 != ca4

    def test_plot(self) -> None:
        """Test plot method."""
        # Detail off:
        ConeArray(self.C1).plot(detail=False)
        ConeArray(self.C2).plot(detail=False)
        ConeArray(self.C3).plot(detail=False)
        ConeArray(self.C4).plot(detail=False)

        # Detail on:
        ConeArray(self.C1).plot(detail=True)
        ConeArray(self.C2).plot(detail=True)
        ConeArray(self.C3).plot(detail=True)
        ConeArray(self.C4).plot(detail=True)
