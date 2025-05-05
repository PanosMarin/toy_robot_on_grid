from toy_robot.toy_robot import SimpleRobotOnGridFactory
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise RuntimeError('Invalid number of arguments provided.')
    robot_factory = SimpleRobotOnGridFactory()
    robot = robot_factory.add_square_grid(
        5).add_stub_command_receiver(sys.argv[1]).create_robot()
    robot.spin()
