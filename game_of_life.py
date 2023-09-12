
import random
import numpy as np

# Create a 3x4 array filled with zeros
a = random.randint(0,3)

my_array = np.zeros((3, 4)) #3 is lentgh y and 4 lenth x
my_arra = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#print(my_arra[0,1]) this prints number 2

# my_arra = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print(my_arra[0,1])
# my_arra[0,1] = 10
# print(my_arra[0,1])


# for row in my_arra:
#     print(row)
#     for element in row:
#         print(element)


def create_start_pos(x_len, y_len,num_alive):
    start_pos = []
    for i in range(num_alive):
        x = random.randint(0,x_len-1)
        y = random.randint(0,y_len-1)
        start_pos.append((x,y))
    return start_pos #still need to make sure not same value twice


def create_starting_map(x_len,y_len, num_alive): #start_pos is a list with all pos of num_alive
    mapp = np.zeros((y_len, x_len))
    start_pos = []

    for i in range(num_alive):
        x = random.randint(0,x_len-1)
        y = random.randint(0,y_len-1)
        start_pos.append((x,y))

    for i in range(num_alive):
        #mapp[start_pos[i][0], start_pos[i][1]] = 1
        x = random.randint(0,x_len-1)
        y = random.randint(0,y_len-1)
        mapp[x,y] = 1
        print(x,y)
    return mapp

        


# s = create_start_pos(4,4,7)


mapps = create_starting_map(4, 4, 7)


print(mapps)














