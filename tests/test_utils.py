import unittest
from unittest.mock import MagicMock, patch
from toy_robot.utils import Direction


class Test_Direction(unittest.TestCase):
    '''Unit tests for Direction class'''

    def test_opposite(self):
        '''Test for opposite property'''
        direction = Direction.NORTH
        self.assertEqual(direction.opposite, Direction.SOUTH)
        direction = Direction.SOUTH
        self.assertEqual(direction.opposite, Direction.NORTH)
        direction = Direction.EAST
        self.assertEqual(direction.opposite, Direction.WEST)
        direction = Direction.WEST
        self.assertEqual(direction.opposite, Direction.EAST)

    def test_clockwise(self):
        '''Test for clockwise site property'''
        direction = Direction.NORTH
        self.assertEqual(direction.clockwise, Direction.EAST)
        direction = Direction.EAST
        self.assertEqual(direction.clockwise, Direction.SOUTH)
        direction = Direction.SOUTH
        self.assertEqual(direction.clockwise, Direction.WEST)
        direction = Direction.WEST
        self.assertEqual(direction.clockwise, Direction.NORTH)

    def test_counter_clockwise(self):
        '''Test for clockwise site property'''
        direction = Direction.NORTH
        self.assertEqual(direction.counter_clockwise, Direction.WEST)
        direction = Direction.WEST
        self.assertEqual(direction.counter_clockwise, Direction.SOUTH)
        direction = Direction.SOUTH
        self.assertEqual(direction.counter_clockwise, Direction.EAST)
        direction = Direction.EAST
        self.assertEqual(direction.counter_clockwise, Direction.NORTH)


if __name__ == "__main__":
    unittest.main()
