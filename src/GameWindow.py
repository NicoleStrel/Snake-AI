#imports
import pygame
import time
from  Moogle import Moogle
from Snake import Snake
from Algorithms import *
from Graph import Graph
#from Algorithms import Graph
import random

pygame.init()

#USER CAN CHANGE THESE
size = (600,600) #must be >= 600x600s
dim=30; #size[0]//20
algorithm=1 #1- BFS, 2-DFS, 3-longest path, 4-Hamilton

#--------------Functions-------------------------------------
def draw_MainMenu(screen, size):
    '''
    (pyame diplay,Tuple)-> int
    
    draw the main menu of the program and returns an int of what screen we are on
    '''
    menu=1
    #colour constants
    white = (255, 255, 255)
    red = (220,20,60)
    blue=(64, 96, 161)
    green=(222,229,141)
    screen.fill(blue)

    
    #background screen
    main = pygame.image.load('pictures/mainmenu.png') 
    menu_pos=((size[0]//2) -300, (size[1]//2)-300)
    screen.blit(main, menu_pos) 
   
    #buttons
    rect1_pos=[menu_pos[0]+130, menu_pos[1]+400, 150, 50]
    rect2_pos=[menu_pos[0]+320, menu_pos[1]+400, 150, 50]
    pygame.draw.rect(screen, green,rect1_pos)
    pygame.draw.rect(screen, green,rect2_pos)
    
    mouse = pygame.mouse.get_pos()
    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
    
    #rectangle 1-play button
    if rect1_pos[0]<= mouse[0]<= rect1_pos[0]+rect1_pos[2] and rect1_pos[1]<= mouse[1]<=rect1_pos[1]+rect1_pos[3]:
        pygame.draw.rect(screen, red,rect1_pos)
        if pressed1:
            menu=2
            
    else:
        pygame.draw.rect(screen, green,rect1_pos)
    
    #rectangle 2-ai button
    if rect2_pos[0]<= mouse[0]<= rect2_pos[0]+rect2_pos[2] and rect2_pos[1]<= mouse[1]<=rect2_pos[1]+rect2_pos[3]:
        pygame.draw.rect(screen, red,rect2_pos)
        if pressed1:
            menu=3
    else:
        pygame.draw.rect(screen, green,rect2_pos)
        
    
    #fonts
    font = pygame.font.Font('freesansbold.ttf', 22)
    play = font.render("Play", True, blue) 
    ai = font.render("AI", True, blue) 
    textRect1 = play.get_rect()  
    textRect1.center = (rect1_pos[0]+(rect1_pos[2]//2), rect1_pos[1]+(rect1_pos[3]//2))
    textRect2 = ai.get_rect()  
    textRect2.center = (rect2_pos[0]+(rect2_pos[2]//2), rect2_pos[1]+(rect2_pos[3]//2))  
    screen.blit(play, textRect1) 
    screen.blit(ai, textRect2)    
    
    return menu   
 

def draw_border(screen, size, dim):
    '''
    (pyame diplay,Tuple, int)-> None
    
    draws the white border in accordance iwth size and dimension
    '''
    white = (255, 255, 255)
    rect1_pos=[0, 0, size[0], dim]
    rect2_pos=[0, 0, dim, size[1]]
    rect3_pos=[0, size[1]-dim, size[0], dim]
    rect4_pos=[size[0]-dim, 0, dim, size[1]]
     
    #draw white border
    pygame.draw.rect(screen, white,rect1_pos)
    pygame.draw.rect(screen, white,rect2_pos)
    pygame.draw.rect(screen, white,rect3_pos)
    pygame.draw.rect(screen, white,rect4_pos)
          
    
def draw_score(screen, dim, score): 
    '''
    (pyame diplay,int, int)-> None
    
    draws the score in the top left corner 
    '''
    blue=(64, 96, 161)
    font = pygame.font.Font('freesansbold.ttf', 22)
    score = font.render("Score: "+str(score), True, blue) 
    textRect = score.get_rect()  
    textRect.center = (dim*2, dim//2)
    screen.blit(score, textRect)
    
def draw_algorithm(screen, size, dim, algorithm): 
    '''
    (pyame diplay, Tuple, int, int)-> None
    
    draws the algorithm name at the top middle of the screen 
    '''
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 22)
    if algorithm==1:
        label=font.render("Breadth First Search", True, black)
    elif algorithm==2:
        label=font.render("Depth First Search", True, black)
    elif algorithm==3:
        label=font.render("Longest Path BFS", True, black)
    elif algorithm==4:
        label=font.render("Hamilton Cycle", True, black)
    textRect = label.get_rect()  
    textRect.center = (size[0]//2, dim//2)
    screen.blit(label, textRect)
    
def draw_gameover(screen, size, score):
    '''
    (pyame diplay, Tuple, int)-> None
    
    draws the game over screen and displays the final score
    '''
    menu=2
    game_over=True
    
    green=(222,229,141)
    red = (220,20,60)
    blue=(64, 96, 161)
    over = pygame.image.load('pictures/gameover.png') 
    over_pos=((size[0]//2) -300, (size[1]//2)-300)
    screen.blit(over, over_pos)
    
    rect_pos=[over_pos[0]+220, over_pos[1]+360, 150, 50]
    pygame.draw.rect(screen, green,rect_pos)
    
    
    
    mouse = pygame.mouse.get_pos()
    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
    #rectangle 1-play button
    if rect_pos[0]<= mouse[0]<= rect_pos[0]+rect_pos[2] and rect_pos[1]<= mouse[1]<=rect_pos[1]+rect_pos[3]:
        pygame.draw.rect(screen, red,rect_pos)
        if pressed1:
            game_over=False
            menu=1
            
    else:
        pygame.draw.rect(screen, green,rect_pos)
    
    #draw font
    
    font = pygame.font.Font('freesansbold.ttf', 20)
    playagain = font.render("Play Again", True, blue) 
    scoretext = font.render("Score: "+str(score), True, green) 
    textRect = playagain.get_rect()  
    textRect2 = scoretext.get_rect()
    textRect.center = (rect_pos[0]+(rect_pos[2]//2), rect_pos[1]+(rect_pos[3]//2))
    textRect2.center = (rect_pos[0]+(rect_pos[2]//2), rect_pos[1]+(rect_pos[3]//2)-50)
    screen.blit(playagain, textRect)
    screen.blit(scoretext, textRect2)
    
    return game_over, menu
    
 #---------------------------------------------------------------   
if (__name__ == "__main__"):
    #initilizing values
    screen = pygame.display.set_mode(size) 
    pygame.display.set_caption("Snek AI- Magini's Adventure")     
    exit=False;  
    frame = pygame.time.Clock()  
    menu=1;
    xmove=0;
    ymove=0;
    score=0;
    game_over=False
    last=pygame.KEYUP
    path=[]
    
    #characters
    coord=(dim, dim)
    m=Moogle(coord, dim)
    s=Snake(dim, dim, dim)
    g=Graph([], [])
    
    #------------MAIN  loop--------   
    while not exit:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu=1
                    if menu!=3 and (event.key == pygame.K_LEFT or event.key == ord('a')):
                        if last!=pygame.K_RIGHT: #restrict movement
                            xmove = -dim
                            ymove = 0
                        last=pygame.K_LEFT
                    elif menu!=3 and (event.key == pygame.K_RIGHT  or event.key == ord('d')): 
                        if last!=pygame.K_LEFT: #restrict movement
                            xmove = dim
                            ymove = 0
                        last=pygame.K_RIGHT
                    elif menu!=3 and (event.key == pygame.K_UP or event.key == ord('w')):
                        if last!=pygame.K_DOWN:#restrict movement
                            ymove = -dim
                            xmove = 0
                        last=pygame.K_UP
                    elif menu!=3 and (event.key == pygame.K_DOWN or event.key == ord('s')):
                        if last!=pygame.K_UP:#restrict movement
                            ymove = dim
                            xmove = 0
                        last=pygame.K_DOWN
        #graphics/action listeners
        blue=(64, 96, 161)
            
        '''
            ---------------------------------Main Menu----------------------------------------------
            '''
        if menu==1:
            started=False
            indicator=False
            game_over=False
            score=0
            path=[]
            xmove=0
            ymove=0
            reset(g)
            menu=draw_MainMenu(screen, size)
            if menu==2:
                s.reset(dim)
                m.coord=m.random_coord(size, s)
            if menu==3:
                s.reset(dim)
                #create graph
                g.gridboxes=create_gridboxes(dim, size);
                g.adjacency_matrix=create_adjacency_matrix((size[0]//dim)-2, (size[1]//dim)-2);
                m.coord=m.random_coord(size, s)
    
                if (algorithm==1):
                    path=BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                    path.pop(0) #starting node, already there
                elif (algorithm==2):
                    path=DFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                    path.pop(0) #starting node, already there
                elif (algorithm==3):
                    path=longest_BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                    path.pop(0) #starting node, already there
                elif (algorithm==4):
                    path=hamilton_cycle(g, s, last, dim)
                    path.pop(0) #starting node, already there
                    #for grid in path:
                        #if grid.prev==None:
                          #  print ("Grid:, ", grid.x, ", ", grid.y, " prev: NONE!")
                       # else:
                           # print ("Grid:, ", grid.x, ", ", grid.y, " prev: (", grid.prev.x, grid.prev.y, ")")
                
            '''
            ---------------------------------Game/ AI Screen----------------------------------------------
            '''
        elif menu==2 or menu==3:             
            if game_over==True:
                screen.fill(blue)
                game_over, menu=draw_gameover(screen, size, score)
            else:  
                screen.fill(blue)
                m.draw(screen, size)
                
                if menu==3:
                    #print("path here: ", path)
                    if len(path)>0:
                        collision=False # local variable
                        grid=path.pop(0)
                        collision=check_snakecollision(g, s, grid)
                        if (collision):
                            path.clear()
                            reset(g)
                            #RUN ALGORITHM AGAIN
                            if (algorithm==1):
                                path=BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            elif (algorithm==2):
                                path=DFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                                #if path!=[]:
                                    #path.pop(0) #starting node, already there
                            elif (algorithm==3):
                                path=longest_BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                                #if path!=[]:
                                    #path.pop(0) #starting node, already there
                            elif (algorithm==4):
                                 path=hamilton_cycle(g, s, last, dim)
                            #check path
                            if (path==[]):
                                collision=True
                                print ("failed here: grid: ", grid.x, grid.y)
                            else:
                                path.pop(0) #starting node, already there
                                grid=path.pop(0)
                                collision=check_snakecollision(g, s, grid)
                            #check collision
                            if (collision):#a second time, no more paths :(
                                print ("failed here: grid: ", grid.x, grid.y)
                                path=[]
                            else:
                                xmove, ymove, last=s.AI_findmove(grid, dim)
                                
                        else:
                            xmove, ymove, last=s.AI_findmove(grid, dim)   
                        #print ("grid: ", grid.x, ", ", grid.y)
                        #for hi in path:
                        #    print(hi.x,", ",hi.y)
                        #print ("-----------")
    
                    else:
                        print("NO PATHS WHERE SNAKE DOESNT COLLIDE") 
                        game_over=True
                
                if (not (game_over)):
                   # print ("before: ",s.body,"x/ ymove: ", xmove, ymove)
                    s.move(xmove, ymove)#CULPRIT
                    #print ("after: ", s.body)
                    s.draw(screen) 
        
                    #check boundries
                    if s.x >= dim and s.x <=size[0]-dim*2  and s.y >= dim and s.y <= size[1]-dim*2: #in between
                        game_over = s.checkcollision() #check snake collision now
                    else:
                        game_over=True
                        print ("BORDER COLLISION")
                        
            
                    #food detection
                    if s.x==m.coord[0] and s.y==m.coord[1]:
                        print ("MOOGLE EATEN")
                        score+=1
                        m.coord=m.random_coord(size, s)
                        s.update(last)
                        s.length=s.length+1
                        
                        if menu==3:
                            #call depth first search
                            path.clear()
                            reset(g)
                            if (algorithm==1):
                                path=BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            elif (algorithm==2):
                                path=DFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            elif (algorithm==3):
                                path=longest_BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            elif (algorithm==4):
                                 path=hamilton_cycle(g, s, last, dim)
                            
                            if path!=[]:
                                path.pop(0) #starting node, already there
                            else:
                                print ("failed at initial search after moogle")
                        s.draw(screen)
                        
                    draw_border(screen, size, dim)
                    draw_score(screen, dim, score)   
                    if menu==3:
                        draw_algorithm (screen, size, dim, algorithm)
                   
        pygame.display.flip() #update screen
        frame.tick(10*4)
    
    pygame.quit() 
