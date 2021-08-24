#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Reference: http://www.sarathlakshman.com/2011/04/29/writing-a-tic-tac

import copy
import time

class Game(object):
    """A tic-tac-toe game."""

    def __init__(self, grid):
        """Instances differ by their grid marks."""
        self.grid = copy.deepcopy(grid) # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            print(row)
            
    #Done by Nick
    def moves(self):
        """Return a list of possible moves given the current marks."""
        #Basically, check which space has - and return that this is a
        #a possible move. We will use it afterwards with minimax
        #returns the pair of possible locations
        moveGrid = []
        #fill array with possible moves based on what is blank, or '-'
        for i in range(3):
            for j in range(3):
                if (self.grid[i][j] == '-'):
                    moveGrid.append([i, j])
        
        return moveGrid
    #Done by both
    def neighbor(self, move, mark):
        """Return a Game instance like this one but with one move made."""
        # Mark is either 'X' or 'O', move is a 2d list, needs to return self?
        
        # fills position on board with mark and return the game state
        if self.grid[move[0]][move[1]] == '-':
            self.grid[move[0]][move[1]] = mark
        else:
            print("Position full")
        
        return self
    
    #Done by Victor
    def utility(self):
        """Return the minimax utility value of this game:
        1 = X win, -1 = O win, 0 = tie, None = not over yet."""
        # for utility here, check the code from this link
        #http://www.sarathlakshman.com/2011/04/29/writing-a-tic-tac
        #to calculate the utility of this current board.
        
        winPositions = [([0,0],[0,1],[0,2]), ([1,0],[1,1],[1,2]), ([2,0],[2,1],[2,2]), ([0,0],[1,0],[2,0]),([0,1],[1,1],[2,1]),([0,2],[1,2],[2,2]), ([0,0],[1,1],[2,2]), ([0,2],[1,1],[2,0])]
        #interate through potential win positions to see if they are currently on the board
        for i,j,k in winPositions:
            if self.grid[i[0]][i[1]] == self.grid[j[0]][j[1]] == self.grid[k[0]][k[1]] and self.grid[i[0]][i[1]] != '-':
                if self.grid[i[0]][i[1]] == 'X':
                    return 1
                elif self.grid[i[0]][i[1]] == 'O':
                    return -1
                
        # if there are not win positions, but possible moves left, return none, and return 0 when the board is full or when
        # there are no moves left
        if self.moves():
            return None
        else:
            return 0
        
            
        
        #returns an integer or None
    

class Agent(object):
    """Knows how to play tic-tac-toe."""

    def __init__(self, mark):
        """Agents use either X or O."""
        self.mark = mark
    
    #Done by both
    def maxvalue(self, game, opponent):
        """Compute the highest utility this game can have."""
        
        #if state is a completed game, return its utility
        #otherwise return the opponent's max(min-value(child)) over all children of state
        
        # copy the board for possible game states, value by default is not in favor of agent
        possibleGame = copy.deepcopy(game)
        value = -1
        move = None
        
        # iterate through possible game moves
        for i in possibleGame.moves():
            #look at current move in list
            possibleGame = possibleGame.neighbor(i, self.mark)

            #check utility resulting from move, if there is no utility, then recurse through possible board states
            utility = possibleGame.utility()
            if utility != None:
                possibleValue = utility
            else:
                # recurse through possible board states
                (possibleValue, move) = opponent.minvalue(possibleGame, self)
                
                
            # reset possible board states after recursion
            possibleGame = copy.deepcopy(game)
            
            #if the possible score is better than prior moves, take this move
            if possibleValue > value:
                value = possibleValue
                move = i       
                
        return (value, move)

    #Done by both
    def minvalue(self, game, opponent):
        """Compute the lowest utility this game can have."""
        
        #if state is a completed game, return its utility
        #otherwise return the opponent's min(max-value(child)) over all children of state
        
        # copy the board for possible game states, value by default is not in favor of agent
        possibleGame = copy.deepcopy(game)
        value = 1
        move = None
        
        # iterate through possible game moves
        for i in possibleGame.moves():
            #look at current move in list
            possibleGame = possibleGame.neighbor(i, self.mark)
            
            #check utility resulting from move, if there is no utility, then recurse through possible board states
            utility = possibleGame.utility()
            if utility != None:
                possibleValue = utility
            else:
                # recurse through possible board states
                (possibleValue, move) = opponent.maxvalue(possibleGame, self)
                
            
            # reset possible board states after recursion
            possibleGame = copy.deepcopy(game)
            
            #if the possible score is better than prior moves, take this move
            if possibleValue < value:
                value = possibleValue
                move = i
        
        return (value, move)

def main():
    """Create a game and have two agents play it."""

    game = Game([['-','-','-'], ['-','-','-'], ['-','-','-']])
    game.display()
    print("")
    
    maxplayer = Agent('X')
    minplayer = Agent('O')

    while True:
        (value, move) = maxplayer.maxvalue(game, minplayer)
        game = game.neighbor(move, maxplayer.mark)
        time.sleep(1)
        game.display()
        print("")
        
        if game.utility() is not None:
            break
        
        (value, move) = minplayer.minvalue(game, maxplayer)
        game = game.neighbor(move, minplayer.mark)
        time.sleep(1)
        game.display()
        print("")
        
        if game.utility() is not None:
            break

        
            
if __name__ == '__main__':
    main()


# In[ ]:




