import pygame
class Snake:
    def __init__(self, x, y, dim):
        '''
        (self, int, int,int)-> none
    
        Function to define the attributes of class Snake
    
        Attributes:
        x: x coordinate of the head, type int
        y: y coordinate of the head, type int
        dim: width of snake, type int
        body: coordinates of the nake body type List[Tuple]
        length: length of the snake, typeint
        ''' 
        self.x=x; #coord of head
        self.y=y; #coord of head
        self.dim=dim;
        self.body=[(x,y)] #list that acts as a queue
        self.length=0
    
    def draw(self, screen):
        '''
        (self, pygame display)-> none
    
        draws the snake
        '''
        #probably will be for loop to draw the snake
        for coord in self.body:
            pygame.draw.rect(screen,(222,229,141),[coord[0], coord[1], self.dim, self.dim])
    
    def update(self, last):#add new coordinates
        '''
        (self, pygame event)-> none
    
        adds a block to the end of the snake's tail
        s'''
        x=0
        y=0
        if (last==pygame.K_LEFT):
            x=self.body[-1][0]+self.dim
            y=self.body[-1][1]
            
        elif (last==pygame.K_RIGHT):  
            x=self.body[-1][0]-self.dim
            y=self.body[-1][1]
        
        elif (last==pygame.K_UP): 
            y=self.body[-1][1]+self.dim
            x=self.body[-1][0]    
        
        elif (last==pygame.K_DOWN):  
            y=self.body[-1][1]-self.dim
            x=self.body[-1][0]
        else:
            print ("last variable wrong")
        self.body.append((x,y))
    
      
    def move(self, xmove, ymove): #movesnake
        '''
        (self, int, int)-> none
    
        moves the head of the tail by xmove and ymove, and shifts the body over
        ''' 
        #move body
        if (self.length>=1):
            for i in range(self.length, 0, -1):
                self.body[i]=self.body[i-1][0], self.body[i-1][1]
        
        #move head
        self.x+=xmove
        self.y+=ymove
        self.body[0]=(self.x, self.y) 
          
    def reset (self, dim):
        '''
        (self, int)-> none
    
        resets the attributes of the snake so that a new game could start
        ''' 
        self.x=dim
        self.y=dim
        self.length=0
        self.body.clear();
        self.body=[(self.x,self.y)]
        
    def checkcollision (self): #checks the collision with itslef
        '''
        (self)-> none
    
        checks if the snake has collided with itself
        ''' 
        for i in range(1,self.length):
            x=self.body[i][0]
            y=self.body[i][1]
            if self.x==x and self.y==y:
                print ("SNAKE COLLISION")
                return True
        
        return False
    
    def AI_findmove(self, grid, dim): 
        '''
        (self, GridBox, int)-> int, int, pygame event
    
        find the next move, left, right, up, or down based on the next gridbox. 
        Returns the pygame event equivilent of the move, as well as the shift in x and y coordinates. 
        ''' 
        last=pygame.KEYUP
        xmove=0
        ymove=0
        
        if grid.x>self.x and grid.y==self.y:
            xmove=dim
            ymove=0
            last=pygame.K_RIGHT
        elif grid.x<self.x and grid.y==self.y:
            xmove=-dim
            ymove=0
            last=pygame.K_LEFT
        elif grid.x==self.x and grid.y>self.y:
            xmove=0
            ymove=dim
            last=pygame.K_DOWN
        elif grid.x==self.x and grid.y<self.y:
            xmove=0
            ymove=-dim
            last=pygame.K_UP
        return xmove, ymove, last
         
        