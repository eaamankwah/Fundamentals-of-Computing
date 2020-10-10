"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 'obstacle'
HUMAN = 'human'
ZOMBIE = 'zombie'


class Zombie(Grid): # for grader add poc_grid.
    '''
    class for simulating zombie pursuit of human on grid with obstacles
    '''

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        '''
        create a simulation of given size with given obstacles, humans, and zombies
        '''
        Grid.__init__(self, grid_height, grid_width)    # for grader add poc_grid.
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            # obstacle list was missing! (perhaps intentionally?)
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        '''
        set cells in obstacle grid to be empty,
        reset zombie and human lists to be empty
        '''
        self._zombie_list = []
        self._human_list = []
        Grid.clear(self)    # for grader add poc_grid.

    def add_zombie(self, row, col):
        '''
        add a zombie to the zombie list
        '''
        self._zombie_list.append((row, col))

    def num_zombies(self):
        '''
        return current number of zombies
        '''
        return len(self._zombie_list)

    def zombies(self):
        '''
        generator that yields the zombies in the order they were added
        '''
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        '''
        add human to the human list
        '''
        self._human_list.append((row, col))

    def num_humans(self):
        '''
        return current number of humans
        '''
        return len(self._human_list)

    def humans(self):
        '''
        generator that yields the humans in the order they were added
        '''
        for human in self._human_list:
            yield human

    def obstacle(self):
        '''
        generator that yields the list of obstacles
        '''
        for obstacle in self._obstacle_list:
            yield obstacle

    def compute_distance_field(self, entity_type):
        '''
        function computes a 2D distance field, distance at member of entity_queue is zero;
        shortest paths avoid obstacles and use distance_type distances
        '''
        # same size as the grid and initialized with artifically high values
        distance_field =[[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                         for dummy_row in range(self._grid_height)]

        # grid visited initialized as to be empty
        visited = Grid(self._grid_height, self._grid_width) # for grader add poc_grid.
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])

        # creates a copy of the human/zombie list
        boundary = Queue()    # for grader add poc_queue.
        if entity_type == ZOMBIE:
            list_type = self._zombie_list
        elif entity_type == HUMAN:
            list_type = self._human_list

        # check whether the cell is passable and update the neighbor's distance
        for item in list_type:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0

        # breadth-first search
        while boundary:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])
            for resident in neighbors:
                if visited.is_empty(resident[0], resident[1]):
                    distance_field[resident[0]][resident[1]] = min(distance_field[resident[0]][resident[1]],
                                                                   distance_field[cell[0]][cell[1]] + 1)
                    visited.set_full(resident[0], resident[1])
                    boundary.enqueue(resident)

        return distance_field

    def move_humans(self, zombie_distance):
        '''
        function that moves humans away from zombies, diagonal moves are allowed,
        returns noting
        '''
        temp_human_list = []
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            # store current position
            distance = [zombie_distance[human[0]][human[1]]]
            location = [human]

            for resident in neighbors:
                if self.is_empty(resident[0], resident[1]):
                    # and store rest of 8 other positions if not occupied
                    distance.append(zombie_distance[resident[0]][resident[1]])
                    location.append(resident)
            # find the current safest location, move there
            safest = location[distance.index(max(distance))]
            self.set_empty(human[0], human[1])
            temp_human_list.append(safest)

        self._human_list = temp_human_list


    def move_zombies(self, human_distance):
        '''
        function that moves zombies towards humans, diagonal moves are NOT allowed,
        returns nothing
        '''
        temp_zombie_list = []
        #for zombie in self.zombies():
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            # store current position
            distance = [human_distance[zombie[0]][zombie[1]]]
            location = [zombie]

            for resident in neighbors:
                if self.is_empty(resident[0], resident[1]):
                    # and store rest of 4 other positions if not occupied
                    distance.append(human_distance[resident[0]][resident[1]])
                    location.append(resident)
            # find the current most closest location, move there
            closest = location[distance.index(min(distance))]
            self.set_empty(zombie[0], zombie[1])
            temp_zombie_list.append(closest)

        self._zombie_list = temp_zombie_list


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))