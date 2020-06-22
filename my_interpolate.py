import numpy as np
import pygame
import cv2

SCREEN_SIZE = [400,400]
SCALE = 10
GRID_SIZE = (SCREEN_SIZE[0]//SCALE,SCREEN_SIZE[1]//SCALE)

def dont(array,scale):

    new_array = np.repeat(np.repeat(array,scale,axis=0),scale,axis=1)

    return new_array


def bad(array,scale):
    
    shape=array.shape
    new_array = np.zeros( ((shape[0]+1)*scale,(shape[1]+1)*scale) )

    dim_array = np.repeat(np.repeat(array,scale,axis=0),scale,axis=1)/scale**2

    for x in range(scale):
        for y in range(scale):
            new_array[ x:shape[0]*scale+x, y:shape[1]*scale+y ] += dim_array

    return new_array[scale//2:shape[0]*scale+scale//2, scale//2:shape[1]*scale+scale//2]
            

def stolen(array,scale):

    shape = array.shape

    new_array = cv2.resize(array, dsize=(shape[0]*scale,shape[1]*scale), interpolation=cv2.INTER_CUBIC)

    return new_array



def get_surface(array,scale,function):

    #smallerSize = array.shape[0]//scale,array.shape[1]//scale

    #np.random.seed(0)
    #array = np.random.randint( 0,255, size=smallerSize,dtype='uint8' )
    array = function(array,10)
    array[array<0] = 0
    array[array>255] = 255

    surf = pygame.Surface((array.shape[0]*scale,array.shape[1]*scale))

    surfarray = pygame.surfarray.pixels3d(surf)

    surfarray[:array.shape[0],:array.shape[1],0] = array
    surfarray[:array.shape[0],:array.shape[1],1] = array
    surfarray[:array.shape[0],:array.shape[1],2] = array

    del surfarray

    return surf




def show():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    currentFunction = 0
    functions = [dont,bad,stolen]

    np.random.seed(0)
    baseArray = np.random.randint( 0,255, GRID_SIZE,dtype='uint8' )

    surf = get_surface(baseArray,SCALE,functions[currentFunction])
    screen.blit(surf,(0,0))
    pygame.display.update()

    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                currentFunction = (currentFunction+1)%len(functions)
                surf = getSurface(baseArray,SCALE,functions[currentFunction])
                screen.blit(surf,(0,0))
                pygame.display.update()                



if __name__ == '__main__':
    show()
  
