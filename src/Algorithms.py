from  GridBox import GridBox
from Graph import Graph
import pygame


def create_adjacency_matrix(rows, columns):
    '''
    (int, int)-> List[List[int]]
    
    creates an adjacency matrix of all the grids where 1s represent connections
    '''
    n=rows*columns
    matrix=[]
    
    #fill  with zeros
    for i in  range(0, n):
        matrix.append([])
        for j in range(0, n):
            matrix[i].append(0);
    
    #fill with  connections
    for i in  range(0, rows):
        for j in range(0, columns):
            index=i*columns +j
            #inner diagonals
            if j>0:
                matrix[index-1][index] = matrix[index][index-1]=1
            
            #outer diagonals
            if i>0:
                matrix[index-columns][index] = matrix[index][index-columns]=1
    
    return matrix;            

def create_gridboxes(dim, size): 
    '''
    (int, Tuple)-> List[Gridboxes]
    
    creates a list of all the Gridboxes based on the coordinates of the grid (dimesnion)
    '''  
    gridboxes=[]
    for i in range (dim, size[1]-dim, dim): 
        for j in range(dim, size[0]-dim, dim):
            g=GridBox(j, i)
            gridboxes.append(g)
    
    i=0       
    for grid in gridboxes:
        grid.idx=i
        i+=1
        
    return gridboxes

def reset(g): 
    '''
    (Graph)->none
    
    resets the attributes of the graph: gridboxes list and their indexes
    '''
    i=0   
    for grid in g.gridboxes:
        grid.prev=None
        #print ("idx ", grid.idx, " curr node: ", grid.x, ", ", grid.y, " prev: NONE!")
        grid.idx=i
        i+=1
def check_snakecollision(g, s, grid): 
    '''
    (Graph, Snake, GridBox)->bool
    
    checks if the snake has coolided with itsself.
    '''
    #check if node not on starting snake body
    for coord in s.body:
        if (coord[0]!=s.x and coord[1]!=s.y):
            if coord[0]==grid.x and coord[1]==grid.y:
                return True   
    return False

def reorder_gridboxes(g, end):  #so the end x, y coord  has the  last index
    save=GridBox(0,0)
    i=0
    for grid in g.gridboxes:
        if (grid.x==end[0] and grid.y==end[1]):
            save=grid
        else:
            grid.idx=i
            i+=1
    save.idx=i
'''
------------------------------------Breadth first search algorithm-----------------------------------
'''
def BFS(g, s, startx, starty, goalx, goaly): 
    '''
    (Graph, Snake, int, int, int, int)->List[GridBox]
    
    creates a BFS path using the starting and ending indicies
    '''
    queue=[]
    visited=[] #tuples of x and y
    
    #append start
    for grid in g.gridboxes:
        if grid.x==startx and grid.y==starty:
            queue.append (grid)
    grid=None
    loop=True
    
    while (len(queue)>0 and loop):
        grid=queue.pop(0)
        
        if (grid.x, grid.y)  in visited: #skip
            continue
        
        elif grid.x==goalx and grid.y==goaly:
            loop=False
        
        else:
            index=grid.idx
            for i in range(len(g.adjacency_matrix)):
                if g.adjacency_matrix[index][i]!=0:#found a connection 
                    if (g.gridboxes[i].x, g.gridboxes[i].y)  in visited:
                        continue
                    else:
                        add=True
                        #check if not in queue already
                        for q in queue:
                            if q.x==g.gridboxes[i].x and q.y==g.gridboxes[i].y:
                                add=False
                        
                        #check if node not on starting snake body
                        for coord in s.body:
                            if coord[0]==g.gridboxes[i].x and coord[1]==g.gridboxes[i].y:
                                add=False
                                
                        if (add):
                            queue.append(g.gridboxes[i])
                            if g.gridboxes[i].prev==None:
                                g.gridboxes[i].prev=grid
                        
            visited.append((grid.x, grid.y))
    
    #now, trace path back:
    path=[]
    if (grid.x==goalx and grid.y==goaly):
        path.append(grid)
        while (not(grid.x==startx and grid.y==starty)):
            grid=grid.prev
            path.append(grid)
        
    return list(reversed(path))
   
    
