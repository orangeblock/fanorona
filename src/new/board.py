import logic
import utils
from constants import *

class Board():
    """
    A logical representation of the game board as list of lists.
    Each list represents a row and contains stones(Stone class).
    """
    def __init__(self, b = None):
        if b:
            self.stones = [sub[:] for sub in b.stones]
            self.whiteCount = b.whiteCount
            self.blackCount = b.blackCount
        else:
            self.stones = [[BLACK]*9,
                           [BLACK]*9,
                           [BLACK, WHITE, BLACK, WHITE, NULL, BLACK, WHITE, BLACK, WHITE],
                           [WHITE]*9,
                           [WHITE]*9]
            self.whiteCount = self.blackCount = 22
        self.strong = [(0,0), (0,2), (0,4), (0,6), (0,8),
                       (1,1), (1,3), (1,5), (1,7),
                       (2,0), (2,2), (2,4), (2,6), (2,8),
                       (3,1), (3,3), (3,5), (3,7),
                       (4,0), (4,2), (4,4), (4,6), (4,8)] # strong intersections
        self.moves = {}
        self.score = None
        self.blackChildren = []
        self.whiteChildren = []
        
    def __getitem__(self, index):
        return self.stones[index]
    
    def __setitem__(self, key, value):
        self.stones[key] = value
        
    def adjacent(self, pos):
        """
        Returns all neighboring free positions to given.
        """
        neighbors = []
        directions = NDIRECTIONS
        if pos in self.strong:
            directions = NDIRECTIONS + DDIRECTIONS
        for d in directions:
            newpos = utils.tadd(pos, d)
            if self.valid(newpos) and self.empty(newpos):
                neighbors.append(newpos)
        return neighbors
    
    def move(self, x1, y1, x2, y2):
        """ Moves a stone from one position to another. No checking. """
        self[x2][y2] = self[x1][y1]
        self[x1][y1] = NULL
        
    def calcmoves(self):
        """
        Updates the board possible moves using the game logic.
        The result is a dict with starting positions as keys
        and possible end positions as values.
        """
        for i in range(5):
            for j in range(9):
                if self[i][j] != NULL:
                    self.moves[(i,j)] = logic.refine(self, (i,j), self.adjacent((i,j)))
        
    def valid(self, pos):
        x, y = pos
        if x not in range(5) or y not in range(9):
            return False
        else:
            return True
    
    def empty(self, pos):
        x, y = pos
        if self[x][y] == NULL:
            return True
        return False
    
    def display(self):
        for i in range(5):
            for j in range(9):
                if self[i][j] == WHITE:
                    print 'W ',
                elif self[i][j] == BLACK:
                    print 'B ',
                else:
                    print '  ',
            print '\n'
            
if __name__ == '__main__':
    b = Board()
    b.calcmoves()
    b.display()
    for i in range(5):
        for j in range(9):
            if b[i][j] == BLACK:
                print (i,j), b.moves[(i,j)]