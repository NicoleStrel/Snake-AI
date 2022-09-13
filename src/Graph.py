#Adapted from ESC190 graphs.py
class Graph:  
 def __init__(self, gridboxes, adjacency_matrix):
    '''
    (self, List[Gridboxes], List[List[int]])-> none

    Function to define the attributes of class Graph

    Attributes:
    gridboxes: list of all the Gridboxes, type List[Gridboxes]
    adjacency_matrix: an adjacency matrix of all the grids where 1s represent connections , type  List[List[int]]
    ''' 
    self.gridboxes = gridboxes 
    self.adjacency_matrix = adjacency_matrix 