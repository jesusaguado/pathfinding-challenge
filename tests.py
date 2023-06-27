from functions import *

rod1 = rod([(0,0),(1,0),(2,0)])
rod2 = rod([(0,0),(0,1),(0,2)])
rod99 = rod([(7,0),(8,0),(9,0)])
rod55 = rod([(0,4),(0,5),(0,6)])


rodt = rod1

s = '.........'
s = 9*s
lab_base = str2lab(s)
lab_obs = put_obstacles(lab_base, [(0,0)])
#print(lab_base)

lab = lab_obs

assert check_rod(rodt)
assert check_collision(rodt, lab)
