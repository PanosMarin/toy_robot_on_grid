import unittest
from unittest.mock import MagicMock, patch
from toy_robot.utils import Direction, Coordinates
from toy_robot.toy_robot import Robot, RobotApiHandler, MoveRobotCommand, PlaceRobotCommand, ReportRobotCommand, TurnRobotCommand, RobotRotation, NopRobotCommand
from io import StringIO
from sys import stdout


class Test_Robot(unittest.TestCase):
    '''Tests for the Robot class'''

    def setUp(self):
        self._grid = MagicMock()
        self._command_receiver = MagicMock()
        self._robot = Robot(self._grid, self._command_receiver)

    def test_direction_property(self):
        '''Test Robot.direction property'''
        self.assertEqual(self._robot.direction, None)
        self._robot.direction = Direction.NORTH
        self.assertEqual(self._robot.direction, Direction.NORTH)

    def test_coordinates_property(self):
        '''Test Robot.coordinates property'''
        self.assertEqual(self._robot.coordinates, None)
        self._robot.coordinates = Coordinates(0, 0)
        self.assertEqual(self._robot.coordinates, Coordinates(0, 0))

    def test_get_grid(self):
        '''Test Robot.get_grid method'''
        self.assertEqual(self._robot.get_grid(), self._grid)

    def test_robot_on_grid(self):
        '''Tests the Robot.is_on_grid method'''
        self.assertEqual(self._robot.is_on_grid(), False)
        self._robot.direction = Direction.EAST
        self.assertEqual(self._robot.is_on_grid(), False)
        self._robot.coordinates = Coordinates(0, 0)
        self.assertEqual(self._robot.is_on_grid(), True)

    def test_robot_spin(self):
        '''Tests the Robot.spin method'''
        command = MagicMock()
        command.execute = MagicMock(side_effect=[True])
        self._command_receiver.recv = MagicMock(side_effect=[command, None])
        self._robot.spin()
        self.assertEqual(self._command_receiver.recv.call_count, 2)


class Test_RobotApiHandlerPlaceCommandGeneration(unittest.TestCase):
    '''Tests place command generation in RobotApiHandler class'''

    def test_valid_place_command_generation(self):
        '''Test valid place command generation'''
        command: PlaceRobotCommand = RobotApiHandler.generate_command(
            'PLACE 0,0,NORTH')
        self.assertEqual(type(command), PlaceRobotCommand)
        self.assertEqual(command._coordinates, Coordinates(0, 0))
        self.assertEqual(command._direction, Direction.NORTH)

    def test_incorrect_format_place_command(self):
        '''Test incorrect format.'''
        command = RobotApiHandler.generate_command('PLACE 0,0')
        self.assertEqual(type(command), NopRobotCommand)

    def test_incorrect_arguments_place_command(self):
        '''Test incorrect arguments.'''
        command = RobotApiHandler.generate_command('PLACE X,0,NORTH')
        self.assertEqual(type(command), NopRobotCommand)
        command = RobotApiHandler.generate_command('PLACE 0,X,NORTH')
        self.assertEqual(type(command), NopRobotCommand)
        command = RobotApiHandler.generate_command('PLACE 0,0,X')
        self.assertEqual(type(command), NopRobotCommand)


class Test_RobotApiHandlerMoveCommandGeneration(unittest.TestCase):
    '''Tests move command generation in RobotApiHandler class'''

    def test_valid_move_command(self):
        '''Test valid move command generation.'''
        command: MoveRobotCommand = RobotApiHandler.generate_command('MOVE')
        self.assertEqual(type(command), MoveRobotCommand)

    def test_incorrect_format_place_command(self):
        '''Test incorrect format.'''
        command = RobotApiHandler.generate_command('MOVE 1')
        self.assertEqual(type(command), NopRobotCommand)


class Test_RobotApiHandlerTurnCommandGeneration(unittest.TestCase):
    '''Tests turn command generation in RobotApiHandler class'''

    def test_valid_turn_command(self):
        '''Test valid turn command generation.'''
        command: TurnRobotCommand = RobotApiHandler.generate_command('LEFT')
        self.assertEqual(type(command), TurnRobotCommand)
        self.assertEqual(command._robot_rotation, RobotRotation.LEFT)

        command: TurnRobotCommand = RobotApiHandler.generate_command('RIGHT')
        self.assertEqual(type(command), TurnRobotCommand)
        self.assertEqual(command._robot_rotation, RobotRotation.RIGHT)

    def test_incorrect_format_turn_command(self):
        '''Test incorrect format.'''
        command = RobotApiHandler.generate_command('LEFT 1')
        self.assertEqual(type(command), NopRobotCommand)


class Test_RobotApiHandlerReportCommandGeneration(unittest.TestCase):
    '''Tests report command generation in RobotApiHandler class'''

    def test_valid_report_command(self):
        '''Test valid report generation format.'''
        command: ReportRobotCommand = RobotApiHandler.generate_command(
            'REPORT')
        self.assertEqual(type(command), ReportRobotCommand)

    def test_incorrect_format_turn_command(self):
        '''Test incorrect format.'''
        command = RobotApiHandler.generate_command('REPORT 1')
        self.assertEqual(type(command), NopRobotCommand)


