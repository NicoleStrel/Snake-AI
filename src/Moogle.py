import pygame
import random

class Moogle:
    def __init__(self,coord, dim):
        '''
        (self, Tuple, int)-> none
    
        Function to define the attributes of class Moogle
    
        Attributes:
        coord: coordinate of the moogle, type Tuple
        dim: width of moogle, type int
        ''' 
        self.coord=coord #tuple
        self.dim=dim
        
    def draw(self, screen, size):
        '''
        (self, pygame display, Tuple)-> none
    
        draws the moogle
        '''
        pygame.draw.rect(screen, (220,20,60),[self.coord[0], self.coord[1], self.dim, self.dim])
    
    def random_coord(self,size, s):
        '''
        (self, Tuple, Snake)-> int, int
    
        determines the coordinates of the moogle
        '''
        retry=True
        
        while (retry):
            x=random.randrange(self.dim,size[0]-self.dim, self.dim )
            y=random.randrange(self.dim,size[1]-self.dim, self.dim )
            
            #check if not on snake
            again=False
            for i in range(len(s.body)):
                
                snakex=s.body[i][0]
                snakey=s.body[i][1]
                if snakex==x and snakey==y:
                    again=True
            
            if (again): #check for collision
                retry=True
            else:
                retry=False
            
        return x,y
     
           