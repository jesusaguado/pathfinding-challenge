import numpy as np
import copy

RADIUS = 1 # how long the arm of the rod extends from the center.

# FUNCTIONS OF THE ROD OBJECT

def rod2tup(rod):
    """ Inverse function of the above """
    return (rod[0],rod[1],rod[2])

def create_rod(x,y,o):
    """
    This function creates a numpy array encoding the rod's position and
    orientation. Orientation is 0 if horizontal (aligned with x axis)
    or 1 if vertical (aligned with y axis.
    Inputs:
        - x,y: integers encoding the x and y position of the center of the rod
        - o: a binary integer encoding the orientation.
    Output:
        - numpy array or 3 integer elements.
    """
    return np.array([x,y,o])

def point_in_box(x,y,lx,ly):
    """ Check in point lies within the box of size lx x ly """
    return all([ 0 <= y, y < ly , 0 <= x, x < lx ])


def sits_in_box(rod_array, len_x, len_y):
    """
    This function checks that the rod sits within the given box.
    Inputs:
        - rod_array: a numpy array of 3 integer elements encoding the rod
            position and orientation
        - len_x, len_y: the dimensions of the labyrinth
    Output:
        - boolean attesting to whether the rod sits entirely within the frame
    """
    x = rod_array[0]
    y = rod_array[1]
    o = rod_array[2]
    if bool(o): # rod is vertical
        return all([ RADIUS <= y, y < len_y - RADIUS, 0 <= x, x < len_x ])
    else: # rod is horizontal
        return all([ 0 <= y, y < len_y, RADIUS <= x, x < len_x - RADIUS])

def get_xs_ys(rod_array):
    """
    Gives xs and ys list of all positions.
    Input:
        - rod_array: a numpy array containing position of the center and orientation
    Output:
        - xs, ys: two lists of the same length, non-decreasing lists of the x and y
            positions of all nodes of the rod
    """
    x = rod_array[0]
    y = rod_array[1]
    o = rod_array[2]

    l = (2*RADIUS + 1) # the total length of the rod

    # generate all the points to check
    if o: # if rod  is vertical
        ys = [y - RADIUS, y, y + RADIUS]
        xs = l*[x]
    else: # if rod is vertical
        xs = [x - RADIUS, x, x + RADIUS]
        ys = l*[y]
    return xs,ys

def rotate_rod(rod_array):
    """
    This function changes the orientation of the rod from vertical to horizontal
    and viceverse.

    Input:
        - rod_array: an numpy array of 3 integers, center's x and y position, orientation
    Output:
        - the numpy array of the rotated rod
    """

    x = rod_array[0]
    y = rod_array[1]
    o = rod_array[2]
    new_o = (o + 1) % 2

    return create_rod(x,y,new_o)

def shift_rod(rod_array, s, delta = 1):
    """
    This functions displaces the rod by delta units (global constant).
    Displacement is encoded in cardinal directions, north, south, west, east
    Inputs: 
        - rod_array: the numpy array encoding the center's position and orientation
        - s: a character/string, either 'e' (DELTA+1 x), 'w' (-1 x), 'n' (-1 y) or 's' (+1 y)
        - delta (optional): the amount of units to shift
    Outputs:
        - the numpy array encoding the new rod with the shift
    """

    x = rod_array[0]
    y = rod_array[1]
    o = rod_array[2]

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
    return create_rod(x,y,o)


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
 
# FUNCTIONS RELATED TO ROD - LABYRINTH INTERACTION



def point_collision(x,y,lab):
    """
    This function checks whether a point is a solid block of the labyrinth.
    """
    lx,ly = get_shape(lab)
    if not point_in_box(x,y,lx,ly):
        return False # otherwise we cannot test if the point is a block
    return (lab[y][x] == '#') 

def rod_collision(rod_array, lab):
    """
    This function checks whether the given rod sits within
    the labyrinth without colliding with the walls. 
    Inputs:
        - rod_array: a numpy array encoding the rod
        - lab: the list of lists encoding the labyrinth
    Outpus:
        - a boolean, True if there is a collision or exits the box, False otherwise.
    """
    len_x, len_y = get_shape(lab)
    if not sits_in_box(rod_array, len_x, len_y):
        return True

    xs, ys = get_xs_ys(rod_array)
    l = len(xs) # total length of the rod

    for k in range(l):
        if point_collision(xs[k],ys[k],lab):
            return True
    return False

def can_rotate(rod_array, lab, verbose = False):
    """
    This function checks whether there is a L x L box of air
    surrounding the rod within the confines of the box.

    Inputs:
        - rod_array: the numpy array encoding the center of the rod and its position
        - lab: the list of lists encoding the labyrinth
    Output:
        - bool, whether rod can be rotated collisionless within labyrinth
    """
    x,y = rod_array[0], rod_array[1]
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

def print_all(rod_array, lab):
    """
    This function prints the rod in the labyrinth. Rod points are marked with
    'X', and block elements of the labyrinth are marked with '#'.
    It assumes the rod is within the box, but it does not assume that there
    is no collision labyrinth - rod.

    Inputs:
        - rod_array: the numpy array encoding the center of the rod and its position
        - lab: the list of lists encoding the labyrinth
    """
    print_lab = copy.deepcopy(lab)

    len_x, len_y = get_shape(lab)

    if not sits_in_box(rod_array, len_x, len_y):
        raise ValueError("Rod exits the boundary of the box")

    xs, ys = get_xs_ys(rod_array)

    for k in range(len(xs)):
        i, j = xs[k], ys[k]
        if point_collision(i,j,lab):
            print_lab[j][i] = 'C' # represent collision
        else:
            print_lab[ys[k]][xs[k]] = 'X' # represent rod, if it sits within
    for row in print_lab:
        print(row)

    return None

def show_config(rod_array,lab):
    """
    Function that prints a rod configuration in its ambient labyrinth.
    It assumes the rod is within the box, but it does not assume that there
    is no collision labyrinth - rod.
    Inputs:
        - rod_array: the numpy array encoding the center of the rod and its position
        - lab: the list of lists encoding the labyrinth
    """

    print_all(rod_array, lab)
    lx, ly = get_shape(lab)

    print(f"Collision: {rod_collision(rod_array,lab)}")
    print(f"Possible moves: {allowed_moves(rod_array, lab)}")

# FUNCTIONS RELATED TO LABYRINTH EXPLORATION

def allowed_moves(rod_array, lab, delta = 1):
    """
    This function gives the allowed moves for a given configuration of the
    rod and the lab. It checks whether the shifted (defaulte 1 unit of shift)
    rod sits within the labyrinth and does not collide. If it can rotate,
    the test already passes, the function can_rotate( ) already implements
    these tests.

    Inputs:
        - rod_array: the numpy array encoding the center of the rod and its position
        - lab: the list of lists encoding the labyrinth
    Output:
        - a string composed of the possible shifts and moves, 
            encoded as 'e','w','s','n','r'
    """

    len_x, len_y = get_shape(lab)

    moves = ""
    for s in "ewsn":
        possible_rod = shift_rod(rod_array, s)
        if sits_in_box(possible_rod, len_x, len_y) & (not rod_collision(possible_rod, lab)):
            moves = moves + s
    if can_rotate(rod_array, lab):
        moves = moves + "r"
    return moves

# This function will do the heavy lifting

def config_space(lab, verbose = False):
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
                rod = create_rod(x,y,o)
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

    return configurations, count











