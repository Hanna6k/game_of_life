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
        
        print("hiiii")

    def count_neighbours(self):
        for cell in self.alive_cells:
            pos_neigh = []
            pos_corner = [cell.x-1, cell.y-1]
            print("rhis is pos cell", [cell.x, cell.y])
            
            for y in range(3):
                for x in range(3):
                    if pos_corner != [cell.x, cell.y]:
                        pos_neigh.append(pos_corner.copy())
                    pos_corner[0] += 1
                pos_corner[0] -= 3
                pos_corner[1] += 1
            print(pos_neigh)

            for possible_neig in self.alive_cells:
                if [possible_neig.x, possible_neig.y] in pos_neigh:
                    cell.num_alive_neighbours += 1
            print(cell.num_alive_neighbours)

    def die_over_under_pop(self):
        print("funktion die over under pop")

        copy_of_alive_cells = self.alive_cells.copy()
        for cell in copy_of_alive_cells:
            if cell.num_alive_neighbours < 2:
                cell.is_alive = False
                self.alive_cells.remove(cell)
                print("dies underpopulation", [cell.x, cell.y])
            elif cell.num_alive_neighbours > 3:
                cell.is_alive = False
                self.alive_cells.remove(cell)
                print("dies overpopulation", [cell.x, cell.y])
            else:
                print("stays alive", [cell.x, cell.y])

    def update(self):
        for cell in self.alive_cells:
            print(cell.x, cell.y)
            
            cell.check_stay_alive() 



class Cell:
    def __init__(self, x, y, status, stays_alive):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.is_alive = status  # is currently alive
        self.stays_alive = stays_alive  # will still be alive in the next round
        self.num_alive_neighbours = 0

    def check_stay_alive(self):
        # Implement your logic for checking if the cell stays alive here
        # You can access self.is_alive and self.neighbours to make decisions
        
        print("Cell at ({}, {}) is checking if it stays alive.".format(self.x, self.y))

# Create a World instance and call the update method
world = World(start_num_alive=6, visual_x_size=2, visual_y_size=2)
world.create_starting_cells()
world.count_neighbours()
world.die_over_under_pop()
