from toy_robot.utils import Direction, Coordinates
from toy_robot.grid import AbstractGrid, SquareGrid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List


class RobotRotation(Enum):
    '''Enumeration representing the possible robot rotations.'''
    RIGHT = 0,
    LEFT = 1


class RobotCommand(ABC):
    '''Abstract class for robot command'''
    @abstractmethod
    def execute(self, robot: 'Robot') -> bool:
        '''
        Executes a robot command.

        Args:
            robot(Robot): Robot to execute the command.
        Returns:
            bool: True if operation was successful, False otherwise.
        '''
        pass


class NopRobotCommand(RobotCommand):
    def execute(self, robot: 'Robot') -> bool:
        '''
        No operation robot command.

        Args:
            robot(Robot): Robot to execute the command.
        Returns:
            bool: Returns always true.
        '''
        return True


class PlaceRobotCommand(RobotCommand):
    '''Implements a robot place command'''

    def __init__(self, coordinates: Coordinates, direction: Direction):
        '''
        Initialises a robot placement command.
        '''
        self._coordinates = coordinates
        self._direction = direction

    def execute(self, robot: 'Robot'):
        '''
        Places the robot on the grid.

        Args:
            robot(Robot): Robot to execute the command.
        Returns:
            bool: True if operation was successful, False otherwise.
        '''
        if robot.get_grid().is_valid_cell(self._coordinates):
            robot.coordinates = self._coordinates
            robot.direction = self._direction
            return True
        else:
            print(f'Cell with coordinates {self._coordinates} not valid.')
            return False


class MoveRobotCommand(RobotCommand):
    '''Implements a robot move command'''

    def execute(self, robot: 'Robot') -> bool:
        '''
        Moves robot to next grid cell.

        Args:
            robot(Robot): Robot to execute the command.
        Returns:
            bool: True if operation was successful, False otherwise.
        '''
        if not robot.is_on_grid():
            print('Robot not yet placed on grid. Move command not possible.')
            return False
        new_coordinates = robot.get_grid().get_next_cell_coordinates(
            robot.coordinates, robot.direction)
        if new_coordinates is None:
            return False
        robot.coordinates = new_coordinates
        return True


class TurnRobotCommand(RobotCommand):
    '''Implements a robot turn command'''

    def __init__(self, robot_rotation: RobotRotation):
        '''
        Initialises a robot rotation command.
        '''
        self._robot_rotation = robot_rotation

    def execute(self, robot: 'Robot') -> bool:
        '''
        Rotates robot clockwise or counter clockwise.

        Args:
            robot(Robot): Robot to execute the command.
        Returns:
            bool: True if operation was successful, False otherwise.
        '''
        if not robot.is_on_grid():
            print('Robot not yet placed on grid. Turn command not possible.')
            return False
        if self._robot_rotation == RobotRotation.RIGHT:
            robot.direction = robot.direction.clockwise
        else:
            robot.direction = robot.direction.counter_clockwise
        return True


class ReportRobotCommand(RobotCommand):
    '''Implements a robot report command'''

    def execute(self, robot: 'Robot') -> bool:
        '''
        Makes robot report position and direction.

        Args:
            robot(Robot): Robot to execute the command.
        Returns:
            bool: True if operation was successful, False otherwise.
        '''
        if not robot.is_on_grid():
            print('Robot not yet placed on grid.')
            return False
        coordinates = robot.coordinates
        print(
            f'Output: {coordinates.x},{coordinates.y},{robot.direction.name}')
        return True


class AbastractRobotApiHandler(ABC):
    '''Class that generates robot commands from API'''
    @classmethod
    @abstractmethod
    def generate_command(data: Any) -> RobotCommand:
        '''
        Generates robot command based on API specifics.

        Args:
            data(Any): Data specific to API for command generation.
        Returns:
            RobotCommand: Robot command generated
        '''
        pass


