import game
class Stone():
    def __init__(self, color):
        self.color = color
        self.captured = False
        
########################################################################################CHAIN RULE VIOLATION############################
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
            self.stones = [[Stone(0)]*9,
                           [Stone(0)]*9,
                           [Stone(0), Stone(1), Stone(0), Stone(1), None, Stone(0), Stone(1), Stone(0), Stone(1)],
                           [Stone(1)]*9,
                           [Stone(1)]*9]
            self.whiteCount = self.blackCount = 22
        self.strong = [(0,0), (0,2), (0,4), (0,6), (0,8),
                       (1,1), (1,3), (1,5), (1,7),
                       (2,0), (2,2), (2,4), (2,6), (2,8),
                       (3,1), (3,3), (3,5), (3,7),
                       (4,0), (4,2), (4,4), (4,6), (4,8)] # strong intersections
        self.score = None
        self.blackChildren = []
        self.whiteChildren = []
        
    
    def __getitem__(self, index):
        return self.stones[index]
    
    def __setitem__(self, key, value):
        self.stones[key] = value
        
    def getPossibleMoves(self, x, y, color, direction = None, path = None):
        """
        Returns all possible moves for given player at given point.
        Capturing moves are obligatory.
        Returns empty list if point not valid, empty or does not belong to given player.
        Direction argument is used to show the forbidden direction in case of chaining.
        """
        if not self._isValidIndex(x, y) or self._isEmpty(x, y) or self.stones[x][y].color != color:
            return []
        
        directions = self._getPossibleDirections(x, y)
        appr, withd = self._getCaptureDirections(x, y, color, directions)
        if len(appr) == 0 and len(withd) == 0:
            # if there are no capturing moves with other pieces return paika moves.
            # else return no moves
            if not self._hasCapturingMoves(color) and not direction:
                return directions
            else:
                print 'HI'
                print 'prevdir: ', direction
                print 'hascapturing?: ', self._hasCapturingMoves(color)
                return []
        else:
            if direction:
                # chaining - remove forbidden directions
                l = list(set(appr+withd))
                for i, tup in enumerate(l):
                    if (x+tup[0], y+tup[1]) in path or (tup == direction):
                        del l[i]
                return l
            else:
                return list(set(appr + withd))
        
    def getCaptureDirections(self, x, y, color):
        return self._getCaptureDirections(x, y, color, self._getPossibleDirections(x, y)) 
        
    def getCaptured(self, x, y, color, direction):
        """
        Returns a list of all the stones captured by withdrawal and approach captures.
            x, y - position starting capture from.
        """
        approach, withdraw = self._getCaptureDirections(x, y, color, [direction])
        if len(approach) > 0:
            approach = []
            apprX = x + 2*direction[0]
            apprY = y + 2*direction[1]
            while self._isValidIndex(apprX, apprY) and not self._isEmpty(apprX, apprY) and self.stones[apprX][apprY].color != color:
                approach.append((apprX, apprY))
                apprX += direction[0]
                apprY += direction[1]
        if len(withdraw) > 0:
            withdraw = []
            withX = x - direction[0]
            withY = y - direction[1]
            while self._isValidIndex(withX, withY) and not self._isEmpty(withX, withY) and self.stones[withX][withY].color != color:
                withdraw.append((withX, withY))
                withX -= direction[0]
                withY -= direction[1]
        return [approach, withdraw]
    
    def remove(self, tiles):
        """ Removes given list of stones from play. Also updates stone count. """
        for tile in tiles:
            x, y = tile
            if self[x][y].color == game.WHITE:
                self.whiteCount -= 1
            elif self[x][y].color == game.BLACK:
                self.blackCount -= 1
            self[x][y] = None
            
    def hasCapturingMoves(self, x, y, color):
        a, w = self._getCaptureDirections(x, y, color, self._getPossibleDirections(x, y))
        if len(a) > 0 or len(w) > 0:
            return True
        else:
            return False
    
    def getChildren(self, color):
        """ 
        Returns a list of all possible board positions, from current, for given player.
        Also returns the moves that lead to that board position.
        [board, [(movestogetthere)]]...
        """
        self.whiteChildren = []
        self.blackChildren = []
        for i in range(5):
            for j in range(9):
                if self.stones[i][j] and self.stones[i][j].color == color:
                    for move in self.getPossibleMoves(i, j, color):
                        captured = self.getCaptured(i, j, color, move)
                        if len(captured[0]) > 0 and len(captured[1]) > 0:
                            # resolve - approach
                            newboard = Board(self)
                            moves = []
                            #path = [(i,j)]
                            #path.append((i+move[0], j+move[1]))
                            newboard.move(i, j, move)
                            moves.append(((i,j),move, 0))
                            newboard.remove(captured[0])
                            chain = newboard.chain(i+move[0], j+move[1], color, move, moves, game.path[:])
                            for link in chain:
                                if color == game.BLACK:
                                    self.blackChildren.append(link)
                                else:
                                    self.whiteChildren.append(link)
                            # resolve - withdrawal
                            newboard = Board(self)
                            moves = []
                            #path = [(i,j)]
                            #path.append((i+move[0], j+move[1]))
                            newboard.move(i, j, move)
                            moves.append(((i,j),move, 1))
                            newboard.remove(captured[1])
                            chain = newboard.chain(i+move[0], j+move[1], color, move, moves, game.path[:])
                            for link in chain:
                                if color == game.BLACK:
                                    self.blackChildren.append(link)
                                else:
                                    self.whiteChildren.append(link)
                        elif len(captured[0]) > 0 or len(captured[1]) > 0:
                            # normal capture
                            captured = captured[0] + captured[1]
                            newboard = Board(self)
                            moves = []
                            #path = [(i,j)]
                            #path.append((i+move[0], j+move[1]))
                            newboard.move(i, j, move)
                            moves.append(((i,j), move, None))
                            newboard.remove(captured)
                            chain = newboard.chain(i+move[0], j+move[1], color, move, moves, game.path)
                            for link in chain:
                                if color == game.BLACK:
                                    self.blackChildren.append(link)
                                else:
                                    self.whiteChildren.append(link)
                        else:
                            newboard = Board(self)
                            moves = []
                            newboard.move(i, j, move)
                            moves.append(((i,j), move, None))
                            if color == game.BLACK:
                                self.blackChildren.append((newboard, moves))
                            else:
                                self.whiteChildren.append((newboard, moves))
        if color == game.WHITE:
            return self.whiteChildren
        else:
            return self.blackChildren
    
    def chain(self, i, j, color, prevdir, movechain, path):
        chain = []
        for move in self.getPossibleMoves(i, j, color, prevdir, game.path):
            captured = self.getCaptured(i, j, color, move)
            if len(captured[0]) > 0 and len(captured[1]) > 0:
                # resolve - approach
                game.path = path
                newboard = Board(self)
                moves = movechain[:]
                #newpath = path[:]
                #newpath.append((i+move[0],j+move[1]))
                #newpath.append((i,j))
                newboard.move(i, j, move)
                moves.append(((i,j),move, 0))
                newboard.remove(captured[0])
                #print newpath
                children = newboard.chain(i+move[0], j+move[1], color, move, moves, game.path[:])
                for child in children:
                    chain.append(child)
                # resolve - withdrawal
                game.path = path
                newboard = Board(self)
                moves = movechain[:]
                #newpath = path[:]
                #newpath.append((i+move[0],j+move[1]))
                #newpath.append((i,j))
                newboard.move(i, j, move)
                moves.append(((i,j),move, 1))
                newboard.remove(captured[1])
                children = newboard.chain(i+move[0], j+move[1], color, move, moves, game.path[:])
                for child in children:
                    chain.append(child)
            elif len(captured[0]) > 0 or len(captured[1]) > 0:
                # normal capture
                captured = captured[0] + captured[1]
                newboard = Board(self)
                moves = movechain[:]
                #path.append((i+move[0],j+move[1]))
                #path.append((i,j))
                newboard.move(i, j, move)
                moves.append(((i,j), move, None))
                newboard.remove(captured)
                children = newboard.chain(i+move[0], j+move[1], color, move, moves, game.path)
                for child in children:
                    chain.append(child)
        if chain:
            return chain
        else:
            return [(self, movechain)]
    
    def eval(self, color):
        """
        cpu is MAX
        player is MIN
        atm both players are aggressive
        """
        if color == game.cpu:
            if color == game.WHITE:
                return 22 - self.blackCount
            else:
                return 22 - self.whiteCount                
        else:
            if color == game.WHITE:
                return self.blackCount
            else:
                return self.whiteCount
        
    def cpuWins(self):
        if game.cpu == game.BLACK:
            if self.whiteCount == 0:
                return True
            else:
                return False
        else:
            if self.blackCount == 0:
                return True
            else:
                return False
            
    def playerWins(self):
        if game.player == game.BLACK:
            if self.whiteCount == 0:
                return True
            else:
                return False
        else:
            if self.blackCount == 0:
                return True
            else:
                return False
    
    def isTerminal(self):
        return self.whiteCount == 0 or self.blackCount == 0
          
    def move(self, x, y, direction):
        game.path.append((x,y))
        i, j = direction
        self[x+i][y+j] = self[x][y]
        self[x][y] = None
        
    def _hasCapturingMoves(self, color):
        for i in range(5):
            for j in range(9):
                if self[i][j] and self[i][j].color == color:
                    if self.hasCapturingMoves(i, j, color):
                        return True
        return False
    
    def _getCaptureDirections(self, x, y, color, directions):
        """
        Returns a list of possible capturing moves with the given move directions.
        """    
        approach = []
        withdraw = []
        for direction in directions:
            i, j = direction
            
            # check for approach captures
            apprX = x + 2*i
            apprY = y + 2*j
            if self._isValidIndex(apprX, apprY) and not self._isEmpty(apprX, apprY) and self.stones[apprX][apprY].color != color:
                approach.append(direction)
                
            #check for withdrawal captures
            withX = x - i
            withY = y - j
            if self._isValidIndex(withX, withY) and not self._isEmpty(withX, withY) and self.stones[withX][withY].color != color:
                withdraw.append(direction)
        return approach, withdraw
        
    def _getPossibleDirections(self, x, y):
        """
        Returns a list of the possible move directions for a given stone
        """
        directions = []
        if self._isValidIndex(x+1, y) and self._isEmpty(x+1, y):
            directions.append((1, 0)) # down
        if self._isValidIndex(x-1, y) and self._isEmpty(x-1, y):
            directions.append((-1, 0)) # up
        if self._isValidIndex(x, y+1) and self._isEmpty(x, y+1):
            directions.append((0, 1)) # right
        if self._isValidIndex(x, y-1) and self._isEmpty(x, y-1):
            directions.append((0, -1)) # left
        if (x,y) in self.strong:
            # stones on strong intersections can also move diagonally
            if self._isValidIndex(x+1, y+1) and self._isEmpty(x+1, y+1):
                directions.append((1, 1)) # down-right
            if self._isValidIndex(x+1, y-1) and self._isEmpty(x+1, y-1):
                directions.append((1, -1)) # down-left
            if self._isValidIndex(x-1, y-1) and self._isEmpty(x-1, y-1):
                directions.append((-1, -1)) # up-left
            if self._isValidIndex(x-1, y+1) and self._isEmpty(x-1, y+1):
                directions.append((-1, 1)) # up-right
                
        return directions
        
    def _isEmpty(self, x, y):
        return self.stones[x][y] == None
    
    def _isValidIndex(self, x, y):
        if x not in range(5) or y not in range(9):
            return False
        else:
            return True
        
    def display(self):
        for i in range(5):
            for j in range(9):
                if self[i][j] and self[i][j].color == game.WHITE:
                    print 'W ',
                elif self[i][j] and self[i][j].color == game.BLACK:
                    print 'B ',
                else:
                    print '  ',
            print '\n'