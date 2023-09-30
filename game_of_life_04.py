import random
import numpy as np
import time
import pygame
# pygame.init()
pygame.font.init()




class World:
    def __init__(self, start_num_alive, random_x_range, random_y_range, start_pos):
        self.alive_cells = []
        self.num_start_alive = 6
        self.start_num_alive = start_num_alive
        self.visual_x_size = random_x_range
        self.visual_y_size = random_y_range
        self.all_dead_neighbours = []
        self.starting_pos = start_pos

    def create_starting_cells(self):   
        pos = []
        if len(self.starting_pos) == 0:     
            while len(self.alive_cells) < self.start_num_alive: #creates exactly number of start_num_alive, all different
                x = random.randint(0, self.visual_x_size)
                y = random.randint(0, self.visual_y_size)
                if [x,y] not in pos:
                    cell = Cell(x, y)
                    self.alive_cells.append(cell)     
                    pos.append([x,y])         
        else:
            for elemnt in self.starting_pos:
                celll = Cell(elemnt[0], elemnt[1])
                self.alive_cells.append(celll)

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

        self.all_dead_neighbours = []
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

class View:
    def __init__(self, world, visual_x_size, visual_y_size, cell_size, menu_size, blue, black, gray, green, red):
        self.world = world
        self.x_lenght = visual_x_size
        self.y_length = visual_y_size
        self.blue = blue
        self.gray = gray
        self.green = green
        self.red = red
        self.black = black
        self.size_cell = cell_size
        self.menu_size = menu_size
        self.screen = pygame.display.set_mode((self.x_lenght, self.y_length +self.menu_size))
        self.run = True
        self.time_delay = 80
        self.size_enter = 30
        pygame.font.init()
        print( pygame.font.get_init(), "second time")
        self.font = pygame.font.Font('freesansbold.ttf', 15) 
        self.again_text = self.font.render("again", self.gray, self.black)
        self.again_text_rect = self.again_text.get_rect()
        # self.again_text_rect.topleft = (self.x_lenght//3-self.size_enter,self.y_length+self.menu_size//3)

        self.quit_text = self.font.render("quit", self.gray, self.black)
        self.quit_text_rect = self.again_text.get_rect()
        # self.quit_text_rect.topleft = (2*(self.x_lenght//3-self.size_enter),self.y_length+self.menu_size//3)



    
    def show(self):
        while self.run:
            pygame.time.delay(self.time_delay)
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    self.run = False      
                    return False  


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check for left mouse button click
                        mouse_x, mouse_y = pygame.mouse.get_pos()  
                        if green_rect.collidepoint(mouse_x, mouse_y):
                            print("clicked on green") 
                            self.run = False
                            return True     

                        if red_rect.collidepoint(mouse_x, mouse_y):
                            print("clicked on red")   
                            self.run = False
                            return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.run = False   
                    return True       

            
            self.screen.fill((255,255,255))
            
            for cell in self.world.alive_cells:
                pygame.draw.rect(self.screen, self.blue, (cell.x * self.size_cell, cell.y * self.size_cell, self.size_cell, self.size_cell))
            pygame.draw.rect(self.screen, self.gray, (0,self.y_length,self.x_lenght, self.menu_size))
            green_rect =pygame.draw.rect(self.screen, self.green, (self.x_lenght//3-self.size_enter,self.y_length+self.menu_size//4,2*self.size_enter, self.size_enter))
            red_rect = pygame.draw.rect(self.screen, self.red, (2*(self.x_lenght//3)-self.size_enter,self.y_length+self.menu_size//4,2*self.size_enter, self.size_enter))
            
            self.again_text_rect.center = (green_rect.center)
            self.quit_text_rect.center = (red_rect.center)

            self.screen.blit(self.again_text, self.again_text_rect)
            self.screen.blit(self.quit_text, self.quit_text_rect)
            pygame.display.flip()

            self.world.update()
        pygame.quit()

class Get_coords():
    def __init__(self, x_len, y_len, cell_size, menu_height, blue, black, gray, green):
        #pygame.font.init
        #pygame.init()
        self.x_len = x_len
        self.y_len = y_len
        self.cell_size = cell_size
        self.blue = blue
        self.black = black
        self.gray = gray
        self.green = green
        self.run = True
        self.show_positions  = []
        self.positions = []
        self.menu_height = menu_height
        self.screen = pygame.display.set_mode((self.x_len, self.y_len+self.menu_height))
        self.size_enter = 30
        pygame.font.init()
        print( pygame.font.get_init(), "first time")
        self.font = pygame.font.Font('freesansbold.ttf', 15) 
        self.enter_cords_text = self.font.render("enter Coodinates", self.gray, self.black)
        self.enter_cords_text_rect = self.enter_cords_text.get_rect()
        #self.enter_cords_text_rect.topleft = (self.x_len//2-self.size_enter,self.y_len+self.menu_height//4)

    def get_start_positions(self):
        while self.run:
            self.screen.fill((255,255,255))
            
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check for left mouse button click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        #print(f"Mouse Clicked at Position: ({mouse_x}, {mouse_y})")
                        x_corner =(mouse_x//self.cell_size)*self.cell_size
                        y_corner = (mouse_y//self.cell_size)*self.cell_size
                        if [x_corner,y_corner] not in self.show_positions:
                            self.show_positions.append([x_corner, y_corner])
                            self.positions.append([x_corner/self.cell_size,y_corner/self.cell_size])
                            #print(self.show_positions)
                        elif [x_corner,y_corner] in self.show_positions:
                            self.show_positions.pop(self.show_positions.index([x_corner, y_corner]))
                            self.positions.pop(self.positions.index([x_corner/self.cell_size,y_corner/self.cell_size]))
                            #print(self.show_positions)

                        if enter_rect.collidepoint(mouse_x, mouse_y): 
                            self.run = False
                            
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.run = False
            
            for i in range(self.x_len//self.cell_size):
                pygame.draw.rect(self.screen, self.black, (i * self.cell_size, 0, 1, self.y_len))
            for i in range(self.y_len//self.cell_size + 1):
                pygame.draw.rect(self.screen, self.black, (0, i * self.cell_size, self.x_len,1 ))
            for pos in self.show_positions:
                pygame.draw.rect(self.screen, self.blue, (pos[0],pos[1],self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, self.gray, (0,self.y_len,self.x_len, self.menu_height))
            enter_rect =pygame.draw.rect(self.screen, self.green, (self.x_len//2-self.size_enter * 2.5,self.y_len+self.menu_height//4,5*self.size_enter, self.size_enter))
            self.enter_cords_text_rect.center = enter_rect.center
            self.screen.blit(self.enter_cords_text, self.enter_cords_text_rect)
            pygame.display.flip()
        pygame.quit()

        return self.positions

# visualisation part
MENU_HEIGHT = 100
X_VISUAL_SIZE = 400
Y_VISUAL_SIZE = 450
# NUMBER_OF_GENERATIONS = 8
# TIME_FOR_NEW_GEN = 3
CELL_SIZE = 15
BLUE = (0,0,255)
BLACK = (15,15,15)
GRAY= (200,200,200)
GREEN = (0,128,0)
RED = (168,0,0)


starting_poitions = [[-1,-1], [0,-1], [-1,0]]
nice_pattern = [[10,10],[11,10],[12,10], [10,11],[10,12],[12,11], [12,12], [10,14], [10,15], [10,16], [11,16], [12,16],[12,15], [12,14]]
glider = [[1,0], [2,0], [0,1], [1,1],[1,2]]
switcher = [[4,0], [4,1],[4,2], [4,6],[4,7], [4,8], [0,4], [1,4], [2,4], [6,4], [7,4], [8,4]]
star = [[4,3], [4,4], [4,5], [3,4], [5,4]]

run = True

if __name__ == "__main__":

    while run:

        get_coords = Get_coords(X_VISUAL_SIZE, Y_VISUAL_SIZE, CELL_SIZE, MENU_HEIGHT, BLUE, BLACK, GRAY, GREEN)
        coords = get_coords.get_start_positions()

        world = World(start_num_alive=6, random_x_range=X_VISUAL_SIZE, random_y_range=Y_VISUAL_SIZE, start_pos=coords)
        world.create_starting_cells()
        mapp = View(world, X_VISUAL_SIZE, Y_VISUAL_SIZE, CELL_SIZE, MENU_HEIGHT,BLUE, BLACK, GRAY, GREEN, RED)
        continu = mapp.show()
        run = continu