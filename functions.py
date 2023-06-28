import numpy as np
import random
import copy

RADIUS = 1 # how long the arm of the rod extends from the center.

# FUNCTIONS OF THE ROD OBJECT

    # A rod is assumed to be encoded as (x,y,o), where x,y are the coordinates
    # of the center of the rod, and o is a binary integer 1: Vertical, 0: Horizontal

def translate_rod(rod):
    """
    Simple function to write the orientation as a string for demonstration
    purposes.
    """
    return (rod[0],rod[1],'ver' if rod[2] else 'hor')

def point_in_box(x,y,lx,ly):
    """ Check in point lies within the box of size lx x ly """
    return all([ 0 <= y, y < ly , 0 <= x, x < lx ])


def sits_in_box(rod, len_x, len_y):
    """
    This function checks that the rod sits within the given box.
    Inputs:
        - rod: a tuple containing x,y position of center and orientation
        - len_x, len_y: the dimensions of the labyrinth
    Output:
        - boolean attesting to whether the rod sits entirely within the frame
    """
    x = rod[0]
    y = rod[1]
    o = rod[2]
    if bool(o): # rod is vertical
        return all([ RADIUS <= y, y < len_y - RADIUS, 0 <= x, x < len_x ])
    else: # rod is horizontal
        return all([ 0 <= y, y < len_y, RADIUS <= x, x < len_x - RADIUS])

def get_xs_ys(rod):
    """
    Gives xs and ys list of all positions.
    Input:
        - rod: a tuple containing x,y position of center and orientation

    Output:
        - xs, ys: two lists of the same length, non-decreasing lists of the x and y
            positions of all nodes of the rod
    """
    x,y,o = rod

    l = (2*RADIUS + 1) # the total length of the rod

    # generate all the points to check
    if o: # if rod  is vertical
        ys = [y - RADIUS, y, y + RADIUS]
        xs = l*[x]
    else: # if rod is horizontal
        xs = [x - RADIUS, x, x + RADIUS]
        ys = l*[y]
    return xs,ys

def rotate_rod(rod):
    """
    This function changes the orientation of the rod from vertical to horizontal
    and viceverse.

    Input:
        - rod: a tuple containing x,y position of center and orientation
    Output:
        - the numpy array of the rotated rod
    """

    x,y,o = rod
    new_o = (o + 1) % 2

    return (x,y,new_o)

def shift_rod(rod, s, delta = 1):
    """
    This functions displaces the rod by delta units (global constant).
    Displacement is encoded in cardinal directions, north, south, west, east
    Inputs: 
        - rod: a tuple containing x,y position of center and orientation
        - s: a character/string, either 'e' (DELTA+1 x), 'w' (-1 x), 'n' (-1 y) or 's' (+1 y)
        - delta (optional): the amount of units to shift
    Outputs:
        - the numpy array encoding the new rod with the shift
    """

    x,y,o = rod

    if s == 'e':
        x += delta
    elif s == 'w':
        x -= delta
    elif s == 's':
        y += delta
    elif s == 'n':
        y -= delta
    else:
        raise ValueError('Supplied shift is not valid.')
    return (x,y,o)


# FUNCTIONS OF THE LABYRINTH OBJECT

def get_shape(lab):
    """
    This function gets the size of the labyrinth and validates that it has
    viable rows.
    """

    len_y = len(lab)

    if len_y == 0:
        raise ValueError("Invalid labyrinth!")

    len_x = len(lab[0])

    for k in range(len_y):
        if len(lab[k]) != len_x:
            raise ValueError("Invalid labyrinth!")
    return len_x, len_y

def str2lab(string):
    """
    This function creates an immutable object encoding
    the labyrinth, namely a list of lists. It assumes that
    the labyrinth is of fixed 5 x 9 size. 

    It is written for convenience of testing.

    Inputs:
        - string: a string of length 45 encoding where the 
            obstacles are. '.' means air, '#' means obstacle.
    Outputs:
        - lab: a list of lists encoding the labyrinth
    """

    if len(string) % 9 != 0:
        raise ValueError("Not a valid labyrinth of 5 x 9")

    if len(string) == 9:
        return [list(string)]

    else:
        row = string[:9]
        return [list(row)] + str2lab(string[9:])

