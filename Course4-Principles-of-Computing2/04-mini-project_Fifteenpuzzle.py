'''
Loyd's Fifteen puzzle (solver and visualizer)
note that solved configuration has the blank (zero) tile in upper left;
use the arrows key to swap this tile with its neighbors
'''
import poc_fifteen_gui
class Puzzle:
    '''
    class representation for The Fifteen Puzzle
    '''

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        '''
        initialize puzzle with default height and width;
        returns a Puzzle object
        '''
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        '''
        generate string representation for puzzle;
        returns a string
        '''
        ans = ''
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += '\n'
        return ans
#####################################
    # GUI methods

    def get_height(self):
        '''
        getter for puzzle height; returns an integer
        '''
        return self._height

    def get_width(self):
        '''
        getter for puzzle width; returns an integer
        '''
        return self._width

    def get_number(self, row, col):
        '''
        getter for the number at tile position pos; returns an integer
        '''
        return self._grid[row][col]

    def set_number(self, row, col, value):
        '''
        setter for the number at tile position pos
        '''
        self._grid[row][col] = value

    def clone(self):
        '''
        make a copy of the puzzle to update during solving;
        returns a Puzzle object
        '''
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

########################################################
    # core puzzle methods

    def current_position(self, solved_row, solved_col):
        '''
        locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved;
        returns a tuple of two integers
        '''
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, 'Value ' + str(solved_value) + ' not found'

    def update_puzzle(self, move_string):
        '''
        updates the puzzle state based on the provided move string
        '''
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == 'l':
                assert zero_col > 0, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == 'r':
                assert zero_col < self._width - 1, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == 'u':
                assert zero_row > 0, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == 'd':
                assert zero_row < self._height - 1, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, 'invalid direction: ' + direction

#############################################################
# phase one methods

    def lower_row_invariant(self, target_row, target_col):
        '''
        check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1);
        returns a boolean
        '''
        # Position zero(0) tile at (i, j)
        if self.get_number(target_row, target_col) == 0:
            # solve all tiles in row i to the right of position (i, j)
            for columns in range(target_col + 1, self.get_width()):
                if not (target_row, columns) == self.current_position(target_row, columns):
                    return False
            # position all tiles in rows i + 1 or below at solved locations
            # stop check if zero(0) tile is in last row
            if not target_row + 1 == self.get_height():
                for col_beneath in range(0, self.get_width()):
                    if not (target_row + 1, col_beneath) == self.current_position(target_row + 1, col_beneath):
                        return False
            return True

        return False

    def move(self, target_row, target_col, row, column):
        '''
        position a tile at target position; target tile's current position must
        be above the target position (k < i) or on the same row to the left (i = k and l < j);
         '''
        move_string = ''
        move_steps = 'druld'

        # calculate row and column variations
        col_change = target_col - column
        row_change = target_row - row

        # always move up arrow first
        move_string += row_change * 'u'
        # for both tiles in the same column, move_steps 'ld' will go first
        if col_change == 0:
            move_string += 'ld' + (row_change - 1) * move_steps
        else:
            # for tiles on the left form target, specific move first
            if col_change > 0:
                move_string += col_change * 'l'
                if row == 0:
                    move_string += (abs(col_change) - 1) * 'drrul'
                else:
                    move_string += (abs(col_change) - 1) * 'urrdl'
            # for tiles on the right from target, specific move first
            elif col_change < 0:
                move_string += (abs(col_change) - 1)  * 'r'
                if row == 0:
                    move_string += abs(col_change) * 'rdllu'
                else:
                    move_string += abs(col_change) * 'rulld'
            # always make common move as last
            move_string += row_change * move_steps

        return move_string


    def solve_interior_tile(self, target_row, target_col):
        '''
        makes use of helper function move()
        updates puzzle and returns a move string
        '''
        assert self.lower_row_invariant(target_row, target_col)
        # open tile values for rows and columns
        row, column = self.current_position(target_row, target_col)
        move_string = self.move(target_row, target_col, row, column)

        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_col0_tile(self, target_row):
        '''
        solve tile in column zero on specified row (> 1);
        updates puzzle and returns a move string
        '''
        assert self.lower_row_invariant(target_row, 0)
        move_string = 'ur'
        self.update_puzzle(move_string)

        # open row and column tile values
        row, column = self.current_position(target_row, 0)
        if row == target_row and column == 0:
            # move tile zero(0) to the right end of that row
            pos = (self.get_width() - 2) * 'r'
            self.update_puzzle(pos)
            move_string += pos
        else:
            # target tile at position (i-1, 1) and zero(0) tile to position (i-1, 0)
            pos = self.move(target_row - 1, 1, row, column)
            # use move string for a 3x2 puzzle to bring the target tile into position (i, 0),
            # move tile zero to the right end of row i-1
            pos += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'
            self.update_puzzle(pos)
            move_string += pos

        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return move_string