class Test_MoveRobotCommand(unittest.TestCase):
    '''Tests the MoveRobotCommand class'''

    def setUp(self):
        self._grid = MagicMock()
        self._command_receiver = MagicMock()
        self._robot = Robot(self._grid, self._command_receiver)
        self._move_command = MoveRobotCommand()

    def test_valid_move_command(self):
        '''Test valid move robot command.'''
        self._robot.direction = Direction.NORTH
        self._robot.is_on_grid = MagicMock()
        self._robot.is_on_grid.return_value = True
        self._grid.get_next_cell_coordinates = MagicMock()
        self._grid.get_next_cell_coordinates.return_value = Coordinates(1, 1)
        self.assertEqual(self._move_command.execute(self._robot), True)
        self.assertEqual(self._robot.coordinates, Coordinates(1, 1))
        self.assertEqual(self._robot.direction, Direction.NORTH)

    def test_invalid_move_command_robot_not_on_grid(self):
        '''Test invalid move robot command due to robot not being on the grid.'''
        self._robot.direction = Direction.NORTH
        self._robot.is_on_grid = MagicMock()
        self._robot.is_on_grid.return_value = False
        self._grid.get_next_cell_coordinates = MagicMock()
        self._grid.get_next_cell_coordinates.return_value = Coordinates(1, 1)
        self.assertEqual(self._move_command.execute(self._robot), False)
        self.assertEqual(self._robot.coordinates, None)
        self.assertEqual(self._robot.direction, Direction.NORTH)

    def test_invalid_move_command_robot_invalid_next_cell(self):
        '''Test invalid move robot command due the next cell grid not being available.'''
        self._robot.direction = Direction.NORTH
        self._robot.is_on_grid = MagicMock()
        self._robot.is_on_grid.return_value = True
        self._grid.get_next_cell_coordinates = MagicMock()
        self._grid.get_next_cell_coordinates.return_value = None
        self.assertEqual(self._move_command.execute(self._robot), False)
        self.assertEqual(self._robot.coordinates, None)
        self.assertEqual(self._robot.direction, Direction.NORTH)


class Test_PlaceRobotCommand(unittest.TestCase):
    '''Tests the MoveRobotCommand class'''

    def setUp(self):
        self._grid = MagicMock()
        self._command_receiver = MagicMock()
        self._robot = Robot(self._grid, self._command_receiver)

    def test_valid_place_command(self):
        '''Test execution of valid place command.'''
        place_command = PlaceRobotCommand(Coordinates(0, 0), Direction.NORTH)
        self._grid.is_valid_cell = MagicMock()
        self._grid.is_valid_cell.return_value = True
        self.assertEqual(place_command.execute(self._robot), True)
        self.assertEqual(self._robot.coordinates, Coordinates(0, 0))
        self.assertEqual(self._robot.direction, Direction.NORTH)

    def test_invalid_place_command_invalid_cell(self):
        '''Test execution of invalid place command due to cell not being valid.'''
        place_command = PlaceRobotCommand(Coordinates(0, 0), Direction.NORTH)
        self._grid.is_valid_cell = MagicMock()
        self._grid.is_valid_cell.return_value = False
        self.assertEqual(place_command.execute(self._robot), False)
        self.assertEqual(self._robot.coordinates, None)
        self.assertEqual(self._robot.direction, None)


class Test_TurnRobotCommand(unittest.TestCase):
    '''Test the TurnRobotCommand class'''

    def setUp(self):
        self._grid = MagicMock()
        self._command_receiver = MagicMock()
        self._robot = Robot(self._grid, self._command_receiver)

    def test_valid_turn_command(self):
        '''Test execution of valid turn command.'''
        self._robot.direction = Direction.NORTH
        self._robot.is_on_grid = MagicMock()
        self._robot.is_on_grid.return_value = True

        command_left = TurnRobotCommand(RobotRotation.LEFT)
        self.assertEqual(command_left.execute(self._robot), True)
        self.assertEqual(self._robot.direction, Direction.WEST)

        command_right = TurnRobotCommand(RobotRotation.RIGHT)
        self.assertEqual(command_right.execute(self._robot), True)
        self.assertEqual(self._robot.direction, Direction.NORTH)

    def test_invalid_turn_command_robot_not_on_grid(self):
        '''Test invalid turn robot command due to robot not being on the grid.'''
        self._robot.direction = Direction.NORTH
        self._robot.is_on_grid = MagicMock()
        self._robot.is_on_grid.return_value = False

        command_left = TurnRobotCommand(RobotRotation.LEFT)
        self.assertEqual(command_left.execute(self._robot), False)
        self.assertEqual(self._robot.direction, Direction.NORTH)

        command_right = TurnRobotCommand(RobotRotation.RIGHT)
        self.assertEqual(command_right.execute(self._robot), False)
        self.assertEqual(self._robot.direction, Direction.NORTH)


class Test_ReportRobotCommand(unittest.TestCase):
    '''Test the ReportRobotCommand class'''

    def setUp(self):
        self._grid = MagicMock()
        self._command_receiver = MagicMock()
        self._robot = Robot(self._grid, self._command_receiver)
        self._report_command = ReportRobotCommand()

    def test_valid_report_command(self):
        '''Test valid execution of report command.'''
        with patch("sys.stdout", new=StringIO()) as console:
            self._robot.coordinates = Coordinates(0, 0)
            self._robot.direction = Direction.NORTH
            self.assertEqual(self._report_command.execute(self._robot), True)
            self.assertEqual(console.getvalue().strip(), "Output: 0,0,NORTH")

    def test_invalid_report_command_robot_not_on_grid(self):
        '''Test valid execution of report command due to robot not being on the grid..'''
        self.assertEqual(self._report_command.execute(self._robot), False)


if __name__ == "__main__":
    unittest.main()
