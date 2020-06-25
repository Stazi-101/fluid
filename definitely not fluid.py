import numpy as np
import pygame
import cv2
from scipy import ndimage
import my_interpolate


SCREEN_SIZE = (500,500)
SCALE = 10
GRID_SIZE = (SCREEN_SIZE[0]//SCALE,SCREEN_SIZE[1]//SCALE)
INTERPOLATE = my_interpolate.stolen

PUSH_MULT = 0.0005
MOVE_MULT = .03
DRAG = 0.9


class Tank():

    def __init__(self, surface, scale):

        self.surface = surface
        self.scale = scale

        self.grid_size = (surface.get_width()//scale,
                          surface.get_height()//scale)

        self.density = np.zeros( self.grid_size )
        self.vel_x   = np.zeros( self.grid_size )
        self.vel_y   = np.zeros( self.grid_size ) #, dtype='uint16' )


    def left_click(self, screen_pos):
        x,y = screen_pos
        x,y = x//self.scale, y//self.scale
        self.density[x-1:x+1,y-1:y+1] += 100

    def right_click(self, screen_pos):
        x,y = screen_pos
        x,y = x//self.scale, y//self.scale
        self.density[x-1:x+1,y-1:y+1] -= 100


    def tick(self):

        def push_dense(self):
            sobel_x = ndimage.sobel( self.density, axis=0 )
            sobel_y = ndimage.sobel( self.density, axis=1 )

            self.vel_x += sobel_x*PUSH_MULT
            self.vel_y += sobel_y*PUSH_MULT

        def move(self):

            for x in range(self.grid_size[0]):
                for y in range(self.grid_size[1]):
                    add_between(self.density,
                                x+self.vel_x[x,y],
                                y+self.vel_y[x,y],
                                self.density[x,y]*MOVE_MULT)
                    self.density[x,y] -= self.density[x,y]*MOVE_MULT
            self.vel_x *= (1-MOVE_MULT)
            self.vel_y *= (1-MOVE_MULT)

        def slow(self):

            self.vel_x *= DRAG
            self.vel_y *= DRAG

        push_dense(self)
        move(self)

        

    def draw(self):

        surf = my_interpolate.get_surface(self.density,
                                         self.scale,
                                         INTERPOLATE)
        self.surface.blit( surf, (0,0) )
        



def add_between(array, x, y, value):
    
    int_x = int(x)
    int_y = int(y)
    dec_x = x%1
    dec_y = y%1

    if not 0<x<array.shape[0]-2:
        int_x = int_x%(array.shape[0]-1)
    if not 0<y<array.shape[1]-2:
        int_y = int_y%(array.shape[1]-1)

    array[int_x  ,int_y  ] += value*(1-dec_x)*(1-dec_y)
    array[int_x+1,int_y  ] += value*(  dec_x)*(1-dec_y)
    array[int_x  ,int_y+1] += value*(1-dec_x)*(  dec_y)
    array[int_x+1,int_y+1] += value*(  dec_x)*(  dec_y)
            

def main():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    tank = Tank( screen, SCALE )
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(30)

        tank.tick()
        tank.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        #    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pressed[0]:
            tank.left_click(mouse_pos)
        if mouse_pressed[2]:
            tank.right_click(mouse_pos)        
    
    

        
if __name__ == '__main__':
    main()
