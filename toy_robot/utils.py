from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    '''Possible directions of toy robot.'''
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4

    @property
    def opposite(self):
        '''Property to retrieve the opposite of the current direction.'''
        return {
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH
        }[self]

    @property
    def counter_clockwise(self):
        '''Property to retrieve the clockwise direction of the current direction.'''
        return {
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH,
            Direction.NORTH: Direction.WEST
        }[self]

    @property
    def clockwise(self):
        '''Property to retrieve the counter clockwise direction of the current direction.'''
        return {
            Direction.WEST: Direction.NORTH,
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST
        }[self]


@dataclass
class Coordinates:
    '''Dataclass representing coordinates on a grid system.'''
    x: int
    y: int
