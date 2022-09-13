#imports
import pygame
import time
from GameWindow import *
from Algorithms import *
from  Moogle import Moogle
from Snake import Snake
from Graph import Graph

def run (algorithm, size, speed):
    '''
    (int, Tuple, int )->bool, List[int], int, int
    
    runs the game based on the algorithm type, size and speed using the Gamewindow functionality and returns
    the winds, the list of all the times to eat the  Moogle, the total score, and the number of gridboxes for that size
    '''
    #initilizing values
    screen = pygame.display.set_mode(size) 
    pygame.display.set_caption("Snek AI- Magini's Adventure")     
    exit=False;  
    frame = pygame.time.Clock()  
    xmove=0;
    ymove=0;
    score=0;
    game_over=False
    last=pygame.KEYUP
    path=[]
    times=[]
    blue=(64, 96, 161)
    dim=30
    pathduplicate=[]
    numboxes=0
    
    #characters
    coord=(dim, dim)
    m=Moogle(coord, dim)
    s=Snake(dim, dim, dim)
    g=Graph([], [])
    
    #set up
    s.reset(dim)
    t0 = time.time()
    #create graph
    g.gridboxes=create_gridboxes(dim, size);
    numboxes=len(g.gridboxes)
    g.adjacency_matrix=create_adjacency_matrix((size[0]//dim)-2, (size[1]//dim)-2);
    m.coord=m.random_coord(size, s)
    #print("moogle, ", m.coord[0], ", ", m.coord[1])

    if (algorithm==1):
        path=BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
        if path!=[]:
            path.pop(0) #starting node, already there
    elif (algorithm==2):
        path=DFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
        path.pop(0) #starting node, already there
    elif (algorithm==3):
        path=longest_BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
        path.pop(0) #starting node, already there
    elif (algorithm==4):
        path=hamilton_cycle(g, dim, size)
        pathduplicate=path
        #for p in path:
            #print (p.x,", ",p.y)
   
    
    #------------MAIN  loop--------   
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
    
        if game_over==True:
            win=False
            if len(s.body)==len(g.gridboxes):
                win=True
            return win, times, score, numboxes
        else:
            screen.fill(blue)
            m.draw(screen, size)
            if len(path)>0:
                    collision=False # local variable
                    grid=path.pop(0)
                   # print ("current gridbox: ", grid.x, ", ", grid.y)
                    #print("snake: ")
                    #for sn in s.body:
                        #print (sn[0], ", ", sn[1])
                    collision=check_snakecollision(g, s, grid)
                    if (collision):
                        if algorithm!=4:
                            path.clear()
                        reset(g)
                        #RUN ALGORITHM AGAIN
                        if (algorithm==1):
                            path=BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            if (path!=[]):
                                path.pop(0) #starting node, already there
                        elif (algorithm==2):
                            path=DFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            if (path!=[]):
                                path.pop(0) #starting node, already there
                        elif (algorithm==3):
                            path=longest_BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                            if (path!=[]):
                                 path.pop(0) #starting node, already there
                        elif (algorithm==4):
                            print ("something went wrong")
                            #path=hamilton_cycle(g, dim, size)
                             #for p in path:
                                 #print (p.x,", ",p.y)
                        #check path
                        if (path==[]):
                            collision=True
                            print ("failed here: grid: ", grid.x, grid.y)
                        else:
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
                        

            else:
                
                if algorithm==4:
                    print ("hi")
                    path=hamilton_cycle(g, dim, size)
                    #for p in path:
                       # print (p.x,", ",p.y)
                    grid=path.pop(0)
                    xmove, ymove, last=s.AI_findmove(grid, dim)  
                else:
                    print("NO PATHS WHERE SNAKE DOESNT COLLIDE/ FIND MOOGLE") 
                    game_over=True
            
            if (not (game_over)):
               # print ("before: ",s.body,"x/ ymove: ", xmove, ymove)
                s.move(xmove, ymove)#CULPRIT
                #print ("after: ", s.body)
                s.draw(screen) 
    
                #check boundries
                print ("head: ", s.x, ", ",s.y)
                if s.x >= dim and s.x <=size[0]-dim*2  and s.y >= dim and s.y <= size[1]-dim*2: #in between
                    game_over = s.checkcollision() #check snake collision now
                else:
                    game_over=True
                    print ("BORDER COLLISION")
                    
        
                #food detection
                if s.x==m.coord[0] and s.y==m.coord[1]:
                    print ("MOOGLE EATEN")
                    #time 
                    t1 = time.time()
                    times.append(t1-t0)
                    t0 = time.time()
                    
                    score+=1
                    print ("hi 1 ")
                    m.coord=m.random_coord(size, s)
                    print ("hi 2 ")
                    #print("moogle, ", m.coord[0], ", ", m.coord[1])
                    s.update(last)
                    s.length=s.length+1
                    
                    #call depth first search
                    if algorithm!=4:
                        path.clear()
                    
                    if (algorithm==1):
                        reset(g)
                        path=BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                        if (path!=[]):
                            path.pop(0) #starting node, already there
                    elif (algorithm==2):
                        reset(g)
                        path=DFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                        if (path!=[]):
                            path.pop(0) #starting node, already there
                    elif (algorithm==3):
                        reset(g)
                        path=longest_BFS(g, s, s.x, s.y, m.coord[0], m.coord[1])
                        if (path!=[]):
                            path.pop(0) #starting node, already there
                    elif (algorithm==4):
                        print ("entered- body:", len(s.body), ", grids: ", len(g.gridboxes))
                        if len(s.body)==len(g.gridboxes):
                            print ("game_over")
                            game_over=True
                        #path=pathduplicate
                    #elif (algorithm==4):
                        #path=hamilton_cycle(g, dim, size)
                         #for p in path:
                          #   print (p.x,", ",p.y)
                    print ("hi")
                    if path==[]:
                        print ("failed at initial search after moogle")
                    
                    s.draw(screen)
                    
                draw_border(screen, size, dim)
                draw_score(screen, dim, score)   
                draw_algorithm (screen, size, dim, algorithm)
    
        pygame.display.flip() #update screen
        frame.tick(10*speed)

    pygame.quit() 

 
    
def testing_commands(algorithm):
    '''
    (int)->None
    
    testing script for all four algorithms
    ''' 
    if algorithm==1:
        f = open("testing/BFS_testing.txt", "w")
        f.write("=================TESTING BREADTH FIRST SEARCH==================\n")
    elif algorithm==2:
        f = open("testing/DFS_testing.txt", "w")
        f.write("=================TESTING DEPTH FIRST SEARCH====================\n")
    elif algorithm==3:
        f = open("testing/BFS_modified_testing.txt", "w")
        f.write("==========TESTING LONGEST PATH BFS MODIFICATION================\n")
    elif algorithm==4:
        f = open("testing/Hamilton_testing.txt", "w")
        f.write("=====================TESTING HAMILTON =========================\n")
    
    #controls
    size=(600,600) 
    speed=2
    
    #OBJECTIVE 1, 2, 3
    f.write("-----Objective 1, 2, 3: testing wins, time conservation and preformance----------\n")
    f.write("control: board size-600x600, speed-2\n")
    f.write("variable: moogle locations\n")
    f.write("\n")
    f.write("Trial\tWin\tAvTime(sec)\tScore\n")
    
    runs=1
    maxim=100
    wins=0
    averages=0
    total=0
    while (runs<=maxim):
        win, times, score, numboxes=run (algorithm, size, speed)
        print(runs)
        #times
        sum=0
        for t in times:
             sum+=t
        av=sum/len(times)
        averages+=av
        
        #wins
        result=""
        if win:
            wins+=1
            result="Win"
        else:
            result="Loss"
        
        #score
        total+=score
        
        f.write(str(runs)+"\t"+result+"\t"+str(round(av,4))+"\t"+str(score)+"\n")
        runs+=1
    
    
    f.write("\n")
    f.write("Summary: \n")
    f.write("Wins over trails: "+str(round(wins/maxim, 2))+ "\n")
    f.write("Totaled average time (sec): "+str(round (averages/maxim,4))+"\n")
    f.write("Total score: "+ str(total)+"\n")
    avscore=total/maxim
    f.write("Average Score: "+ str(round(avscore,2))+"\n")
    f.write("Average grid fill percentage: "+str(round(avscore/numboxes,2)*100)+"%\n")
    
    
    #OBJECTIVE 4
    f.write("\n")
    f.write("---------Objective 4: testing board size adaptability---------\n")
    f.write("control: speed-5\n")
    f.write("variables: board size, moogle locations\n")
    f.write("\n")
    
    #cases
    case1=(180, 180) #smallest possible with snake width (30)
    case2=(210, 210)
    case3=(240,240) 
    case4=(300, 300) 
    case5=(420, 420) 
    case6=(450, 450) 
    case7= (510,510)
    case8=(600,600) 
    case9=(840,840) 
    case10=(900,900) #laargest that caan fit on computer screen (macOS Mojave 10.14.5)
    cases=[case1, case2, case3, case4, case5, case6, case7, case8, case9, case10]
    
    runs=1
    max=10
    for case in cases:
        f.write (str(case[0])+","+str(case[1])+":\n")
        runs=1
        average=0
        while (runs<=max):
            win, times, score, numboxes=run (algorithm, case, 5)
            f.write(str(runs)+"-grid fill percentage: "+str(round(score/numboxes, 2)*100)+"%\n")
            average+=score
            print(runs)
            runs+=1
        
        avscore=average/max
        f.write("Average grid fill percentage: "+str(round(avscore/numboxes, 2)*100)+"%\n")
    
    
    f.close()

if (__name__ == "__main__"):
    #testing_commands()  
    win, times, score, numboxes=run(4, (300, 300), 5)
    print("win: ", win)
     #print("times: ", times)
     #print ("score: ", score)
    # testing_commands(2)
    
    