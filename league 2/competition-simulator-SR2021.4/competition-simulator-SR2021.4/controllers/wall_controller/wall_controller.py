import sys
from typing import cast, List
from pathlib import Path

from controller import Node, Supervisor

# Velocity matrices contain linear and rotational velocities [x, y, z, rot_x, rot_y, rot_z]
# -0.3m/s is used since the wall is 0.3m tall
# so the wall will have fully retracted after 1 second
LINEAR_DOWNWARDS = [0, -0.3, 0, 0, 0, 0]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(1, str(REPO_ROOT / 'modules'))

import controller_utils  # isort:skip


def move_walls_after(seconds: int) -> None:
    robot = Supervisor()
    timestep = robot.getBasicTimeStep()
    walls: List[Node] = [
        cast(Node, robot.getFromDef('west_moving_wall')),
        cast(Node, robot.getFromDef('east_moving_wall')),
    ]

    if controller_utils.get_robot_mode() == 'comp':
        # Interact with the supervisor "robot" to wait for the start of the match.
        while robot.getCustomData() != 'start':
            robot.step(int(timestep))

    # wait for the walls to start moving in ms
    robot.step(seconds * 1000)

    print('Moving arena walls')  # noqa: T001
    for wall in walls:
        wall.setVelocity(LINEAR_DOWNWARDS)

    # wait for the walls to reach their final location
    robot.step(1000)

    for wall in walls:
        wall.resetPhysics()


if __name__ == "__main__":
    move_walls_after(seconds=60)
