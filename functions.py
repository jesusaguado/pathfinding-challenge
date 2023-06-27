import numpy as np

def rod(list_of_tuples):
    """
    This function creates a rod from a list of positions
    and encodes it in a numpy array. 

    Why numpy array: they are mutable and I am easily able
    to move them in the grid because of this, without
    having memory issues.

    Inputs:
        - list of tuples: a list of at least 2 tuples of dimension 2
    Outputs:
        - a numpy array containing the 2 x n positions
    """

    n = len(list_of_tuples)

    if n < 2:
        raise ValueError("Rod needs to have more at least 2 nodes")

    for tup in list_of_tuples:
        if len(tup)!=2:
            raise ValueError("Some tuple is not 2-dimensional")

    #return np.array(list_of_tuples).reshape(2,n)
    xs = [i for i,j in list_of_tuples]
    ys = [j for i,j in list_of_tuples]
    return np.array([xs,ys])

def sits_in_box(rod_array):
    xs = rod_array[0,:]
    ys = rod_array[1,:]

    if not all(xs >= 0) & all(xs <= 8) & all(ys >= 0) & all(ys <= 4):
        print("Box test did not pass")
        return False
    return True


def check_rod(rod_array):
    """
    This function checks that the rod_array provided is
    valid: it is rigid, and it fits within the 5 x 9 box.

    Inputs:
        - rod_array: a numpy array assumed to be of shape 2 x n
    Outputs:
        - check: a boolean that records if it is a valid rod.
    """

    m = rod_array.shape[1] # the length of the rod
    #print(rod_array)

    # check that the array fits in the box
    xs = rod_array[0,:]
    #print(xs)
    ys = rod_array[1,:]
    #print(ys)

    if not sits_in_box(rod_array):
        return False

    # check that the array increases in one and only one direction
    if xs[0] == xs[1]:
        #print("First x's equal")
        # check that xs is constant and ys increases by 1
        if not all((xs - xs[0]) == 0):
            print("X should be constant and it isn't")
            return False
        for k in range(1,m-1):
            if not ys[k+1] == (ys[k] + 1):
                return False

    elif ys[0] == ys[1]:
        #print("First y's equal")
        # check that ys is constant and xs increases by 1
        if not all((ys - ys[0]) == 0):
            print("Y should be constant and it isn't")
            return False
        for k in range(1,m-1):
            if not xs[k+1] == (xs[k] + 1):
                return False

    return True

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

import copy
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
        new_lab[i][j]='#'
    return new_lab
 

def check_collision(rod, lab):
    """
    This function checks whether the given rod sits within
    the labyrinth without colliding with the walls. It
    """
    if not sits_in_box(rod):
        #print('Rod does not sit in box')
        return True
    m = rod.shape[1]
    for k in range(0,m):
        i,j = rod[:,k] # extract x,y components of k-th node
        if lab[i][j] == '#':
            #print(f"Collision at {i,j}")
            return True

    return False
