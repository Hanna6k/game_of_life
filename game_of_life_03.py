import random
import numpy as np
import time
import pygame

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
    def __init__(self, world, visual_x_size, visual_y_size, cell_size, menu_size,time_delay, blue, black, gray, green, red, white):
        self.world = world
        self.x_lenght = visual_x_size
        self.y_length = visual_y_size
        self.blue = blue
        self.gray = gray
        self.green = green
        self.red = red
        self.black = black
        self.white = white
        self.size_cell = cell_size
        self.menu_size = menu_size
        self.screen = pygame.display.set_mode((self.x_lenght, self.y_length +self.menu_size))
        self.run = True
        self.time_delay = time_delay
        self.size_enter = 30
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 15) 
        self.again_text = self.font.render("again", self.gray, self.black)
        self.again_text_rect = self.again_text.get_rect()
        self.quit_text = self.font.render("quit", self.gray, self.black)
        self.quit_text_rect = self.again_text.get_rect()
    
    def show(self):
        while self.run:
            pygame.time.delay(self.time_delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False      
                    return False  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check for left mouse button click
                        mouse_x, mouse_y = pygame.mouse.get_pos()  
                        if green_rect.collidepoint(mouse_x, mouse_y): # if clicked on green rect, returns True so while loop isn't broken
                            self.run = False
                            return True     
                        if red_rect.collidepoint(mouse_x, mouse_y):  # if clicked on red rect, returns False so while loop is broken and everything stopps
                            self.run = False
                            return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # if enter is pressed, returns True so while loop isn't broken
                    self.run = False   
                    return True       
            
            self.screen.fill((255,255,255))
            
            for cell in self.world.alive_cells: # draw all alive cells
                pygame.draw.rect(self.screen, self.blue, (cell.x * self.size_cell, cell.y * self.size_cell, self.size_cell, self.size_cell))

            pygame.draw.rect(self.screen, self.gray, (0,self.y_length,self.x_lenght, self.menu_size)) # is menu bellow game 
            green_rect =pygame.draw.rect(self.screen, self.green, (self.x_lenght//3-self.size_enter,self.y_length+self.menu_size//4,2*self.size_enter, self.size_enter)) #button
            red_rect = pygame.draw.rect(self.screen, self.red, (2*(self.x_lenght//3)-self.size_enter,self.y_length+self.menu_size//4,2*self.size_enter, self.size_enter))#button
            
            self.again_text_rect.center = (green_rect.center)
            self.quit_text_rect.center = (red_rect.center)

            for i in range(self.x_lenght//self.size_cell):
                pygame.draw.rect(self.screen, self.white, (i * self.size_cell, 0, 1, self.y_length)) #draws vertical lines
            for i in range(self.y_length//self.size_cell + 1):
                pygame.draw.rect(self.screen, self.white, (0, i * self.size_cell, self.x_lenght,1 ))#draws hrizontal lines

            self.screen.blit(self.again_text, self.again_text_rect) # text --> again--> to reenter coords
            self.screen.blit(self.quit_text, self.quit_text_rect) #text --> quit --> to quit the whole game
            pygame.display.flip()
            self.world.update()
        pygame.quit()

class GetCoords(): # this class allows you to choose your alive cells 
    def __init__(self, x_len, y_len, cell_size, menu_height, list_of_patterns,blue, black, gray, green):
        self.x_len = x_len
        self.y_len = y_len
        self.cell_size = cell_size
        self.pattern_list = list_of_patterns
        self.pos_pattern = 0
        self.patterns_last_object = False
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
        self.font = pygame.font.Font('freesansbold.ttf', 15) 
        self.enter_cords_text = self.font.render("enter Coodinates", self.gray, self.black)
        self.enter_cords_text_rect = self.enter_cords_text.get_rect()

    def get_start_positions(self):
        while self.run:
            self.screen.fill((255,255,255))
            
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    self.run = False
                    return self.positions

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check for left mouse button click
                        mouse_x, mouse_y = pygame.mouse.get_pos()                       
                        x_corner =(mouse_x//self.cell_size)*self.cell_size
                        y_corner = (mouse_y//self.cell_size)*self.cell_size
                        if [x_corner,y_corner] not in self.show_positions: # add the coordintaes of mouse if they arent in the list already
                            self.show_positions.append([x_corner, y_corner])
                            self.positions.append([x_corner/self.cell_size,y_corner/self.cell_size])
                            
                        elif [x_corner,y_corner] in self.show_positions: # if the coordinates are already in the list the are removed
                            self.show_positions.pop(self.show_positions.index([x_corner, y_corner]))
                            self.positions.pop(self.positions.index([x_corner/self.cell_size,y_corner/self.cell_size]))
                            
                        if enter_rect.collidepoint(mouse_x, mouse_y): #if green rect is clicked on --> loop stops and coords are returned
                            self.run = False
                            return self.positions

                        if pattern_rect.collidepoint(mouse_x, mouse_y):
                            if self.pos_pattern-1 >=0 or self.patterns_last_object == True: # is to delete the pattern again if green square is pressed again
                                for i in self.pattern_list[self.pos_pattern-1]:
                                    self.show_positions.pop(self.show_positions.index([i[0]*self.cell_size, i[1]*self.cell_size]))
                                    self.positions.pop(self.positions.index(i))
                            for i in (self.pattern_list[self.pos_pattern]): # is to add the next patern when green square is pressed again
                                self.show_positions.append([i[0]*self.cell_size, i[1]*self.cell_size])
                                self.positions.append(i)
                            if self.pos_pattern == len(self.pattern_list)-1: # to go to next pattern in the list
                                self.pos_pattern = 0 
                                self.patterns_last_object = True
                            else:
                                self.pos_pattern += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # instead of clicking the green button, can alos just press enter
                    self.run = False
                    return self.positions
            
            for i in range(self.x_len//self.cell_size):
                pygame.draw.rect(self.screen, self.black, (i * self.cell_size, 0, 1, self.y_len)) #draws vertical lines
            for i in range(self.y_len//self.cell_size + 1):
                pygame.draw.rect(self.screen, self.black, (0, i * self.cell_size, self.x_len,1 ))#draws hrizontal lines
            for pos in self.show_positions:
                pygame.draw.rect(self.screen, self.blue, (pos[0],pos[1],self.cell_size, self.cell_size))# drwas the cells
            pygame.draw.rect(self.screen, self.gray, (0,self.y_len,self.x_len, self.menu_height)) 
            enter_rect =pygame.draw.rect(self.screen, self.green, (self.x_len//2-self.size_enter * 2.5,self.y_len+self.menu_height//4,5*self.size_enter, self.size_enter))# green box to enter the values of alive cells
            self.enter_cords_text_rect.center = enter_rect.center
            self.screen.blit(self.enter_cords_text, self.enter_cords_text_rect)
            pattern_rect =pygame.draw.rect(self.screen, self.green, (self.x_len//5,self.y_len+self.menu_height//4,2*self.cell_size, 2*self.cell_size))# green box to iterate through pattern list

            pygame.display.flip()
        pygame.quit()

# visualisation part
MENU_HEIGHT = 100
X_VISUAL_SIZE = 600
Y_VISUAL_SIZE = 450
TIME_FOR_NEW_GEN =150 
CELL_SIZE = 15
BLUE = (0,0,255)
BLACK = (15,15,15)
GRAY= (200,200,200)
GREEN = (0,128,0)
RED = (168,0,0)
WHITE = (255,255,255)

# coordinates of certain patterns which can be chosen 
nice_pattern = [[11.0, 10.0], [11.0, 9.0], [12.0, 9.0], [13.0, 9.0], [13.0, 10.0], [13.0, 11.0], [11.0, 11.0], [11.0, 14.0], [11.0, 13.0], [13.0, 13.0], [13.0, 14.0], [13.0, 15.0], [12.0, 15.0], [11.0, 15.0], [23.0, 32.0]]
glider = [[4.0, 2.0], [5.0, 2.0], [6.0, 2.0], [6.0, 1.0], [5.0, 0.0], [14.0, 2.0], [15.0, 3.0], [15.0, 4.0], [14.0, 4.0], [13.0, 4.0], [5.0, 11.0], [6.0, 12.0], [6.0, 13.0], [4.0, 13.0], [5.0, 13.0], [0.0, 19.0], [1.0, 19.0], [1.0, 17.0], [2.0, 19.0], [2.0, 18.0], [13.0, 8.0], [14.0, 9.0], [14.0, 10.0], [13.0, 10.0], [12.0, 10.0], [11.0, 14.0], [12.0, 15.0], [12.0, 16.0], [11.0, 16.0], [10.0, 16.0], [6.0, 20.0], [7.0, 22.0], [6.0, 22.0], [5.0, 22.0], [7.0, 21.0], [23.0, 1.0], [24.0, 2.0], [24.0, 3.0], [23.0, 3.0], [22.0, 3.0], [22.0, 6.0], [23.0, 7.0], [23.0, 8.0], [22.0, 8.0], [21.0, 8.0], [18.0, 32.0]]
birds = [[1.0, 17.0], [1.0, 15.0], [2.0, 14.0], [4.0, 17.0], [5.0, 16.0], [5.0, 15.0], [5.0, 14.0], [4.0, 14.0], [3.0, 14.0], [8.0, 15.0], [8.0, 17.0], [9.0, 14.0], [10.0, 18.0], [12.0, 17.0], [13.0, 16.0], [13.0, 15.0], [13.0, 14.0], [10.0, 14.0], [11.0, 14.0], [12.0, 14.0], [16.0, 15.0], [17.0, 14.0], [16.0, 17.0], [18.0, 18.0], [19.0, 18.0], [21.0, 17.0], [22.0, 16.0], [22.0, 15.0], [22.0, 14.0], [18.0, 14.0], [19.0, 14.0], [20.0, 14.0], [21.0, 14.0], [13.0, 32.0]]
block = [[12.0, 10.0], [13.0, 10.0], [14.0, 10.0], [15.0, 10.0], [15.0, 11.0], [14.0, 11.0], [12.0, 11.0], [13.0, 11.0], [12.0, 12.0], [13.0, 12.0], [14.0, 12.0], [15.0, 12.0], [16.0, 10.0], [16.0, 11.0], [16.0, 12.0], [13.0, 13.0], [12.0, 13.0], [14.0, 13.0], [16.0, 13.0], [15.0, 13.0], [16.0, 14.0], [15.0, 14.0], [14.0, 14.0], [13.0, 14.0], [12.0, 14.0], [22.0, 32.0]]
four_squares = [[13.0, 13.0], [14.0, 12.0], [14.0, 11.0], [14.0, 10.0], [12.0, 13.0], [11.0, 13.0], [13.0, 15.0], [12.0, 15.0], [11.0, 15.0], [14.0, 16.0], [14.0, 17.0], [14.0, 18.0], [16.0, 16.0], [16.0, 18.0], [16.0, 17.0], [18.0, 15.0], [17.0, 15.0], [19.0, 15.0], [16.0, 12.0], [16.0, 11.0], [16.0, 10.0], [17.0, 13.0], [18.0, 13.0], [19.0, 13.0], [13.0, 20.0], [12.0, 20.0], [11.0, 20.0], [9.0, 16.0], [9.0, 18.0], [9.0, 17.0], [17.0, 20.0], [19.0, 20.0], [18.0, 20.0], [21.0, 16.0], [21.0, 17.0], [21.0, 18.0], [9.0, 12.0], [9.0, 10.0], [9.0, 11.0], [11.0, 8.0], [12.0, 8.0], [13.0, 8.0], [17.0, 8.0], [18.0, 8.0], [19.0, 8.0], [21.0, 12.0], [21.0, 11.0], [21.0, 10.0], [16.0, 32.0]]
space_ship = [[12.0, 8.0], [13.0, 7.0], [13.0, 8.0], [14.0, 7.0], [12.0, 10.0], [13.0, 10.0], [13.0, 11.0], [14.0, 11.0], [15.0, 8.0], [15.0, 9.0], [15.0, 10.0], [16.0, 9.0], [20.0, 32.0]]
static = [[3.0, 4.0], [4.0, 4.0], [4.0, 3.0], [3.0, 3.0], [7.0, 9.0], [6.0, 10.0], [6.0, 11.0], [7.0, 12.0], [8.0, 11.0], [8.0, 10.0], [15.0, 5.0], [16.0, 6.0], [17.0, 4.0], [16.0, 4.0], [17.0, 5.0], [15.0, 21.0], [15.0, 23.0], [14.0, 22.0], [16.0, 22.0], [25.0, 18.0], [26.0, 19.0], [26.0, 17.0], [27.0, 16.0], [28.0, 17.0], [27.0, 18.0], [29.0, 7.0], [29.0, 6.0], [30.0, 6.0], [31.0, 7.0], [31.0, 8.0], [31.0, 9.0], [32.0, 9.0], [15.0, 14.0], [16.0, 13.0], [17.0, 12.0], [16.0, 15.0], [17.0, 15.0], [18.0, 13.0], [18.0, 14.0], [17.0, 32.0]]
crosses = [[4.0, 2.0], [4.0, 4.0], [3.0, 3.0], [5.0, 3.0], [4.0, 3.0], [14.0, 2.0], [14.0, 3.0], [14.0, 4.0], [13.0, 3.0], [15.0, 3.0], [23.0, 3.0], [24.0, 2.0], [24.0, 3.0], [24.0, 4.0], [25.0, 3.0], [33.0, 3.0], [34.0, 3.0], [34.0, 2.0], [35.0, 3.0], [34.0, 4.0], [9.0, 9.0], [9.0, 10.0], [9.0, 11.0], [8.0, 10.0], [10.0, 10.0], [20.0, 11.0], [20.0, 10.0], [20.0, 9.0], [19.0, 10.0], [21.0, 10.0], [29.0, 9.0], [29.0, 10.0], [28.0, 10.0], [29.0, 11.0], [30.0, 10.0], [4.0, 16.0], [4.0, 17.0], [4.0, 18.0], [3.0, 17.0], [5.0, 17.0], [14.0, 16.0], [14.0, 18.0], [15.0, 17.0], [14.0, 17.0], [13.0, 17.0], [24.0, 16.0], [24.0, 17.0], [23.0, 17.0], [24.0, 18.0], [25.0, 17.0], [34.0, 16.0], [34.0, 18.0], [35.0, 17.0], [34.0, 17.0], [33.0, 17.0], [9.0, 23.0], [9.0, 24.0], [9.0, 25.0], [8.0, 24.0], [10.0, 24.0], [20.0, 23.0], [20.0, 24.0], [20.0, 25.0], [21.0, 24.0], [19.0, 24.0], [29.0, 23.0], [29.0, 24.0], [29.0, 25.0], [28.0, 24.0], [30.0, 24.0], [22.0, 32.0]]
oszillating =[[2.0, 3.0], [4.0, 3.0], [3.0, 3.0], [8.0, 12.0], [9.0, 11.0], [9.0, 10.0], [10.0, 12.0], [10.0, 13.0], [11.0, 11.0], [16.0, 5.0], [16.0, 4.0], [16.0, 3.0], [17.0, 4.0], [17.0, 5.0], [17.0, 6.0], [3.0, 21.0], [3.0, 20.0], [4.0, 20.0], [4.0, 21.0], [6.0, 23.0], [5.0, 23.0], [6.0, 22.0], [5.0, 22.0], [26.0, 2.0], [27.0, 2.0], [28.0, 2.0], [28.0, 3.0], [28.0, 4.0], [26.0, 3.0], [26.0, 4.0], [27.0, 4.0], [29.0, 2.0], [29.0, 3.0], [29.0, 4.0], [30.0, 4.0], [31.0, 4.0], [32.0, 4.0], [32.0, 3.0], [32.0, 2.0], [30.0, 2.0], [31.0, 2.0], [30.0, 3.0], [27.0, 21.0], [27.0, 22.0], [27.0, 23.0], [28.0, 24.0], [29.0, 24.0], [30.0, 24.0], [31.0, 24.0], [28.0, 21.0], [28.0, 22.0], [27.0, 20.0], [29.0, 23.0], [30.0, 23.0], [28.0, 19.0], [29.0, 19.0], [30.0, 19.0], [30.0, 20.0], [29.0, 20.0], [31.0, 19.0], [32.0, 20.0], [31.0, 21.0], [32.0, 21.0], [31.0, 22.0], [32.0, 22.0], [32.0, 23.0], [22.0, 32.0], [12.0, 20.0], [12.0, 21.0], [13.0, 21.0], [13.0, 22.0], [13.0, 23.0], [15.0, 21.0], [15.0, 22.0], [15.0, 23.0], [16.0, 21.0], [16.0, 20.0], [12.0, 24.0], [12.0, 25.0], [11.0, 24.0], [11.0, 23.0], [16.0, 24.0], [16.0, 25.0], [17.0, 24.0], [17.0, 23.0], [18.0, 11.0], [18.0, 12.0], [19.0, 11.0], [20.0, 12.0], [20.0, 14.0], [21.0, 15.0], [22.0, 15.0], [22.0, 14.0], [17.0, 32.0]]

pattern_list = []
pattern_list.extend([nice_pattern])
pattern_list.extend([static])
pattern_list.extend([crosses])
pattern_list.extend([oszillating])
pattern_list.extend([birds])
pattern_list.extend([block])
pattern_list.extend([four_squares])
pattern_list.extend([space_ship])
pattern_list.extend([glider])

run = True
if __name__ == "__main__":
    while run:
        get_coords = GetCoords(X_VISUAL_SIZE, Y_VISUAL_SIZE, CELL_SIZE, MENU_HEIGHT,pattern_list, BLUE, BLACK, GRAY, GREEN)
        coords = get_coords.get_start_positions()
        #print(coords)
        world = World(start_num_alive=6, random_x_range=X_VISUAL_SIZE, random_y_range=Y_VISUAL_SIZE, start_pos=coords)
        world.create_starting_cells()
        mapp = View(world, X_VISUAL_SIZE, Y_VISUAL_SIZE, CELL_SIZE, MENU_HEIGHT,TIME_FOR_NEW_GEN,BLUE, BLACK, GRAY, GREEN, RED, WHITE)
        continu = mapp.show()
        run = continu