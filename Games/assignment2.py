import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):
        grid = []
        for num in range(row):
            row_list = []
            for amount in range(col):
                row_list.append(0)
            grid.append(row_list)
        
        return grid
            
    def setCell(self, cell, val):
        row = int(cell/len(self._grid))
        col = cell%len(self._grid)
        
        self._grid[row][col] = val


    def getCell(self, cell):
        row = int(cell/len(self._grid))
        col = cell%len(self._grid)
        
        return self._grid[row][col]

    def assignRandCell(self, init=False):

        """
        This function assigns a random empty cell of the grid
        a value of 2 or 4.

        In __init__() it only assigns cells the value of 2.

        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned
        a value of 4
        """

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):

        """
        This function draws the grid representing the state of the game
        grid
        """

        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)
        print()


    def updateEmptiesSet(self):

        """
        This function should update the list of empty cells of the grid.
        """
        self.emptiesSet = []
        start_grid = []
        for cell in range(self.row*self.col):
            start_grid.append(self.getCell(cell))
            
        for cell in range(len(start_grid)):
            if self.getCell(cell) == 0:
                self.emptiesSet.append(cell)
                
    def collapsible(self):
        """
        This function should test if the grid of the game is collapsible
        in any direction (left, right, up or down.)

        It should return True if the grid is collapsible.
        It should return False otherwise.
        """
        collapse = False
        test_grid = []
        for cell in range(self.row*self.col):
            test_grid.append(self.getCell(cell))
            if self.getCell(cell) == 0:
                collapse = True
        if not collapse:
            test_grid = [test_grid[i:i+self.row] for i in range(0, len(test_grid), self.row)]
            # check horizontal matches
            for row in test_grid:
                check_cell = 0
                for cell in row:
                    if check_cell == cell:
                        collapse = True
                    else:
                        check_cell = cell
            # check vertical matches
            for index in range(self.row):
                check_cell = 0
                for row in test_grid:
                    if row[index] == check_cell:
                        collapse = True
                    else:
                        check_cell = row[index]
        return collapse
        
    def collapseRow(self, lst):

        """
        This function takes a list lst and collapses it to the LEFT.

        This function should return two values:
        1. the collapsed list and
        2. True if the list is collapsed and False otherwise.
        """
        new_list= []
        check_list = list(lst)
        coll = True
        # remove zeros
        while 0 in lst: 
            lst.remove(0)
        while lst != []:
            new_list.append(lst.pop(0))
            try:
                if new_list[-1] == lst[0]:
                    new_num = new_list[-1] + lst.pop(0)
                    new_list[-1] = new_num
                    self.score =  self.score + new_num
            except IndexError:
                pass
        trailer = len(check_list) - len(new_list)
        if trailer != 0:
            for i in range(trailer):
                new_list.append(0)
        #print('New Row')
        #print('OG',check_list)
        #print('newbert',new_list)
        if check_list == new_list:
            coll = False
        print(coll)
        return (new_list,coll)

    def collapseLeft(self):

        """
        This function should use collapseRow() to collapse all the rows
        in the grid to the LEFT.

        This function should return True if any row of the grid is collapsed
        and False otherwise.
        """
        results = []
        start_grid = []
        for cell in range(self.row*self.col):
            start_grid.append(self.getCell(cell))
        start_grid = [start_grid[i:i+self.row] for i in range(0, len(start_grid), self.row)]
        
        collapse = False
        new_grid = []
        for row in start_grid:
            row_tuple = self.collapseRow(row)
            new_row = row_tuple[0]
            results.append(row_tuple[1])
            for cell in new_row:
                new_grid.append(cell)       
        for index in range(self.row*self.col):
            self.setCell(index,new_grid[index])
            
        if True in results:
            collapse = True
            
        return collapse
        
    def collapseRight(self):

        """
        This function should use collapseRow() to collapse all the rows
        in the grid to the RIGHT.

        This function should return True if any row of the grid is collapsed
        and False otherwise.
        """
        results = []
        start_grid = []
        for cell in range(self.row*self.col):
            start_grid.append(self.getCell(cell))
        start_grid = [start_grid[i:i+self.row] for i in range(0, len(start_grid), self.row)]
        
        collapse = False
        new_grid = []        
        for row in start_grid:
            reverse_row = []
            for cell in reversed(row):
                reverse_row.append(cell)
            row_tuple = self.collapseRow(reverse_row)
            new_row = row_tuple[0]
            results.append(row_tuple[1])                
            for cell in reversed(new_row):
                new_grid.append(cell)       
        for index in range(self.row*self.col):
            self.setCell(index,new_grid[index])
            
        if True in results:
            collapse = True
            
        return collapse

    def collapseUp(self):

        """
        This function should use collapseRow() to collapse all the columns
        in the grid to UPWARD.

        This function should return True if any column of the grid is
        collapsed and False otherwise.
        """
        results = []
        collapse = False
        start_grid = []
        for cell in range(self.row*self.col):
            start_grid.append(self.getCell(cell))
        start_grid = [start_grid[i:i+self.row] for i in range(0, len(start_grid), self.row)]
        
        columns = []
        for index in range(self.row):
            col = []
            for row in start_grid:
                col.append(row[index])
            columns.append(col)
            
        colp_cols = []
        for col in columns:
            col_tuple = self.collapseRow(col)
            colp_cols.append(col_tuple[0])
            results.append(col_tuple[1])                        
        new_grid = []
        for index in range(self.row):
            for col in colp_cols:
                new_grid.append(col[index])
                
        for index in range(self.row*self.col):
            self.setCell(index,new_grid[index])
            
        if True in results:
            collapse = True
        
        return collapse 
                
    def collapseDown(self):

        """
        This function should use collapseRow() to collapse all the columns
        in the grid to DOWNWARD.

        This function should return True if any column of the grid is
        collapsed and False otherwise.
        """
        results = []
        collapse = False
        start_grid = []
        for cell in range(self.row*self.col):
            start_grid.append(self.getCell(cell))
        start_grid = [start_grid[i:i+self.row] for i in range(0, len(start_grid), self.row)]
        
        columns = []
        for index in range(self.row):
            col = []
            for row in start_grid:
                col.append(row[index])
            columns.append(col)
        
        rev_cols = []    
        for col in columns:
            rev_col = []
            for num in reversed(col):
                rev_col.append(num)
            rev_cols.append(rev_col)
            
        colp_cols = []
        for col in rev_cols:
            col_tuple = self.collapseRow(col)
            colp_cols.append(col_tuple[0])
            results.append(col_tuple[1])                      
        new_grid = []
        for index in reversed(range(self.row)):
            for col in colp_cols:
                new_grid.append(col[index])
                
        for index in range(self.row*self.col):
            self.setCell(index,new_grid[index])
            
        if True in results:
            collapse = True

        return collapse
    
class Game():
    def __init__(self, row=4, col=4, initial=2):
        """
        Creates a game grid and begins the game
        """

        self.game = Grid(row, col, initial)
        self.play()

    def printPrompt(self):

        """
        Prints the instructions and the game grid with a move prompt
        """

        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')

def main():
    game = Game()
 
main()