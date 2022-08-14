# CS131 hw4
# Neal Zhao
# 3/30/2022


from copy import copy
import numpy as np

# Class Sudoku
# This class handles the data of a Sudoku, including its constraint status
class Sudoku:
    # Add the constraints caused by a value assignment
        # position: the position (a tuple) there this value is put
        # value: the integer value it puts in
    def add_constraint(self, position, value):
        # adding the constraints for the row and the column
        for i in range(9):
            self.constraints[i, position[1]].discard(value)
            self.constraints[position[0], i].discard(value)
        # adding the constraints for the 3x3 block
        block = (position[0]//3*3, position[1]//3*3) # positon of top left
        for i in range(3):
            for j in range(3):
                self.constraints[block[0]+i, block[1]+j].discard(value)
    
    # compute the constraint status for the whole sudoku
    def compute_constraint(self):
        self.constraints = np.empty([9,9], set)
        # this filling process must be done through loop, `np.fill` has a shallow copy problem
        for i in range(9):
            for j in range(9):
                self.constraints[i,j] = {1,2,3,4,5,6,7,8,9} # all value is valid at the beginning
        # setting constraints by each already-filled numbers
        for i in range(9):
            for j in range(9):
                if self.matrix[i,j] != 0:
                    self.add_constraint((i,j), self.matrix[i,j])
    
    # matrix: the 9x9 matrix that used to represent the sudoku puzzle
    def __init__(self, matrix):
        self.matrix = matrix.copy()
        self.compute_constraint()
    
    # make a copy of itself. 
    def copy(self):
        new = Sudoku(self.matrix.copy())
        return new
    
    # return the variable's position with minimum remaining values 
    def MRV(self):
        min_constraints_n = 9 # number of constraints
        for i in range(9):
            for j in range(9):
                if (len(self.constraints[i,j]) < min_constraints_n) and (self.matrix[i,j] == 0):
                    min_constraints_n = len(self.constraints[i,j])
                    best_place = (i,j)
        return best_place
    
    # write a number `value` into a position tuple `p`
    def update(self, p, value):
        self.matrix[p[0], p[1]] = value
        self.add_constraint((p[0], p[1]), value)
    
    # check whether the puzzle is solved.
    def check_complete(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i,j] == 0:
                    return False
        return True


# Solve the puzzle
class CSP():
    # a recursive function that solve the puzzle `s`
    def forward_checking(self, s):
        # base case: find result
        if s.check_complete():
            print('Result Found')
            return True
        # recursive case: not finished
        new = s.copy()
        i,j = new.MRV()
        possible_value = new.constraints[i,j].copy()
        for x in possible_value: # check for each possible value of the MRV position
            new.update((i,j), x)
            print('update ({},{}) to {}'.format(i,j,x))
            print(new.matrix)
            print()
            if self.forward_checking(new):
                return True



if __name__ == "__main__":
    print('Please specify which puzzle to test')
    # input which puzzle to play
    puzzle_str = input('`1` for the easy puzzle, `2` for the harder puzzle: ')
    try:
        puzzle = int(puzzle_str)
    except ValueError:
        raise ValueError('Input is not a integer')
    if puzzle != 1 and puzzle != 2:
        raise ValueError('Must be `1` or `2`')
        
    S1 = np.array(
      [[6, 0, 8, 7, 0, 2, 1, 0, 0],
       [4, 0, 0, 0, 1, 0, 0, 0, 2],
       [0, 2, 5, 4, 0, 0, 0, 0, 0],
       [7, 0, 1, 0, 8, 0, 4, 0, 5],
       [0, 8, 0, 0, 0, 0, 0, 7, 0],
       [5, 0, 9, 0, 6, 0, 3, 0, 1],
       [0, 0, 0, 0, 0, 6, 7, 5, 0],
       [2, 0, 0, 0, 9, 0, 0, 0, 8],
       [0, 0, 6, 8, 0, 5, 2, 0, 3]])
    S2 = np.array(
       [[0, 7, 0, 0, 4, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 6, 1, 0],
        [3, 9, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 4, 0, 0, 9],
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 1, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 7, 6],
        [0, 5, 4, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 1, 0, 0, 5, 0]]
    )    
    print()
    print('`0` stands for unsolved places`')
    print()
    
    if puzzle == 1:
        sudoku1 = Sudoku(S1)
        csp = CSP()
        csp.forward_checking(sudoku1)       
    else:
        sudoku2 = Sudoku(S2)
        test = CSP()
        test.forward_checking(sudoku2)

