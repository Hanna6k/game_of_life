
import random
import numpy as np
import time

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



def live_die_born(mapp, alive_pos):
    y = mapp.shape[0] #gives lenght y
    x = mapp.shape[1] #gives lengh x

    next_map = mapp
    still_alive = []
    chance_realiven = []

    for element in alive_pos:
        alive_neighbours = 0
        element_top_corner = [element[0]-1, element[1]-1]
        

        for e in range(3):
            for i in range(3):
                
                if element_top_corner in alive_pos and element_top_corner != element:
                    alive_neighbours += 1

                if element_top_corner not in alive_pos: #and 0<=element_top_corner[0]<=(y-1) and 0<=element_top_corner[1]<=(x-1):
                    if element_top_corner[0] >= 0 and element_top_corner[1] >= 0:
                        if element_top_corner[0] < y and element_top_corner[1] <x:       
                            test = element_top_corner.copy()
                            chance_realiven.append(test)

                element_top_corner[1] += 1

            element_top_corner[0] += 1
            element_top_corner[1] -= (x-1)

        if alive_neighbours < 2:
            next_map[element[0],element[1]] = 0

        if alive_neighbours == 3 or alive_neighbours == 2:
            still_alive.append(element)

        if alive_neighbours > 3:
            next_map[element[0],element[1]] = 0

    for element in chance_realiven:
        count = chance_realiven.count(element)
        if count ==3 and next_map[element[0], element[1]] == 0:
            still_alive.append(element)
            next_map[element[0],element[1]] = 1
    
    return next_map, still_alive


start_map, position = create_starting_map(5,7, 20)
run = True
print("first generation:")
print(start_map)

while run:
    next_gen, alive_coord = live_die_born(start_map, position)

    start_map = next_gen
    position = alive_coord
    print("next generation:")
    print(start_map)
    time.sleep(5)


            