'''
------------------------------------Depth first search algorithm-----------------------------------
'''   
def  DFS(g, s, startx, starty, goalx, goaly):
    '''
    (Graph, Snake, int, int, int, int)->List[GridBox]
    
    creates a DFS path using the starting and ending indicies
    '''
    visited=[]
    stack=[]
  
    #append start
    for grid in g.gridboxes:
        if grid.x==startx and grid.y==starty:
            stack.append (grid)
    grid=None
    loop=True
    
    while (len(stack)>0 and loop):
        grid=stack.pop(-1)
        
        if (grid.x, grid.y)  in visited: #skip
            continue
        
        elif grid.x==goalx and grid.y==goaly:
            loop=False
        
        else:
            index=grid.idx
            for i in range(len(g.adjacency_matrix)):
                if g.adjacency_matrix[index][i]!=0:#found a connection 
                    if (g.gridboxes[i].x, g.gridboxes[i].y)  in visited:
                        continue
                    else:
                        add=True
                        #check if not in queue already
                        for st in stack:
                            if st.x==g.gridboxes[i].x and st.y==g.gridboxes[i].y:
                                add=False
                        
                        #check if node not on starting snake body
                        for coord in s.body:
                            if coord[0]==g.gridboxes[i].x and coord[1]==g.gridboxes[i].y:
                                add=False
                                
                        if (add):
                            stack.append(g.gridboxes[i])
                            if g.gridboxes[i].prev==None:
                                g.gridboxes[i].prev=grid
                        
            visited.append((grid.x, grid.y))
    
    #now, trace path back:
    path=[]
    if (grid.x==goalx and grid.y==goaly):
        path.append(grid)
        while (not(grid.x==startx and grid.y==starty)):
            grid=grid.prev
            path.append(grid)
        
    return list(reversed(path))

'''
------------------------------------Longest Path Breadth First search algorithm-----------------------------------
'''       
#bread first search algorithm modification
def longest_BFS(g, s, startx, starty, goalx, goaly):  
    '''
    (Graph, Snake, int, int, int, int)->List[GridBox]
    
    creates a modified BFS path using the starting and ending indicies
    ''' 
    #preform BFS
    visited=[]
    path=BFS(g, s, startx, starty, goalx, goaly)
    
    j=1
    #now try to add adjacent nodes in between
    while (j<len(path)):
        if path[j].prev==path[j-1]: #consequtive nodes
            # try to add 2 unoccupied nodes to makeit longer
            
            found_expansion=False
            has_neighbor=False
            endidx=path[j].idx
            visited.append((path[j].x, path[j].y))
            visited.append((path[j-1].x, path[j-1].y))
            
            #expand path[i-1] 
            index=path[j-1].idx 
            for i in range(len(g.adjacency_matrix)): #expand node
                if g.adjacency_matrix[index][i]!=0:#found a connection
                    #not in visited
                    if (g.gridboxes[i].x, g.gridboxes[i].y)  in visited:
                            continue
                    #in path already
                    elif g.gridboxes[i] in path:
                        continue   
                    else:
                        expand=True
                        #check if node not on starting snake body
                        for coord in s.body:
                            if coord[0]==g.gridboxes[i].x and coord[1]==g.gridboxes[i].y:
                                expand=False
                                    
                        if (expand):
                            has_neighbor=True
                            newindex=g.gridboxes[i].idx
                            for k in range(len(g.adjacency_matrix)):#expand neighboring node
                                if g.adjacency_matrix[newindex][k]!=0:#found a connection
                                    #check visited
                                    if (g.gridboxes[k].x, g.gridboxes[k].y)  in visited:
                                        continue
                                    #check on path
                                    elif  g.gridboxes[k] in path:
                                        continue
                                    else:
                                        expand=True
                                         #check if node not on starting snake body
                                        for coord in s.body:
                                             if coord[0]==g.gridboxes[k].x and coord[1]==g.gridboxes[k].y:
                                                 expand=False
                                        
                                        if (expand):
                                            #if connected to end index
                                            if g.adjacency_matrix[k][endidx]!=0: #connected to result

                                                #update prev values:
                                                g.gridboxes[i].prev=path[j-1]
                                                g.gridboxes[k].prev= g.gridboxes[i]
                                                path[j].prev=g.gridboxes[k]
                                               
                                                #we found it,isnert it to the list!
                                                path.insert(j,g.gridboxes[k])
                                                path.insert(j,g.gridboxes[i])
                                                
                                                #mark as visited
                                                visited.append((g.gridboxes[k].x ,g.gridboxes[k].y))
                                                visited.append((g.gridboxes[i].x,g.gridboxes[i].y) )
                                                
                                                found_expansion=True
                                                break;
                                        
                if (found_expansion):
                    break    

            if (not (found_expansion)):
                j+=1 #next one
    return path       
