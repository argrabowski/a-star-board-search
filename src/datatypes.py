from __future__ import annotations

from enum import Enum, auto
from typing import Union


class PrintableFields(object):
    def __str__(self):
        return self.selfString()

    # def __repr__(self):
    #     return self.selfString()

    def selfString(self):
        return "<{} {}>".format(type(self).__name__, str(vars(self)))


class Vector2(PrintableFields):
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union[int, float]):
        return Vector2(self.x * other, self.y * other)

    def __eq__(self, other: Vector2):
        return self.x == other.x and self.y == other.y


class BoardState(PrintableFields):
    coords: Vector2
    direction: Direction
    bash: bool

    def __init__(self, coords: Vector2, direction: Direction, bash: bool):
        self.coords = coords
        self.direction = direction
        self.bash = bash

    def __hash__(self):
        return hash((self.coords.x, self.coords.y, self.direction.value, self.bash))

    def __copy__(self):
        return BoardState(Vector2(self.coords.x, self.coords.y), self.direction, self.bash)

    def heuristic(self, board: list[list[Union[int, str]]], heuristicType: int) -> int:
        goalCoords: Vector2 = search2DArray(board, 'G')

        ans = None

        match heuristicType:
            case 1:
                ans = 0
            case 2:
                ans = self.minOrthogonal(goalCoords)
            case 3:
                ans = self.maxOrthogonal(goalCoords)
            case 4:
                ans = self.manhattanDistanceToGoal(goalCoords)
            case 5:
                ans = self.manhattanDistanceWeighted(board, goalCoords)
            case 6:
                ans = 5 * self.manhattanDistanceWeighted(board, goalCoords)

        return ans

    def minOrthogonal(self, goal: Vector2) -> int:
        xDiff: int = abs(goal.x - self.coords.x)
        yDiff: int = abs(goal.y - self.coords.y)

        return min(xDiff, yDiff)

    def maxOrthogonal(self, goal: Vector2) -> int:
        xDiff: int = abs(goal.x - self.coords.x)
        yDiff: int = abs(goal.y - self.coords.y)

        return max(xDiff, yDiff)

    def manhattanDistanceToGoal(self, goal: Vector2) -> int:
        xDiff: int = abs(goal.x - self.coords.x)
        yDiff: int = abs(goal.y - self.coords.y)

        return xDiff + yDiff

    def manhattanDistanceWeighted(self, board: list[list[Union[int, str]]], goal: Vector2) -> int:
        xDiff: int = abs(goal.x - self.coords.x)
        yDiff: int = abs(goal.y - self.coords.y)
        distance = xDiff + yDiff

        lowestComplexity = 9

        # Find the lowest complexity
        for row in board:
            for tile in row:
                if isinstance(tile, int) and tile < lowestComplexity:
                    lowestComplexity = tile

        lowestComplexity = min(3, lowestComplexity)

        return distance * lowestComplexity


class Action(PrintableFields):
    actionType: ActionType
    state: BoardState
    cost: int
    totalCost: int
    prevAction: Action

    def __init__(self, actionType: ActionType, cost: int, totalCost: int, prevAction: Union[Action, None], state: BoardState):
        self.actionType = actionType
        self.state = state
        self.cost = cost
        self.totalCost = totalCost
        self.prevAction = prevAction

    def selfString(self):
        varDict = vars(self)
        if self.prevAction is not None:
            varDict['prevAction'] = "<Action {}>".format(hash(self.prevAction))
        return "<{} {}>".format(type(self).__name__, str(varDict))


class ActionType(Enum):
    TURNLEFT = auto()
    TURNRIGHT = auto()
    FORWARD = auto()
    BASH = auto()
    START = auto()

    def __str__(self):
        strings = {
            ActionType.TURNLEFT: "left",
            ActionType.TURNRIGHT: "right",
            ActionType.FORWARD: "forward",
            ActionType.BASH: "bash",
            ActionType.START: "start"
        }

        return str(strings[self])


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def right(direction: Direction):
        directions: list[Direction] = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

        if direction.value == len(directions) - 1:
            return Direction.UP
        else:
            return directions[direction.value + 1]

    @staticmethod
    def left(direction: Direction):
        directions: list[Direction] = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

        return directions[direction.value - 1]


def search2DArray(array, value) -> Union[Vector2, None]:
    """Searches a 2d array for the given value and returns a vector2 representing the coordinates of the first
    instance of value. Returns None if the value is not found."""

    coordinate = Vector2(-1, -1)

    for row in range(0, len(array)):
        rowArray = array[row]
        try:
            coordinate.x = rowArray.index(value)
            coordinate.y = row
            break
        except ValueError:
            continue

    if coordinate.x == -1:
        return None
    else:
        return coordinate