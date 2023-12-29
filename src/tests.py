
import csv
import math
import random
from AStar import AStar
from fileparser import parseFile
from datatypes import Vector2
import time


def genBoard(xDim, yDim):
	retBoard = []

	for row in range(xDim):
		retBoard.append([])
		for col in range(yDim):
			retBoard[row].append(random.randrange(1, 10))

	start = Vector2(random.randrange(0, xDim), random.randrange(0, yDim))
	goal = Vector2(random.randrange(0, xDim), random.randrange(0, yDim))

	while goal == start:
		goal = Vector2(random.randrange(0, xDim), random.randrange(0, yDim))

	retBoard[start.y][start.x] = 'S'
	retBoard[goal.y][goal.x] = 'G'

	return retBoard


def increasingTimeTest(heuristic):
	averageTime = 0
	dims = 10

	table = [['size', 'averageTimes', 'explored']]

	while averageTime < 3:
		times = []
		explored = []

		for n in range(0, 4):
			board = genBoard(dims, dims)

			# Initialize, run, and time the pathfinder
			pathfinder = AStar(board, heuristic)

			print("Running on {0}x{0} board using heuristic {1}...".format(dims, heuristic))

			startTime = time.time()
			result = pathfinder.doAStar()
			timeTaken = time.time() - startTime

			# Append to averages
			times.append(timeTaken)
			explored.append(pathfinder.numExplored)

			table.append([dims, timeTaken, pathfinder.numExplored])

		averageTime = sum(times) / len(times)
		averageExplored = sum(explored) / len(explored)

		# dims += 2
		dims += math.ceil(30 - averageTime)

	fileName = "../time_increase.csv"
	with open(fileName, "w") as my_csv:
		csvWriter = csv.writer(my_csv, delimiter=',')
		csvWriter.writerows(table)


boards = []


for n in range(1, 11):
	boards.append(genBoard(50, 50))


def branchingFactorTests():
	table = [['Board', 'Heuristic', 'Time (s)', 'Nodes explored', 'Solution depth']]

	for heuristic in range(1, 7):
		for boardNumber in range(1, 11):
			board = boards[boardNumber]

			# Initialize, run, and time the pathfinder
			pathfinder = AStar(board, heuristic)

			print("Running on board {} board using heuristic {}...".format(boardNumber, heuristic))

			startTime = time.time()
			result = pathfinder.doAStar()
			timeTaken = time.time() - startTime

			# Append to table
			newRow = [boardNumber, heuristic, timeTaken, pathfinder.numExplored, len(result)]
			table.append(newRow)

	print("\nWriting to csv...")

	fileName = "../branching_factor_tests.csv"
	with open(fileName, "w") as my_csv:
		csvWriter = csv.writer(my_csv, delimiter=',')
		csvWriter.writerows(table)

	print("\n successfully written to {}!".format(fileName))


increasingTimeTest(6)
# branchingFactorTests()