# phase two methods

    def row0_invariant(self, target_col):
        '''
        check whether the puzzle satisfies the row zero invariant at the given column (col > 1);
        returns a boolean
        '''
        # don’t check for more if zero(0) tile is not in expected column
        if not self.get_number(0, target_col) == 0:
            return False

        for column in range(self.get_width()):
            for row in range(self.get_height()):
                # exclude non-expected tiles and then check if the rest of tiles is solved
                if (row == 0 and column > target_col) or (row == 1 and column >= target_col) or row > 1:
                    if not (row, column) == self.current_position(row, column):
                        return False

        return True


    def row1_invariant(self, target_col):
        '''
        check whether the puzzle satisfies the row one invariant at the given column (col > 1);
        returns a boolean
        '''
        # don’t check for more if  row 1 is not solved
        if not self.lower_row_invariant(1, target_col):
            return False

        # check if all tiles in rows beneath row 1 are positioned at their solved location
        for column in range(0, self.get_width()):
            for row in range(2, self.get_height()):
                if not (row, column) == self.current_position(row, column):
                    return False

        return True


    def solve_row0_tile(self, target_col):
        '''
        solve the tile in row zero at the specified column;
        updates puzzle and returns a move string
        '''
        assert self.row0_invariant(target_col)
        move_string = 'ld'
        self.update_puzzle(move_string)

        # open row and column tile values
        row, column = self.current_position(0, target_col)
        if row == 0 and column == target_col:
            return move_string
        else:
            # target tile at position (1, j-1) and zero tile at position (1, j-2)
            pos = self.move(1, target_col - 1, row, column)
            # use move string for a 2x3 puzzle
            pos += 'urdlurrdluldrruld'
            self.update_puzzle(pos)
            move_string += pos

        # check if assert fails for some reason: assert self.row0_invariant(target_col - 1)
        return move_string


    def solve_row1_tile(self, target_col):
        '''
        solve the tile in row one at the specified column;
        updates puzzle and returns a move string
        '''
        # assert if check fails for some reason: assert self.row1_invariant(target_col)
        # open row and column tile values
        row, column = self.current_position(1, target_col)
        move_string = self.move(1, target_col, row, column)
        move_string += 'ur'

        self.update_puzzle(move_string)
        return move_string


# phase 3 methods

    def solve_2x2(self):
        '''
        solves the upper left 2x2 part of the puzzle;
        updates the puzzle and returns a move string
        '''
        # check if assert fails for some reason: assert self.row1_invariant(1)
        move_string = ''
        init_move = ''

        if self.get_number(1, 1) == 0:
            init_move += 'ul'
            self.update_puzzle(init_move)
            if (0, 1) == self.current_position(0, 1) and (1, 1) == self.current_position(1, 1):
                return init_move

            # pick a move depending on current configuration
            if self.get_number(0, 1) < self.get_number(1, 0):
                move_string += 'rdlu'
            else:
                move_string += 'drul'
            self.update_puzzle(move_string)

        return init_move + move_string


    def solve_puzzle(self):
        '''
        generate a solution string for a puzzle;
        updates the puzzle and returns a move string
        '''
        move_string = ''

        # position zero(0) tile in the right lower corner
        row = self.get_height() - 1
        column = self.get_width() - 1
        # open row and column tile values
        cur_row, cur_column = self.current_position(0, 0)
        # calculate row and column variations
        col_change = cur_column - column
        row_change = cur_row - row
        pos = abs(col_change) * 'r' + abs(row_change) * 'd'
        self.update_puzzle(pos)
        move_string += pos

        # bottom m-2 rows in order from bottom to top and right to left
        for dummy_row in range(row, 1, -1):
            for dummy_col in range(column, 0, -1):
                move_string += self.solve_interior_tile(dummy_row, dummy_col)
            move_string += self.solve_col0_tile(dummy_row)

        # rightmost n-2 columns of the top two rows in a bottom to top and right to left order
        for dummy_col in range(column, 1, -1):
            move_string += self.solve_row1_tile(dummy_col)
            move_string += self.solve_row0_tile(dummy_col)

        # unsolved is upper left 2 by 2 portion
        move_string += self.solve_2x2()
        return move_string


# start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

# Testing

# lower_row_invariant(self, target_row, target_col)
#obj = Puzzle(4, 4, [[8,1,2,3],[9,6,4,7],[5,0,10,11],[12,13,14,15]])
#print obj.lower_row_invariant(2, 1)
#print ""

# solve_interior_tile(self, target_row, target_col)
#obj = Puzzle(4, 4, [[8,1,2,3],[9,6,4,7],[5,0,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_interior_tile(2, 1)
#print ""

#obj = Puzzle(4, 4, [[8,1,2,3],[7,6,4,9],[5,0,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_interior_tile(2, 1)
#print ""

# solve_col0_tile(self, target_row)
#obj = Puzzle(4, 4, [[7,1,2,3],[8,6,4,5],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

#obj = Puzzle(4, 4, [[8,1,2,3],[7,6,4,5],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

#obj = Puzzle(4, 4, [[3,1,2,8],[7,6,4,5],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

#obj = Puzzle(4, 4, [[3,1,2,5],[7,6,4,8],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

# row1_invariant(self, target_col)
#obj = Puzzle(4, 4, [[4,1,2,3],[5,0,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row1_invariant(1)
#print ""

# row1_invariant(self, target_col)
#obj = Puzzle(4, 4, [[4,1,2,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row1_invariant(0)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(4, 4, [[2,1,0,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row0_invariant(2)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(4, 4, [[3,1,2,0],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row0_invariant(3)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(3, 3, [[3, 0, 2], [1, 4, 5], [6, 7, 8]])
#print obj.row0_invariant(1)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(4, 5, [[7, 2, 0, 3, 4], [5, 6, 1, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.row0_invariant(2)
#print ""

# solve_row0_tile(self, target_col)
#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_row0_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_row1_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 4], [2, 1, 0, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_row1_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_row1_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_row1_tile(4)
#print ""

# solve_2x2(self)
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_2x2()
#print ""

# solve_puzzle(self)
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_interior_tile(self, target_row, target_col)
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#print obj.__str__()
#print obj.solve_interior_tile(2, 1)
#print ""

# solve_puzzle(self)
#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_puzzle(self)
#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_puzzle(self)
#obj = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_puzzle(self)
#obj = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""