def put_obstacles(lab, list_of_obstacles):
    """
    This is a test-helping function allowing to modify a given
    lab and putting new obstacles.

    copy.deepcopy( ) method is used to create new labs
    instead of simply modifying the existing one in memory

    Inputs:
        - lab: a list of 5 lists, each of length 9
        - list_of_obstacles: a list of tuples containing the
            indices of where to put an obstacle
    Output:
        - new_lab: a list of 5 lists, each of length 9
    """

    # this seems to be modifying the labyrinth in place
    # unless I make a specific copy

    new_lab = copy.deepcopy(lab)
    for i,j in list_of_obstacles:
        new_lab[j][i]='#'
    return new_lab

def random_lab(lx = 9, ly = 5, fill = 0.2):
    """
    This function generates a labyrinth with approximate pre-established
    filling with blocks.

    Optional inputs:
        - fill: float between 0 and 1, percentage of filling
        - lx, ly: positive integers, size of the labyrinth
    Output:
        - list of list of strings, the labyrinth generated
    """
    lab_base = str2lab(5*'.........')
    new_lab = copy.deepcopy(lab_base)
    for i in range(lx):
        for j in range(ly):
            if random.random() <= fill:
                new_lab[j][i] = '#'
    return new_lab

 
# FUNCTIONS RELATED TO ROD - LABYRINTH INTERACTION



def point_collision(x,y,lab):
    """
    This function checks whether a point is a solid block of the labyrinth.
    """
    lx,ly = get_shape(lab)
    if not point_in_box(x,y,lx,ly):
        return False # otherwise we cannot test if the point is a block
    return (lab[y][x] == '#') 

def rod_collision(rod, lab):
    """
    This function checks whether the given rod sits within
    the labyrinth without colliding with the walls. 
    Inputs:
        - rod: a tuple containing x,y position of center and orientation
        - lab: the list of lists encoding the labyrinth
    Outpus:
        - a boolean, True if there is a collision or exits the box, False otherwise.
    """
    len_x, len_y = get_shape(lab)
    if not sits_in_box(rod, len_x, len_y):
        return True

    xs, ys = get_xs_ys(rod)
    l = len(xs) # total length of the rod

    for k in range(l):
        if point_collision(xs[k],ys[k],lab):
            return True
    return False

def can_rotate(rod, lab, verbose = False):
    """
    This function checks whether there is a L x L box of air
    surrounding the rod within the confines of the box.

    Inputs:
        - rod: a tuple containing x,y position of center and orientation
        - lab: the list of lists encoding the labyrinth
    Output:
        - bool, whether rod can be rotated collisionless within labyrinth
    """
    x,y,o = rod
    l = 2*RADIUS + 1

    xs = [x + shift for shift in range(-RADIUS,RADIUS+1)]
    ys = [y + shift for shift in range(-RADIUS,RADIUS+1)]
    lx,ly = get_shape(lab)
    for px in xs:
        for py in ys:
            if any([point_collision(px,py,lab), not point_in_box(px,py,lx,ly)]):
                if verbose:
                    print([point_collision(px,py,lab), point_in_box(px,py,lx,ly)])
                    print(f"Point {px,py} does not pass rotation check")
                return False
    return True

def print_all(rod, lab, omit_rod = False):
    """
    This function prints the rod in the labyrinth. Rod points are marked with
    'X', and block elements of the labyrinth are marked with '#'.
    It assumes the rod is within the box, but it does not assume that there
    is no collision labyrinth - rod.

    Inputs:
        - rod: a tuple containing x,y position of center and orientation
        - lab: the list of lists encoding the labyrinth
    """
    print_lab = copy.deepcopy(lab)


    len_x, len_y = get_shape(lab)

    if not omit_rod:
        if not sits_in_box(rod, len_x, len_y):
            raise ValueError("Rod exits the boundary of the box")

        xs, ys = get_xs_ys(rod)

        for k in range(len(xs)):
            i = xs[k]
            j = ys[k]
            if point_collision(i,j,lab):
                print_lab[j][i] = 'C' # represent collision
            else:
                print_lab[ys[k]][xs[k]] = 'X' # represent rod, if it sits within
    for row in print_lab:
        print(row)

    return None