'''
----------------------------------------Hamilton algorithm------------------------------------------
''' 
'''
def hamilton_cycle(g, s, last, dim):
    path=[] #gridboxes
 
    start=GridBox(0,0)
    #find start
    for grid in g.gridboxes:
        if grid.x==s.x and grid.y==s.y:
           path.append(grid)
           print ("start: ", grid.x, ", ", grid.y, ", idx: ", grid.idx)
           start=grid
    #visited.append((s.x, s.y))
            
    #determine direction and next node:
    end=(0,0)
    next=(0,0)
    recalibrate=False
    if last==pygame.KEYUP:#at the starting pos, wee know length MUST be 0
        #defult goes right!
        end=(dim,2*dim) 
        next=(2*dim,dim)
        
    elif last==pygame.K_RIGHT:
        #startindex must be smaller than next one, and it must go horizontaly
        end=(s.body[-1][0], s.body[-1][1])
        next=(s.x+dim, s.y)
    elif last==pygame.K_LEFT:
        #startindex must be larger than next one, and it must go horizontaly
        end=(s.body[-1][0], s.body[-1][1])
        next=(s.x-dim, s.y)
    elif last==pygame.K_DOWN:
        #start index must be smaller than next one aand it must go vertically
        end=(s.body[-1][0], s.body[-1][1])
        next=(s.x, s.y+dim)
    elif last==pygame.K_UP:
         #start  index must be larger than next one aand it must go vertically
        end=(s.body[-1][0], s.body[-1][1])
        next=(s.x, s.y-dim)
    
    if recalibrate:
        #check around last  snake
        done=False
        #up
        if s.body[-1][1] -dim >=dim:
            end=(s.body[-1][0],s.body[-1][1] -dim )
            done=True
        #down
        elif s.body[-1][1]+dim <size[1]-dim and not(done):
             end=(s.body[-1][0],s.body[-1][1] +dim )
             done=True
        #left
        elif s.body[-1][0]-dim>=dim and not(done):
            end=(s.body[-1][0]-dim,s.body[-1][1])
            done=True
        #right
        elif s.body[-1][0]+dim<size[0]-dim and not(done):
            end=(s.body[-1][0]+dim,s.body[-1][1])
            done=True
       
    print ("end: ", end[0], ",  ", end[1])
    print ("next: ", next[0], ",  ", next[1])
    
    #reorder gridbox indexees  so that the end node is last
    reorder_gridboxes(g, end)
    
    #append next
    curridx=0
    for grid in g.gridboxes:
         if grid.x==next[0] and grid.y==next[1]:
            #grid.prev=start
            path.append (grid)
            #visited.append((next[0], next[1]))
            curridx=grid.idx
            #print ("added, ", grid.x, ", ", grid.y, ", idx: ", grid.idx)
            break
            #if grid.prev==None:
             #   print ("added, ", grid.x, ", ", grid.y, " prev: NONE!")
            #else:
            #    print ("added, ", grid.x, ", ", grid.y, " prev: (", grid.prev.x, grid.prev.y, ")")
    #now,recursively add nodes:
    result=hamiltonrecursive(g, s, path, end, start.idx, curridx)
    if result:
        print("hamilton was possible")
        return path
    else:
        print ("hamilton was not possible")
        return []
'''

'''
                for coord in s.body:
                    if coord[0]==g.gridboxes[n].x and coord[1]==g.gridboxes[n].y: # NEVER go on snake body
                        if coord[0]==end[0] and coord[1]==end[1]: #end of snake
                            expand=True
                            #print("-----here---")
                        else:
                            print ("CONNT BE added, ", g.gridboxes[n].x, ", ", g.gridboxes[n].y)
                            expand=False
                '''
