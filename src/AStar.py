import copy
import heapq
import math
import sys
from typing import Union

from datatypes import *

class AStar:
	"""Class to store values for and run AStar pathfinding"""
	_board: list[list[Union[int, str]]]
	_currentAction: Action
	_actionQueue: dict[int, Action]
	_actionHeap: list[(int, int)]
	_endCoords: Vector2
	_exploredNodes: dict[int, Action]

	numExplored: int = 0
	heuristic: int

	def __init__(self, board: list[list[Union[int, str]]], heuristic: int):
		self._board = board

		startCoords = search2DArray(self._board, 'S')
		self._endCoords = search2DArray(self._board, 'G')

		# Start action queue
		self._currentAction = Action(ActionType.START, 0, 0, None, BoardState(startCoords, Direction.UP, True))
		self.heuristic = heuristic

		self._actionQueue = {}
		self._actionHeap = []
		self._exploredNodes = {}

		self.pushAction(self._currentAction)

	@staticmethod
	def aStar(board, heuristic: int) -> list[Action]:
		"""Run aStar on the given board with the given heuristic"""
		aStarObj = AStar(board, heuristic)

		return aStarObj.doAStar()

	@staticmethod
	def getTile(board, coords: Vector2):
		return board[coords.y][coords.x]

	@staticmethod
	def nextMoves(board, boardState: BoardState) -> list[BoardState]:
		"""Returns a list of actions representing the next possible moves given the board and current board state."""
		nextStates: list[BoardState] = []
		coords = boardState.coords
		boardSize = Vector2(len(board[0]), len(board))

		forwardCoords: Union[Vector2, None] = None
		# Get move forward move
		match boardState.direction:
			case Direction.UP:
				if coords.y > 0:
					forwardCoords = Vector2(coords.x, coords.y - 1)
			case Direction.RIGHT:
				if coords.x < boardSize.x - 1:
					forwardCoords = Vector2(coords.x + 1, coords.y)
			case Direction.DOWN:
				if coords.y < boardSize.y - 1:
					forwardCoords = Vector2(coords.x, coords.y + 1)
			case Direction.LEFT:
				if coords.x > 0:
					forwardCoords = Vector2(coords.x - 1, coords.y)

		# Construct and append forward action to list of states if forward state exists
		if forwardCoords is not None:
			forwardState = copy.deepcopy(boardState)
			forwardState.coords = forwardCoords
			forwardState.bash = True
			nextStates.append(forwardState)

			if boardState.bash:  # Add bash state if bash is possible
				bashState = copy.deepcopy(forwardState)
				bashState.bash = False
				nextStates.append(bashState)

		# Add rotate moves if bash was not just completed
		if boardState.bash:
			leftState: BoardState = copy.deepcopy(boardState)
			rightState: BoardState = copy.deepcopy(boardState)

			leftState.direction = Direction.left(boardState.direction)
			rightState.direction = Direction.right(boardState.direction)

			nextStates.append(leftState)  # left rotate
			nextStates.append(rightState)  # right rotate

		return nextStates

	@staticmethod
	def getComplexity(board: list[list[Union[int, str]]], coords: Vector2) -> int:
		"""Gets the complexity value for the tile at the given coordinates on the given board. Returns 1 if it is a
		goal or start state. """
		tileValue = AStar.getTile(board, coords)
		ans: int = 1

		if not isinstance(tileValue, str):
			ans = tileValue

		return ans

	@staticmethod
	def genActionList(currentAction: Action) -> list[Action]:
		"""Given the current action, returns the list of every subsequent action in order"""
		if currentAction.prevAction.actionType == ActionType.START:
			return [currentAction]

		actionList = AStar.genActionList(currentAction.prevAction)
		actionList.append(currentAction)

		return actionList

	def doAStar(self) -> list[Action]:
		"""Run the aStar algorithm with the initial values set within this object. Returns the sequence of actions in
		order to get from the start to the goal """
		currentTile = self._board[self._currentAction.state.coords.y][self._currentAction.state.coords.x]

		while currentTile != 'G':
			# Set the current action to the action in the queue with the lowest total cost
			self._currentAction = self.popLowestCostAction()

			# If not in goal state get a list of next possible actions
			nextActions = self.getNextActions()
			for action in nextActions:
				key = hash(action.state)
				if key in self._actionQueue:
					existingAction = self._actionQueue[key]
					if action.totalCost < existingAction.totalCost:
						self.pushAction(action)
				else:
					self.pushAction(action)

			# Delete current action from queue and add it to explored nodes
			self._exploredNodes[hash(self._currentAction.state)] = self._currentAction
			currentTile = self._board[self._currentAction.state.coords.y][self._currentAction.state.coords.x]

			# Increment explored nodes
			self.numExplored += 1

		# return if the current state is a goal state
		return AStar.genActionList(self._currentAction)

	def getLowestCostAction(self) -> Action:
		"""Searches through the lowest cost """
		lowestCostAction = list(self._actionQueue.values())[0]

		for action in self._actionQueue.values():
			lowestHeuristic: int = 0
			if lowestCostAction.state is not None:
				lowestHeuristic = lowestCostAction.state.heuristic(self._board, self.heuristic)

			if action.totalCost + action.state.heuristic(self._board, self.heuristic) < lowestCostAction.totalCost + lowestHeuristic:
				lowestCostAction = action

		return lowestCostAction

	def getNextActions(self) -> list[Action]:
		"""Generates a list of next possible actions given the current board state"""
		currentState: BoardState = self._currentAction.state
		actionList: list[Action] = []

		for state in AStar.nextMoves(self._board, currentState):
			if hash(state) in self._exploredNodes.keys():
				continue

			complexity = AStar.getComplexity(self._board, state.coords)

			if state.coords != currentState.coords:
				if state.bash:  # Forward Action
					cost = complexity
					actionList.append(
						Action(
							ActionType.FORWARD,
							cost,
							self._currentAction.totalCost + cost,
							self._currentAction,
							state
						)
					)

				else:  # Bash Action
					cost = 3
					actionList.append(
						Action(
							ActionType.BASH,
							cost,
							self._currentAction.totalCost + cost,
							self._currentAction,
							state
						)
					)

				continue

			# Turn actions
			if state.direction != currentState.direction:
				cost = math.ceil(complexity/2)
				actionType: ActionType = None
				if state.direction == Direction.left(currentState.direction):  # Turn left action
					actionType = ActionType.TURNLEFT

				elif state.direction == Direction.right(currentState.direction):  # Turn right action
					actionType = ActionType.TURNRIGHT

				# Add action to list
				actionList.append(
					Action(
						actionType,
						cost,
						self._currentAction.totalCost + cost,
						self._currentAction,
						state
					)
				)

		return actionList

	def pushAction(self, action: Action):
		key = hash(action.state)

		if key not in self._actionQueue:
			heapq.heappush(self._actionHeap, (action.totalCost + action.state.heuristic(self._board, self.heuristic),
										  hash(action.state)))

		self._actionQueue[hash(action.state)] = action

	def popLowestCostAction(self) -> Action:
		hash = heapq.heappop(self._actionHeap)[1]
		action = self._actionQueue[hash]
		del self._actionQueue[hash]

		return action
