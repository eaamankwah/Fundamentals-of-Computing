"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def slide(line):
    """
    Slide the values in the line list such that no zero numbers appears in
    between non zero numbers and return the result list
    """
    result = [0] * len(line)
    for current in line:
        if (current != 0):
            for index in range(len(result)):
                value = result[index]
                if (value == 0):
                    result[index] = current
                    break
    return result

def combined(line):
    """
    Combine and return the numbers in the line list.
    """
    for index in range(len(line)-1):
        if (line[index] == line[index+1]):
            line[index] += line[index+1]
            line[index+1] = 0
    return line


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    slided= slide(line)
    all_combined = combined(slided)
    result= slide(all_combined)
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Initialize class
        """
        self.grid_height = grid_height
        self.grid_width = grid_width
        self._grid = [[0]*self.grid_width for row in range(self.grid_height)]
        self.reset()
        # computing method to make move go cleaner
        up_list = [(0, col) for col in range(self.grid_width)]
        down_list = [(self.grid_height-1, col) for col in range(self.grid_width)]
        left_list = [(row, 0) for row in range(self.grid_height)]
        right_list = [(row, self.grid_width-1) for row in range(self.grid_height)]
        self._move_dict = {UP:up_list, DOWN:down_list, LEFT:left_list, RIGHT:right_list}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                self._grid[row][col] = 0
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        output = ''
        for row in self._grid:
            for entry in row:
                output += str(entry) + '\t'
            output += '\n'
        return output

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        direction_tiles = self._move_dict[direction]
        #print direction_tiles
        offset = list(OFFSETS[direction])

        times = 0
        if (direction == 1 or direction == 2):
            times = self.grid_height
        elif (direction == 3 or direction == 4):
            times = self.grid_width

        for current_tile in direction_tiles:
            tile = list(current_tile)
            temporary_list = []
            temporary_list.append(self.get_tile(tile[0], tile[1]))
            for dummy in range(times-1):
                tile[0] += offset[0]
                tile[1] += offset[1]
                temporary_list.append(self.get_tile(tile[0], tile[1]))
            result = merge(temporary_list)
            tile = list(current_tile)
            self.set_tile(tile[0], tile[1], result[0])
            for index in range(1, times):
                tile[0] += offset[0]
                tile[1] += offset[1]
                self.set_tile(tile[0], tile[1], result[index])

        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #randomly select an empty square
        selected = False
        count = self.grid_width * self.grid_height
        while (selected != True and count != 0):
            row = random.randint(0, self.grid_height-1)
            col = random.randint(0, self.grid_width-1)
            if self.get_tile(row, col) == 0:
                selected = True
            if (selected == True):
                likely_number = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
                tile = random.choice(likely_number)
                self.set_tile(row, col, tile)
            count -= 1

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        #print row, col
        return self._grid[row][col]

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
