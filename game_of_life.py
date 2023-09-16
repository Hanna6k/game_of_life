
import random
import numpy as np

# Create a 3x4 array filled with zeros
a = random.randint(0,3)

# my_array = np.zeros((3, 4)) #3 is lentgh y and 4 lenth x
# my_arra = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#print(my_arra[0,1]) this prints number 2

# my_arra = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print(my_arra[0,1])
# my_arra[0,1] = 10
# print(my_arra[0,1])


# for row in my_arra:
#     print(row)
#     for element in row:
#         print(element)

def create_starting_map(x_len,y_len, num_alive): 
    mapp = np.zeros((y_len, x_len))
    placed_ones = 0
    pos_alive = []

    if x_len * y_len < num_alive:
        num_alive = x_len*y_len

    while placed_ones < num_alive:
        x = random.randint(0,x_len-1)
        y = random.randint(0,y_len-1)

        if mapp[y,x] == 0:
            mapp[y,x] = 1
            placed_ones += 1   
            pos_alive.append([y,x])

    return mapp, pos_alive

mappe, position = create_starting_map(7,9, 40)
print(mappe, position)

def live_die(mapp, alive_pos):
    y = mapp.shape[0] #gives lenght y
    x = mapp.shape[1] #gives lengh x
    print(mapp, alive_pos)
    next_mapp = mapp
    still_alive = []

    for element in alive_pos:
        alive_neighbours = 0
        element_top_corner = [element[0]-1, element[1]-1]
        

        for e in range(3):
            for i in range(3):
                if element_top_corner in alive_pos and element_top_corner != element:
                    alive_neighbours += 1
                    #print("yay")
                element_top_corner[1] += 1
            element_top_corner[0] += 1
            element_top_corner[1] -= (x-1)

        print(alive_neighbours,element)

        if alive_neighbours < 2:
            next_mapp[element[0],element[1]] = 0

            print("die")

        if alive_neighbours == 3 or alive_neighbours == 2:
            still_alive.append(element)
            print("stay alive")

        if alive_neighbours > 3:
            next_mapp[element[0],element[1]] = 0
            print("die")

    print(next_mapp, still_alive)

live_die(mappe, position)





# list = [[2, 3], [1, 3], [0, 3], [2, 1], [3, 1]]         

# for element in list:
#     alive_neighbours = 0
#     element_top_corner = [element[0]-1, element[1]-1]
#     for e in range(3):
#         for i in range(3):
#             if element_top_corner in list:
#                 alive_neighbours += 1
#                 print("yay")
#             element_top_corner[1] += 1
#         element_top_corner[0] += 1
#         element_top_corner[1] -= 3

#     if alive_neighbours < 2:
#         print("die")

#     elif alive_neighbours == 3:
#         print("stay alive")
#     elif alive_neighbours > 3:
#         print("die")

            