def show_config(rod,lab):
    """
    Function that prints a rod configuration in its ambient labyrinth.
    It assumes the rod is within the box, but it does not assume that there
    is no collision labyrinth - rod.
    Inputs:
        - rod: a tuple containing x,y position of center and orientation
        - lab: the list of lists encoding the labyrinth
    """

    print_all(rod, lab)
    lx, ly = get_shape(lab)

    print(f"Collision: {rod_collision(rod,lab)}")
    print(f"Possible moves: {allowed_moves(rod, lab)}")

# FUNCTIONS RELATED TO LABYRINTH EXPLORATION

def allowed_moves(rod, lab, delta = 1, give_neighbors = False):
    """
    This function gives the allowed moves for a given configuration of the
    rod and the lab. It checks whether the shifted (defaulte 1 unit of shift)
    rod sits within the labyrinth and does not collide. If it can rotate,
    the test already passes, the function can_rotate( ) already implements
    these tests.

    Inputs:
        - rod: a tuple containing x,y position of center and orientation
        - lab: the list of lists encoding the labyrinth
        - delta (optional): the size of steps that can be taken in shifts (default 1)
        - give_neighbors (optional): when set to true, the function will 
            output a list of tuples, all accesible rod states from the given one
    Output:
        - a string composed of the possible shifts and moves, 
            encoded as 'e','w','s','n','r'
    """

    len_x, len_y = get_shape(lab)

    moves = ""
    list_of_neighbors = []

    for s in "ewsn": # test which shifts are allowed (sit within box, don't collide)
        possible_rod = shift_rod(rod, s)
        if sits_in_box(possible_rod, len_x, len_y) & (not rod_collision(possible_rod, lab)):
            moves = moves + s
            if give_neighbors:
                list_of_neighbors.append(possible_rod)

    if can_rotate(rod, lab): # already implemented function for checking allowed rotation
        moves = moves + "r"
        if give_neighbors:
            list_of_neighbors.append(rotate_rod(rod))

    if give_neighbors: 
        return list_of_neighbors
    else:
        return moves


def config_space(lab, verbose = False, count_states = False):
    """
    This function generates all the vertices in the configuration space
    for the rod in the labyrinth.

    Inputs:
        - lab: the list of lists encoding the labyrinth
    Output:
        - a list of all the possible rod arrays that are valid
    """
    len_x, len_y = get_shape(lab)

    # we assume that the labyrinth is valid

    configurations = []
    count = 0

    for x in range(0,len_x):
        for y in range(0,len_y):
            for o in [0,1]:
                rod = (x,y,o)
                if all([sits_in_box(rod, len_x, len_y), not(rod_collision(rod,lab))]):
                    if verbose:
                        print(f"Rod {rod} is viable")
                        print(f"In box: {sits_in_box(rod, len_x, len_y)}")
                        print(f"Collision: {rod_collision(rod,lab)}")
                        show_config(rod,lab)
                    configurations.append(rod)
                    count += 1
                elif verbose:
                    print(f"Rod {rod} is not viable")
                    print(f"In box: {sits_in_box(rod, len_x, len_y)}")
                    print(f"Collision: {rod_collision(rod,lab)}")

    if count_states:
        return configurations, count
    else:
        return configurations


def touches_target(rod,xt,yt):
    """
    This function checks whether a rod given by a tuple touches a target 
    coordinate. It checks ALL rod nodes, just in case the target is not
    in a corner of the labyrinth.

    Input:
        - rod: a tuple containing x,y position of center and orientation
        - xt, yt: integer coordinates to check
    Output:
        - bool
    """
    x,y,o = rod
    if not o: # vertical
        #print("Hor")
        #print([(x+1,y) == (xt,yt), (x,y) == (xt, yt), (x-1,y) == (xt,yt)])
        return any([(x+1,y) == (xt,yt), (x,y) == (xt, yt), (x-1,y) == (xt,yt)])
    else: # horizontal
        #print("Vertical")
        #print([(x,y+1) == (xt,yt), (x,y) == (xt, yt), (x,y-1) == (xt,yt)])
        return any([(x,y+1) == (xt,yt), (x,y) == (xt, yt), (x,y-1) == (xt,yt)])
     

