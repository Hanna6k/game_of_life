import random
import numpy as np

class World:
    def __init__(self, start_num_alive, visual_x_size, visual_y_size):
        self.alive_cells = []
        self.num_start_alive = 6
        self.start_num_alive = start_num_alive
        self.visual_x_size = visual_x_size
        self.visual_y_size = visual_y_size
        self.all_dead_neighbours = []

    def create_starting_cells(self):        
        pos = []
        while len(self.alive_cells) < self.start_num_alive: #creates exactly number of start_num_alive, all different
            x = random.randint(0, self.visual_x_size)
            y = random.randint(0, self.visual_y_size)
            if [x,y] not in pos:
                cell = Cell(x, y)
                self.alive_cells.append(cell)
                pos.append([x,y])                
        return pos # list is used to create first np.array

    def count_neighbours(self):
        self.all_dead_neighbours = [] #is used to check if dead cells turn alive

        for cell in self.alive_cells:
            pos_neigh = [] # in this list are all positions around the cell
            pos_corner = [cell.x-1, cell.y-1]
            
            for y in range(3):
                for x in range(3):
                    if pos_corner != [cell.x, cell.y]:
                        pos_neigh.append(pos_corner.copy())
                    pos_corner[0] += 1
                pos_corner[0] -= 3
                pos_corner[1] += 1

            num_neighbours = 0
            dead_neighbours = pos_neigh #all elemnts of dead neighbours are appended to the self.all_dead_neighbours
            for possible_neig in self.alive_cells:
                if [possible_neig.x, possible_neig.y] in pos_neigh:
                    dead_neighbours.remove([possible_neig.x, possible_neig.y])
                    num_neighbours += 1
                cell.num_alive_neighbours = num_neighbours
            self.all_dead_neighbours.extend(dead_neighbours) # here the dead neighbours from every cell are appended to self.all_dead_neighbours

    def die_over_under_pop(self):
        copy_of_alive_cells = self.alive_cells.copy()
        for cell in copy_of_alive_cells: #this checks the number of neighbours of every alive cell
            if cell.num_alive_neighbours < 2:
                self.alive_cells.remove(cell)
            elif cell.num_alive_neighbours > 3:
                self.alive_cells.remove(cell)

    def birth_new_cells(self):
        all_new_cells = []
        while len(self.all_dead_neighbours) > 3:
            realiven_cell = self.all_dead_neighbours[0]
            count = self.all_dead_neighbours.count(realiven_cell)
            if count == 3: # if a dead cell appears exactly three times in the list that means it has three alive neighbours since three alive cells have the same dead neighbour 
                new_cell = Cell(realiven_cell[0], realiven_cell[1])
                all_new_cells.append(new_cell)
            while realiven_cell in self.all_dead_neighbours: # this removes the dead cells that have been checked from the self.all_dead_neighbours list
                self.all_dead_neighbours.remove(realiven_cell)
        return all_new_cells # can't be directly appended to self.alive_cells otherwise they could already die before being displayed

    def update(self):        
        self.count_neighbours()
        new_cells = self.birth_new_cells() # needs to be done before die_over_under_pop() otherwise some cells would already be dead
        self.die_over_under_pop()
        self.alive_cells.extend(new_cells) # new born cells are appended after all the living cells are checked

        positions_cell = []
        for cell in self.alive_cells:
            positions_cell.append([cell.x, cell.y])
        return positions_cell # this list contains all the coordinates of all alive cells, will be displayed in an array

class Cell:
    def __init__(self, x, y):
        self.x = x  
        self.y = y  
        self.num_alive_neighbours = 0

# visualisation part

x_visual_size = 4
y_visual_size = 3
number_of_generations = 4

world = World(start_num_alive=6, visual_x_size=x_visual_size, visual_y_size=y_visual_size)
position_of_first_cells = world.create_starting_cells()

mapp = np.empty((y_visual_size + 1, x_visual_size + 1), dtype=str) 
mapp[:] = '0'
mapp_copy_only_zeros = mapp.copy()
for coords in position_of_first_cells: #array of the first values before any cells are checked
    mapp[coords[1],coords[0]] = "x"    
print(f"generation 1:\n{mapp} \n")

for i in range(number_of_generations):
    position_of_next_generation = world.update()
    mapp = mapp_copy_only_zeros.copy()
    for coordinate in position_of_next_generation:
        try: # since the value can be out of the array boundary
            mapp[coordinate[1],coordinate[0]] = "x"
        except:
            pass
    print(f"generation {i + 2}:\n{mapp}\n")

