# Rigid rod pathfinding challenge

This repository contains a Python implementation for the pathfinding challenge
of finding the shortest way of tranporting a rigid rod, modelled as a 
3 x 1 matrix, within a labyrinth of size 9 x 5 with physical boundaries
and obstacles, from the (0,0) position to the (9,5) position. 

Allowed moves include:

- shifting horizontally or vertically the rod by 1 unit.
- rotating the rod from vertical to horizontal position and viceversa,
provided there's a surrounding empty 3 x 3 space.
    
The implemented solution should take as input the labyrinth (as a list
of lists of characters, `'.'` for air and `'#'` for denoting a solid block)
and output the number of moves required to transport the rod, or -1 in
case of this being impossible.

## How to use this:

Import the defined functions with `import functions` in any python script.
The relevant function is: `solution(lab)` where `lab` is a of type
`List[List[str]]` and the above conventions for solid and air blocks are
assumed. The function `solution(lab)` simply outputs the number of steps
required to translate the rod, and `-1` in case of this being impossible.

The function `show_trajectory(lab)` also allows for printing the steps
either graphically in a terminal display, or enumerating the intermediate
configurations of the shortest path found.

One can execute the `demo.py` with `python` to exhibit the behaviour
of the program with two selected examples of labyrinths, and it shows
in terminal-based animation the intermediate steps.

All functions in `functions.py` are documented and `tests.py` contains several
tests used for developing this project.

## About this module

This solution to the above challenge basically encodes the structures of the
labyrinth and constraints for the rod to move within it as a graph, and the
allowed moves connect different vertices (allowed states of the rod within
the labyrinth). 

The Dijkstra algorithm provides a solution to the problem of finding the distance
of two nodes in a graph, and this module implements this algorithm with a minor
modification, namely that there is not just one prescribed target vertex,
but rather one has to check all vertices that correspondi to the rod touching
the target block in the "physical" labyrinth.

## Generalizations

One could improve this module by implementing the A* algorithm, which 
uses heuristic distance functions to more efficiently find the shortest
path.