class RobotApiHandler(AbastractRobotApiHandler):
    '''Class that generates robot commands from string commands.'''
    initialised = False

    @classmethod
    def _initialise(cls):
        cls.initialised = True
        cls.api_generator_map = {
            'PLACE': cls._generate_place_command,
            'MOVE': cls._generate_move_command,
            'LEFT': cls._generate_turn_command,
            'RIGHT': cls._generate_turn_command,
            'REPORT': cls._generate_report_command
        }

    @classmethod
    def generate_command(cls, command: str) -> RobotCommand:
        '''
        Generates robot command based on API specifics.
        Args:
            data(str): Data specific to API for command generation.
        Returns:
            RobotCommand: Robot command generated.    
        '''
        if not cls.initialised:
            cls._initialise()
        try:
            data = command.split(' ')
            command_generator = cls.api_generator_map.get(data[0], None)
            if command_generator is None:
                raise RuntimeError('Not valid command type.')
            return command_generator(data)
        except Exception as e:
            print(f'Invalid command format. Exception {e}. Command {command}')
            return NopRobotCommand()

    @classmethod
    def _generate_place_command(cls, data: List[str]) -> PlaceRobotCommand:
        '''
        Generates a robot place command.

        Returns:
            PlaceRobotCommand: Returns a Place robot command with the specified parameters.
        Raises:
            Runtime error if command has invalid format.
            Value error if any of the parameters are not of the expected type.
        '''
        if len(data) != 2:
            raise RuntimeError('Invalid place command format.')
        params = data[1].split(',')

        if not params[0].isdigit():
            raise ValueError('X coordinate in not a digit.')
        if not params[1].isdigit():
            raise ValueError('X coordinate in not a digit.')
        if params[2] not in Direction.__members__:
            raise ValueError('Direction provided in command not implemented.')

        return PlaceRobotCommand(Coordinates(int(params[0]), int(params[1])),
                                 Direction[params[2]])

    @classmethod
    def _generate_turn_command(cls, data: List[str]) -> TurnRobotCommand:
        '''
        Generates a robot turn command.

        Returns:
            TurnRobotCommand: Returns a Turn robot command with the specified parameters.
        Raises:
            Runtime error if command has invalid format.
            Value error if any of the parameters are not of the expected type.
        '''
        if len(data) != 1:
            raise RuntimeError('Invalid turn command format.')
        if data[0] not in RobotRotation.__members__:
            raise RuntimeError('Invalid robot rotation command.')
        return TurnRobotCommand(RobotRotation[data[0]])

    @classmethod
    def _generate_move_command(cls, data: List[str]) -> MoveRobotCommand:
        '''
        Generates a robot move command.

        Returns:
            MoveRobotCommand: Returns a Move robot command with the specified parameters.
        Raises:
            Runtime error if command has invalid format.
            Value error if any of the parameters are not of the expected type.
        '''
        if len(data) != 1:
            raise RuntimeError('Invalid move command format.')
        return MoveRobotCommand()

    @classmethod
    def _generate_report_command(cls, data: List[str]) -> MoveRobotCommand:
        '''
        Generates a robot report command.

        Returns:
            MoveRobotCommand: Returns a Report robot command with the specified parameters.
        Raises:
            Runtime error if command has invalid format.
        '''
        if len(data) != 1:
            raise RuntimeError('Invalid report command format.')
        return ReportRobotCommand()


class AbstractCommandReceiver(ABC):
    '''
    Abstract class for command receiver.
    '''
    @abstractmethod
    def recv(self) -> RobotCommand:
        '''
        Returns:
            RobotCommand: Returns the robot command received.
        '''
        pass


class StubFileCommandReceiver(AbstractCommandReceiver):
    '''
    Abstract class for command receiver.
    '''

    def __init__(
            self,
            file: str,
            api_handler: AbastractRobotApiHandler = RobotApiHandler):
        with open(file, 'r') as f:
            self._commands: list[str] = f.readlines()
            self._api_handler = api_handler()

    def recv(self) -> RobotCommand:
        '''
        Returns:
            RobotCommand: Returns the robot command received.
        '''
        while True:
            if len(self._commands) < 1:
                return None
            command = self._api_handler.generate_command(
                self._commands.pop(0).strip('\n'))
            if command is None:
                continue
            return command


class Robot:
    '''Class that implements a robot on a grid like structure'''

    def __init__(
            self,
            grid: AbstractGrid,
            command_receiver: AbstractCommandReceiver):
        '''
        Initialises the toy robot.

        Args:
            grid(AbstractGrid): Grid for the robo to to be placed.
        '''
        self._coordinates: Coordinates = None
        self._direction: Direction = None
        self._grid = grid
        self._command_receiver = command_receiver

    @property
    def direction(self) -> Direction:
        '''Get direction'''
        return self._direction

    @direction.setter
    def direction(self, direction) -> None:
        """Set the direction."""
        self._direction = direction

    @property
    def coordinates(self):
        '''Get coordinates'''
        if self._coordinates is None:
            return None
        return Coordinates(self._coordinates.x, self._coordinates.y)

    @coordinates.setter
    def coordinates(self, coordinates: Coordinates):
        '''Set coordinates'''
        self._coordinates = Coordinates(coordinates.x, coordinates.y)

    def is_on_grid(self) -> bool:
        '''
        Checks if a robot has a valid grid position

        Returns:
            bool: Returns true if robot has been placed on the grid.
        '''
        return self._coordinates is not None and self._direction is not None

    def get_grid(self) -> AbstractGrid:
        '''Get grid'''
        return self._grid

    def spin(self):
        '''Spin robot to run through the commands. Exits when no more commands to be received.'''
        while True:
            command = self._command_receiver.recv()
            if command is None:
                break
            command.execute(self)
        print('No more commands to execute...')


class SimpleRobotOnGridFactory:
    '''Simple factory for application.'''

    def __init__(self):
        '''Initialises factory'''
        self._robot = None
        self._grid = None
        self._command_receiver = None

    def add_square_grid(self, grid_size: int) -> 'SimpleRobotOnGridFactory':
        '''
        Adds a square grid for the robot:

        Args:
            grid_size(int): Size of square grid.
        '''
        self._grid = SquareGrid(grid_size)
        return self

    def add_stub_command_receiver(self, file: str):
        '''
        Adds a stub file receiver for testing.

        Args:
            file(str): Path to file containing instructions.
        '''
        self._command_receiver = StubFileCommandReceiver(file)
        return self

    def create_robot(self) -> 'SimpleRobotOnGridFactory':
        '''
        Adds a square grid for the robot:

        Args:
            grid_size(int): Size of square grid.
        Raises:
            Runtime error if grid or command receiver are not initaliased.
        '''
        if self._grid is None:
            raise RuntimeError('Grid is not yet defined.')
        if self._command_receiver is None:
            raise RuntimeError('Command receiver is not yet defined.')
        return Robot(self._grid, self._command_receiver)
