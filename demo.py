from functions import *

print("This script showcases the programmed functions to solve the problem")

print("#####################")
print("FIRST EXAMPLE: ")
print("#####################")

init_rod = (1,0,0)
print(" > Starting configuration:")
lab01 = str2lab(".........#...#........#.....#.....#..#.....#.")
print_all(init_rod,lab01)
print(f"> Number of required steps: {solution(lab01)}")

input("> Press any key to execute animation of found path.")


print("#####################")
print("SECOND EXAMPLE: ")
print("#####################")
input("Press any key to continue")
lab02 = str2lab(".........#...#..#.....#.....#.....#..#.....#.")
print_all(init_rod,lab02)
print(f"Number of required steps: {solution(lab02)}")
show_me_trajectory(lab02)
