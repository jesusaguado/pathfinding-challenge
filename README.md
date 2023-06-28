# Rigid rod pathfinding challenge

This repo contains a Python implementation for the pathfinding challenge
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
The relevant functions are: `solution(lab)` where `lab` is a of type
`List[List[str]]` and the above conventions for solid and air blocks are
assumed. The function `solution(lab)` simply outputs the number of steps
required to translate the rod, and `-1` in case of this being impossible.

One can execute the `demo.py` with `python` to exhibit the behaviour
of the program with two selected examples of labyrinths, and it shows
in terminal-based animation the intermediate steps.

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