'''    
def hamilton_cycle(g, dim):
    path=[]
    start=(dim, dim) #head of snake
    end=(dim, dim*2)
    
    #find end index
    #endidx=0
    #for grid in g.gridboxes:
     #   if grid.x==end[0] and grid.y==end[1]:
     #    endidx=grid.idx
     #    break
     
    path.append(g.gridboxes[0])
    print ("added, ", g.gridboxes[0].x, ", ", g.gridboxes[0].y)
    result=hamiltonrecursive(g, path, 0, 1) #0 is the start index
    if result:
        print("hamilton was possible")
        return path
    else:
        print ("hamilton was not possible")
        return []


    
def hamiltonrecursive(g,path, endidx, curr):
    #base case- done the cycle:
    if curr==(len(g.gridboxes)-1): #went through entirety of the list
        if  g.adjacency_matrix[curr][endidx]!=0: 
            print ("made it")
            #path.append(g.gridboxes[endidx])
            #print ("added, ", g.gridboxes[endidx].x, ", ", g.gridboxes[endidx].y)
            return True
        else:  
            return False
        
    #try next candidate
    for n in range(1,len(g.adjacency_matrix)): #expand node
        if g.adjacency_matrix[curr][n]!=0:#found a connection
             #not in visited
            if  g.gridboxes[n] in path:
                continue
            
            else:
                #expand=True
                
                #now, recursive call
                #if(expand):
                path.append(g.gridboxes[n])
                print ("added, ", g.gridboxes[n].x, ", ", g.gridboxes[n].y)
                if  (hamiltonrecursive(g, path, endidx, n))==True:
                     return True
                 
                #if doesnt give a solution, remove current vertex
                path.remove(g.gridboxes[n])
                print ("removed, ", g.gridboxes[n].x, ", ", g.gridboxes[n].y)
        
    return False             
#if grid.prev==None:
   # print ("exited here, ", grid.x, ", ", grid.y, " prev: NONE!")
#else:
   # print ("exited here, ", grid.x, ", ", grid.y, " prev: (", grid.prev.x, grid.prev.y, ")")
   
   
'''   
def hamilton_cycle(g,dim, size):
    #start=0, (30,30)
    #end: (30,60)
    path=[]
    path.append(g.gridboxes[0])
    print ("added, ", g.gridboxes[0].x, ", ", g.gridboxes[0].y)
    curr=0;
    rows=size[0]//dim-2
    while (len(path)<=len(g.gridboxes)-rows-1):
        for n in range(0,len(g.adjacency_matrix)):
             if g.adjacency_matrix[curr][n]!=0:
                if  g.gridboxes[n] in path:
                    continue
                if g.gridboxes[n].x==dim:
                    continue
                else: 
                    path.append(g.gridboxes[n])
                    print ("added, ", g.gridboxes[n].x, ", ", g.gridboxes[n].y)
                    curr=n
                    break;
    
    curr=path[-1].idx
    #now, add the rest:
    while (len(path)<len(g.gridboxes)):
        for i in range(0, len(g.adjacency_matrix)):
               if g.adjacency_matrix[curr][i]!=0:
                    if  g.gridboxes[i] in path:
                        continue
                    else:
                       path.append(g.gridboxes[i])  
                       print ("added, ", g.gridboxes[i].x, ", ", g.gridboxes[i].y) 
                       curr=i
                       break;  
                
    return path


#recursive version
def hamilton(g, size, pt, path=[]):
    #print('hamilton called with pt={}, path={}'.format(pt.idx, path))
    if pt not in path:
        path.append(pt)
        if len(path)==size:
            return path
        for pt_next in g.gridboxes:
            if g.adjacency_matrix[pt.idx][pt_next.idx]!=0:#found a connection
                side = math.sqrt(size)
                if pt_next.idx != size - side and (pt.idx-1)%side == 0 and (pt_next.idx)%side == 0:
                    print(str(pt.idx) + ' -> ' + str(pt_next.idx))
                    continue
                else:
                    res_path = [i for i in path]
                    candidate = hamilton(g, size, pt_next, res_path)
                    if candidate is not None:  # skip loop or dead end
                        return candidate
    #    print('path {} is a dead end'.format(path))
    #else:
    #    print('pt {} already in path {}'.format(pt.idx, path))
    # loop or dead end, None is implicitly returned
    

if (__name__ == "__main__"):
    size=(40,40)
    dim=10
    matrix=create_adjacency_matrix((40//10)-2, (40//10)-2)
    for item in matrix:
        print (item)
    print("------------------------------------")
    print("length: ", len (matrix))
    gridboxes=create_gridboxes(10, (40,40))
    for i in gridboxes:
        print(i.idx,": ",i.x, ", ", i.y)
    
    g=Graph(gridboxes, matrix)
    path=BFS(g, 10, 10, 20, 20)
    for grid in path:
        print(grid.x,", ", grid.y)