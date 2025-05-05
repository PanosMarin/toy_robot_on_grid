import unittest
from unittest.mock import MagicMock, patch
from toy_robot.grid import Cell, SquareGrid
from toy_robot.utils import Direction, Coordinates


class Test_Cell(unittest.TestCase):
    '''Unit tests for the Cell class'''

    def setUp(self):
        self._cell1 = Cell(0, 0)
        self._cell12 = Cell(1, 1)

    def test_set_neighbour(self):
        '''Tests the Cell.set_neighbour method'''
        self._cell1.set_neighbour(self._cell12, Direction.EAST)
        self.assertEqual(self._cell1._neighbours[Direction.EAST], self._cell12)
        self.assertEqual(self._cell12._neighbours[Direction.WEST], self._cell1)

    def test_get_neighbour(self):
        '''Tests the Cell.get_neighbour method'''
        self._cell1.set_neighbour(self._cell12, Direction.EAST)
        self.assertEqual(self._cell1._neighbours[Direction.EAST], self._cell12)
        self.assertEqual(self._cell12._neighbours[Direction.WEST], self._cell1)
        self.assertEqual(self._cell1.get_neighbour(
            Direction.EAST), self._cell12)


class Test_Grid(unittest.TestCase):
    '''Unit tests for the SquareGrid class'''

    def setUp(self):
        self._grid = SquareGrid(5)

    def test_is_valid_cell(self):
        '''Test the SquareGrid.is_valid_cell method'''
        self.assertEqual(self._grid.is_valid_cell(Coordinates(0, 0)), True)
        self.assertEqual(self._grid.is_valid_cell(Coordinates(4, 4)), True)
        self.assertEqual(self._grid.is_valid_cell(Coordinates(5, 5)), False)
        self.assertEqual(self._grid.is_valid_cell(Coordinates(0, 5)), False)
        self.assertEqual(self._grid.is_valid_cell(Coordinates(5, 0)), False)

    def test_get_next_cell_coordinates(self):
        '''Test the SquareGrid.get_next_cell_coordinates method'''
        # Check valid cells
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(2, 2), Direction.EAST), Coordinates(3, 2))
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(2, 2), Direction.WEST), Coordinates(1, 2))
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(2, 2), Direction.NORTH), Coordinates(2, 3))
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(2, 2), Direction.SOUTH), Coordinates(2, 1))

        # Check corner cases
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(0, 0), Direction.SOUTH), None)
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(0, 0), Direction.WEST), None)
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(0, 4), Direction.NORTH), None)
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(4, 0), Direction.EAST), None)
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(4, 4), Direction.EAST), None)
        self.assertEqual(self._grid.get_next_cell_coordinates(
            Coordinates(4, 4), Direction.NORTH), None)


if __name__ == "__main__":
    unittest.main()
