import random
import numpy as np
import time

class World:
    def __init__(self, start_num_alive, visual_x_size, visual_y_size):
        self.run = True
        self.alive_cells = [] #is kinof the wolrd
        self.dead_neighbours = []
        self.num_start_alive = 6
        self.start_num_alive = start_num_alive
        self.visual_x_size = visual_x_size
        self.visual_y_size = visual_y_size

        # Create cell instances and add them to the world

    def create_starting_cells(self):
        
        pos = []
        while len(self.alive_cells) < self.start_num_alive:
            x = random.randint(0, self.visual_x_size)
            y = random.randint(0, self.visual_y_size)
            if [x,y] not in pos:
                cell = Cell(x, y, True, True)
                self.alive_cells.append(cell)
                pos.append([x,y])        
        
        return pos

    def count_neighbours(self):
        for cell in self.alive_cells:
            pos_neigh = []
            pos_corner = [cell.x-1, cell.y-1]
            # print("rhis is pos cell", [cell.x, cell.y])
            
            for y in range(3):
                for x in range(3):
                    if pos_corner != [cell.x, cell.y]:
                        pos_neigh.append(pos_corner.copy())
                    pos_corner[0] += 1
                pos_corner[0] -= 3
                pos_corner[1] += 1
            # print(pos_neigh)

            num_neighbours = 0
            for possible_neig in self.alive_cells:
                #num_neighbours = 0
                if [possible_neig.x, possible_neig.y] in pos_neigh:
                    #cell.num_alive_neighbours += 1
                    num_neighbours += 1

                cell.num_alive_neighbours = num_neighbours
            # print(cell.num_alive_neighbours)

    def die_over_under_pop(self):
        print("funktion die over under pop", "num_alive before:", len(self.alive_cells))

        copy_of_alive_cells = self.alive_cells.copy()
        for cell in copy_of_alive_cells:
            if cell.num_alive_neighbours < 2:
                cell.is_alive = False
                self.alive_cells.remove(cell)
                # print("dies underpopulation", [cell.x, cell.y])
            elif cell.num_alive_neighbours > 3:
                cell.is_alive = False
                self.alive_cells.remove(cell)
            #     print("dies overpopulation", [cell.x, cell.y])
            # else:
            #     print("stays alive", [cell.x, cell.y])

        print("num_alive after:", len(self.alive_cells))

    def update(self):
        
        self.count_neighbours()
        self.die_over_under_pop()

        positions_cell = []
        for cell in self.alive_cells:
            positions_cell.append([cell.x, cell.y])
        return positions_cell



class Cell:
    def __init__(self, x, y, status, stays_alive):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.is_alive = status  # is currently alive
        self.stays_alive = stays_alive  # will still be alive in the next round
        self.num_alive_neighbours = 0




# Create a World instance and call the update method

x_visual_size = 2
y_visual_size = 2

number_of_generations = 4

world = World(start_num_alive=6, visual_x_size=x_visual_size, visual_y_size=y_visual_size)
position_of_first_cells = world.create_starting_cells()
print("birth cells",position_of_first_cells)

# position_of_next_generation = world.update()
# print("second cells", position_of_next_generation)

# position_of_next_generation = world.update()
# print("third cells", position_of_next_generation)
mapp = np.empty((y_visual_size + 1, x_visual_size + 1), dtype=str)
mapp[:] = '0'
mapp_copy_only_zeros = mapp.copy()
for coords in position_of_first_cells:
    mapp[coords[1],coords[0]] = "x"    
print(mapp)

for i in range(number_of_generations):
    position_of_next_generation = world.update()

    print("second cells", position_of_next_generation)
    mapp = mapp_copy_only_zeros.copy()
    for coor in position_of_next_generation:
        mapp[coor[1],coor[0]] = "x"
    print(mapp)

# mapp = np.empty((y_visual_size + 1, x_visual_size + 1), dtype=str)
# mapp[:] = '0'

# for coords in position_of_first_cells:
#     mapp[coords[1],coords[0]] = "x"
#     # print(coords[0])

# print(mapp)

# position_of_next_generation = world.update()
# print("second cells", position_of_next_generation)

# print("third cells", position_of_next_generation)

# while len(world.alive_cells) >= 0:
#     new_cells = world.update()
#     for coords in new_cells:
#         mapp[coords[1],coords[0]] = "x"
#     print(mapp)
