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
