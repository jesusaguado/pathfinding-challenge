from functions import *

init_rod = create_rod(1,0,0)

rod1 = create_rod(0,1,1)
rod2 = create_rod(0,1,1)
rod99 = create_rod(8,0,1)
rod55 = create_rod(0,5,0)


s = '.........'
s = 5*s
lab_base = str2lab(s)
lab_obs = put_obstacles(lab_base, [(0,0)])
#print(lab_base)

lab = lab_base


#if can_rotate(rodt,lab):
#    rodt = rotate_rod(rodt)

rod = init_rod

rod = shift_rod(rod,'s')
rod = shift_rod(rod,'e')
rod = rotate_rod(rod)

lx, ly = get_shape(lab)
#assert sits_in_box(rod, lx, ly)

lab = put_obstacles(lab, [(1,1)])
lab = [list("..."),list("..."),list("...")]




print("PRINTING LABYRINTH")
for row in lab:
    print(row)

#show_config(init_rod,lab)


configs, count = config_space(lab)


input()
print("PRINTING ALL VIABLE CONFIGURATIONS")
for c in configs:
    print(c)
    show_config(c,lab)
    input()

