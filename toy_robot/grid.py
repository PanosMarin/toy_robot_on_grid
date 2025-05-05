from toy_robot.utils import Direction, Coordinates
from abc import ABC
from typing import Dict, List
from abc import abstractmethod


class Cell:
    """Represents a cell in a grid."""

    def __init__(self, x: int, y: int):
        """
        Initialise a cell at a given (x, y) coordinate.

        Args:
            x (int): The horizontal position of the cell.
            y (int): The vertical position of the cell.
        """
        self._coordinates = Coordinates(x, y)
        self._neighbours: Dict[Direction, Cell] = {}

    def set_neighbour(self, neighbour: 'Cell', direction: Direction) -> None:
        """
        Set the neighbouring cell at a specific direction.

        Args:
            neighbour (Cell): The neighbouring cell.
            direction (Direction): The neighbouring direction.
        Raises:
            RuntimeError if neighbour already exists in neighbouring direction
        """
        if direction in self._neighbours.keys():
            raise RuntimeError(
                "Cell already has a neighbour in direction {direction.name}")
        self._neighbours[direction] = neighbour
        neighbour._neighbours[direction.opposite] = self

    def get_neighbour(self, direction: Direction) -> 'Cell':
        """
        Gets neighbouring cell in specific direction.

        Args:
            direction (Direction): The neighbouring direction.
        Returns:
            Cell: Neigbouring cell, or None if no neighbouring cell in direction.
        """
        return self._neighbours.get(direction, None)

    def get_coordinates(self) -> Coordinates:
        '''
        Gets coordinates of the cell.

        Returns:
            Coordinates: Coordinates of the cell.
        '''
        return Coordinates(self._coordinates.x, self._coordinates.y)

    def __str__(self):
        neighbours = {
            direction.name: f"Cell coordinates {cell.get_coordinates()}" for direction,
            cell in self._neighbours.items()}
        return f'Coordinates ({self._coordinates}) neighbours {neighbours}'

    def __eq__(self, other: 'Cell') -> bool:
        return self._coordinates.x == other._coordinates.x and self._coordinates.y == other._coordinates.y


class AbstractGrid(ABC):
    '''
    Abstract class for grid like structure that consists of Cell type objects.
    '''
    @abstractmethod
    def get_next_cell_coordinates(
            self,
            coordinates: Coordinates,
            direction: Direction) -> Coordinates:
        '''
        Queries grid structure for neighbouring cell coordinates.

        Args:
            coordinates (Coordinates): Coordinates of current cell.
            direction (Direction): Direction of current's cell neighbour
        Returns:
            Coordinates: Coordinates of neighbouring cell, or None if cell does not exist.
        '''
        pass

    @abstractmethod
    def is_valid_cell(self, coordinates: Coordinates) -> bool:
        '''
        Queries grid structure if cell coordinates are valid.

        Args:
            coordinates (Coordinates): Coordinates of querried cell.
        Returns:
            bool: True if coordinates cooresponds to valid cell, False if not.
        '''
        pass


class SquareGrid(AbstractGrid):
    '''
    Implementation of AbstractGrid interface for a square grid.
    '''

    def __init__(self, size: int):
        '''
        Initialises SquareGrid class.

        Args:
            size (int): Size of square grid.
        '''
        self._size: int = size
        self._cells: List[List[Cell]] = [
            [Cell(x, y) for y in range(size)] for x in range(size)]
        self._initialize_neighbors()

    def _initialize_neighbors(self):
        '''
        Initialises neighbours of square grid.
        '''
        for x in range(self._size):
            for y in range(self._size):
                cell: Cell = self._cells[x][y]
                if x < self._size - 1:
                    cell.set_neighbour(self._cells[x + 1][y], Direction.EAST)
                if y < self._size - 1:
                    cell.set_neighbour(self._cells[x][y + 1], Direction.NORTH)

    def get_next_cell_coordinates(
            self,
            coordinates: Coordinates,
            direction: Direction) -> Coordinates:
        '''
        Queries grid structure for neighbouring cell coordinates.

        Args:
            coordinates (Coordinates): Coordinates of current cell.
            direction (Direction): Direction of current's cell neighbour
        Returns:
            Coordinates: Coordinates of neighbouring cell, or None if cell does not exist.
        '''
        next_cell = self._cells[coordinates.x][coordinates.y].get_neighbour(
            direction)
        if next_cell is None:
            return None
        return next_cell.get_coordinates()

    def is_valid_cell(self, coordinates: Coordinates) -> bool:
        '''
        Queries grid structure if cell coordinates are valid.

        Args:
            coordinates (Coordinates): Coordinates of current cell.
        Returns:
            bool: True if coordinates coorespond to valid cell, False if not.
        '''
        return coordinates.x < self._size and coordinates.y < self._size

    def __str__(self):
        return '\n'.join([str(cell)
                         for cell_row in self._cells for cell in cell_row])
