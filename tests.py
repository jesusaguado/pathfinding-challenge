from functions import *

# ASSET GENERATION

init_rod = (1,0,0) #sits_in_box, cannot rotate, moves 'es'
rod1 = (0,1,1) # sits_in_box, cannot rotate, moves 'es'
rod2 = (1,1,0) # sits_in_box, can rotate, moves 'esnr'
rod99 = (8,0,1) # does not fit in box
rod55 = (0,5,0) # does not fit in box
rod88 = (8,3,1) # sits_in_box, cannot rotate, moves 'wn'
rod44 = (7,4,0) # sits_in_box, cannot rotate, moves 'wn'


# Basic labyrinth with no obstacles
s = '.........'
s = 5*s
lab_base = str2lab(s)


# Labytinth with obstructed origin
lab_origin_obs = put_obstacles(lab_base, [(0,0)])
lab_target_obs = put_obstacles(lab_base, [(8,4)])

lx,ly = get_shape(lab_base)

# BASIC TESTS
assert sits_in_box(init_rod,lx,ly)
assert not can_rotate(init_rod,lab_base)
assert allowed_moves(init_rod,lab_base)=='es'
assert sits_in_box(rod1,lx,ly)
assert not can_rotate(rod1,lab_base)
assert allowed_moves(rod1,lab_base)=='es'
assert sits_in_box(rod2,lx,ly)
assert can_rotate(rod2,lab_base)
assert allowed_moves(rod2,lab_base)=='esnr'
assert not sits_in_box(rod99,lx,ly)
assert not sits_in_box(rod55,lx,ly)
assert sits_in_box(rod88,lx,ly)
assert not can_rotate(rod88,lab_base)
assert allowed_moves(rod88,lab_base)=='wn'
assert sits_in_box(rod44,lx,ly)
assert not can_rotate(rod44,lab_base)
assert allowed_moves(rod44,lab_base)=='wn'
assert rod_collision(init_rod,lab_origin_obs)
assert rod_collision(rod1,lab_origin_obs)
assert rod_collision(rod88,lab_target_obs)
assert rod_collision(rod44,lab_target_obs)

# testing the "touches_target" function
rod = (0,0,0)
assert touches_target(rod,1,0)
assert touches_target(rod,0,0)
assert touches_target(rod,-1,0)

# testing the generation of configurations
configs, count = config_space(lab_base, count_states = True)
assert count == 62


lab_simple = [list("..."),list("..."),list("...")]
configs, count = config_space(lab_simple, count_states = True)
assert count == 6


# TESTING GROUND


# TESTING THE UPPER BOUND

#def random_lab(fill = 0.2):
#    new_lab = copy.deepcopy(lab_base)
#    for i in range(9):
#        for j in range(5):
#            if random.random() <= fill:
#                new_lab[j][i] = '#'
#    return new_lab

# In each execution this generates a random lab filled
# with a random fraction and checks the upper bound
random_fill = random.random()
gen_lab = random_lab(fill = random_fill)
configs, count = config_space(gen_lab, count_states = True)
#print(f"Random labyrinth with {100*random_fill:.2f} % fill. Count: {count}")
#print_all(init_rod, gen_lab, omit_rod = True)
assert count < lx*ly*2

    
# testing the return_neighbors functionality of allowed_moves

assert allowed_moves(init_rod, lab_base, give_neighbors = True) == [(2,0,0),(1,1,0)]


def generate_simple_lab(n):
    generated_lab = [list(n*['.']) for i in range(n)]
    return generated_lab


# automated tests for finding the solution in simple labyrinth

for k in range(3,30):
    temp_lab = generate_simple_lab(k)
    assert solution(generate_simple_lab(k)) == 2*(k-2)
    del temp_lab