# Function that gives the solution to the exercise

def solution(lab, source = (1,0,0), target=None, return_distance_only = True):
    """
    This function finds the distance in a given labyrinth between a source
    configuration of the rod and a target block. It implements a slight
    modification of the Dijkstra algorithm.

    Inputs:
        - lab: a list of list of characters, encoding the labyrinth with '.' and '#'
        - source: a tuple of 3 integers, the center and orientation of the rod at
            the initial configuration.
        - target: a tuple of 2 integers, the block the rod must touch to solve
            the problem of transport.
    Outputs: depending on the value of the flag return_distance_only:
        - distance: the distance as computed by the Dijkstra algorithm

        - dist_dict: a dictionary of distances to the 
            -1 if the target is inaccessible.
        - prev_dict: a dictionary mapping each node to its predecessor in
            the shortest path found
        - access: the specific configuration in which the rod touches the
            target block. There could be several but by the nature of Dijkstra
            algorithm the distance found is minimal.
    """
    # Important initializations

    lx, ly = get_shape(lab) # size of labyrinth


    infinity = 2*lx*ly # upper bound of the amount of states. Only if the
                        # graph is a chain of nodes connected by one edge will
                        # the distance approach this value

    infinity = float("inf")

    # Workaround for default value of the target depending on size of the lab

    if target == None:
        target = (lx-1,ly-1)
    tx, ty = target  # coordinate of target location

    # Easy checks for unfeasibility:

    if rod_collision(source, lab):
        raise ValueError("The initial configuration of rod collides with the labyrinth.")
    if point_collision(target[0],target[1],lab):
        print("The target location is blocked by the labyrinth.")
        return -1

    # Initialization of distances and previous_node dictionaries

    dist_dict = {}
    prev_dict = {}
    Q = config_space(lab) # generates all vertices in the graph, i.e.
                                # possible states of the rod
    for c in Q:
        dist_dict[c] = infinity # all nodes are initialized at very big distance
        prev_dict[c] = None     # no previous knowledge of what node to come from to get                                    # in shortest path to c

    dist_dict[source] = 0 # basic initialization

    # main loop of Dijkstra algorithm

    while Q:

        # choose u some unvisited node of minimal distance to source
        qs_with_distances = {q:dist_dict[q] for q in Q}
        u = min(qs_with_distances, key = qs_with_distances.get)
        
        if touches_target(u,tx,ty): # we must have finished since we arrived at target!
            access = u
            break # exit while loop
        Q.remove(u) # delete it from the "unvisited" list

        # explore the neighbors of u and maybe update their distances to source
        neighbors = allowed_moves(u, lab, give_neighbors = True)
        for n in neighbors:
            if n not in Q:
                continue
            possibly_new_distance = 1 + dist_dict[u]
            if possibly_new_distance < dist_dict[n]:
                dist_dict[n] = possibly_new_distance
                prev_dict[n] = u
   
    if return_distance_only:
        distance = dist_dict[access]
        if distance == float('inf'): # workaround to check the conventions of the challenge
            distance = -1
        return distance
    else:
        return dist_dict, prev_dict, access

def show_me_trajectory(lab, animation = True):

    dist, prev, access  = solution(lab, return_distance_only = False)

    distance = dist[access] # the distance

    if distance == float('inf'): # if there is no solution, exit the function
        print('There is no solution to this labyrinth.')
        return

    source = (1,0,0)
    trajectory = []
    # iterate backward in the prev dictionary
    p = access
    trajectory = [p] + trajectory
    while p != source:
        p = prev[p]
        trajectory = [p] + trajectory

    print(trajectory)
    if animation:
        print("Printing trajectory of minimal distance:")
        for config in trajectory:
            print_all(config, lab)
            input(" (press any key to proceed) ")
    else:
        print("> Found path:")
        for step in trajectory:
            print(translate_rod(step))
    return
