class GridBox:
    def __init__(self,x, y):
        '''
        (self, int, int)-> none
    
        Function to define the attributes of class Gridbox
    
        Attributes:
        x: x coordinate of the Gridbox, type int
        y: y coordinate of the Gridbox, type int
        prev: the previous gridbox connection, type Gridbox
        idx: the index of the Gridbox, type int
        ''' 
        self.x=x;
        self.y=y;
        self.prev=None
        self.idx=0