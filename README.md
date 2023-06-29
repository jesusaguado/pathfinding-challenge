# Rigid rod pathfinding challenge

This repository contains a Python solution for the pathfinding challenge
of finding the shortest way of tranporting a rigid rod, modelled as a 
3 x 1 matrix, within a labyrinth of size 9 x 5 with physical boundaries
and obstacles, from the `(0,0)` position to the `(8,4)` position. 

Allowed moves include:

- shifting horizontally or vertically the rod by 1 unit.
- rotating the rod from vertical to horizontal position and viceversa,
provided there's a surrounding empty 3 x 3 space.
    
The implemented solution takes as input the labyrinth (as a list
of lists of characters, `'.'` for air and `'#'` for denoting a solid block)
and output the number of moves required to transport the rod, or -1 in
case of this being impossible.

## How to use this module

Import the defined functions with `import functions` in a python
script or interactive session.
The relevant function is: `solution(lab)` where `lab` is of type
`List[List[str]]` and the above conventions for solid and air blocks are
assumed. The function `solution(lab)` simply outputs the number of steps
required to translate the rod, and `-1` in case of this being impossible.

The function `show_trajectory(lab)` also allows for printing the steps
either graphically in a terminal display, or enumerating the intermediate
configurations of the shortest path found.

One can execute the `demo.py` with `python` to exhibit the behaviour
of the program on two selected examples of labyrinths, showing
in a terminal-based animation the intermediate steps.

All functions in `functions.py` are properly documented and `tests.py` 
contains several tests used for developing this project.

## About this module

This solution to the above challenge encodes the structures of the
labyrinth and constraints for the rod to move within it as a graph; the
allowed moves connect different vertices, which are nothing but 
allowed states of the rod within the labyrinth.

The Dijkstra algorithm provides a solution to the problem of finding the distance
of two nodes in a graph, and this module implements this algorithm with a minor
modification, namely that there is not just one prescribed target vertex,
but rather one has to check all vertices that correspond to the rod touching
the target block in the "physical" labyrinth.

## Further functionality and generalizations

The given solution does not assume a prefixed size of the labyrinth, and
one can pass different target locations in the function `solution()` with
by passing in the optional parameter `target = (x,y)`, and even modify
the starting configuration of the rod with the parameter `source = (x,y,o)`.
Here `x,y` mean either the target location or the center of the rod, and `o`
should be `1` if the rod is positioned vertically (aligned with y-axis)
or `0` if it is positioned horizontally.

One could improve this module by implementing the A* algorithm, which 
uses heuristic distance functions to more efficiently find the shortest
path.
