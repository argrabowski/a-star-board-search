import sys
import time

from AStar import AStar
from fileparser import *

# Parse command line inputs
fileName = sys.argv[1]
heuristic: int = int(sys.argv[2])

board = parseFile(fileName)

# Initialize, run, and time the pathfinder
pathfinder = AStar(board, heuristic)

print("Running on {} using heuristic {}...\n".format(fileName, heuristic))

startTime = time.time()
result = pathfinder.doAStar()
timeTaken = time.time() - startTime

# Print results
print("Finished in {} secs".format(round(timeTaken, 3)))
print("Explored {} nodes".format(pathfinder.numExplored))
print("Average branching factor of {}\n".format(round(pathfinder.numExplored / len(result), 3)))

print("Actions")
for action in result:
	print("{:<10} ({}, {}) cost: {}".format(str(action.actionType), action.state.coords.x, action.state.coords.y,
											 action.cost))

print("\ntotal cost = {}".format(result[-1].totalCost))
