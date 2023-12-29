# A-Star Board Search

## How to run
**You must use python 3.10 to run this project.**  
Enter the ./src directory and run:
```
python main.py [file_path] [heuristic]
```
* `file_path` is the file path for the board in the standard notation of your os
* `heuristic` is a number from 1-6 as listed in the projects spec

## Heuristic functions
The implementation of the heuristic functions are located in datatypes.py within the 'BoardState' class  
* heuristics 1-4 are as listed in the project spec
* heuristic 5 is the (manhattan distance to the goal) * min(3, lowest complexity on the board)
* heuristic 6 is 5*(heuristic 5) as listed in the project spec. It is not admissible
