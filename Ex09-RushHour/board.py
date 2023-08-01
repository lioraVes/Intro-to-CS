###################################################################
# FILE : board.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex9 2021
# DESCRIPTION: This program contains the board class for the
#              game rush hour.
###################################################################
# Constant variables

VERTICAL = 0
HORIZONTAL = 1

MOVE_UP = "u"
MOVE_DOWN = "d"
MOVE_RIGHT = "r"
MOVE_LEFT = "l"


class Board:
    """
    This class creates a board the size of (7*7) and a target location-(3,
    7). Cars can be added to the board and can be moved on it as long as they
    are not moving out of the borders of the board (or on other cars).
    """
    # Class Constants
    LENGTH_BOARD = 7
    MIDDLE_ROW = 3

    def __init__(self):
        """ creates an initial board list, a dictionary of the cars that are
            added to the board, and a dictionary that holds the information
            about the cars and their possible moves directions. """

        self.__board_lst = []
        for row in range(self.LENGTH_BOARD):
            temp_row_lst = []
            for col in range(self.LENGTH_BOARD):
                temp_row_lst.append("_")
                if row == self.MIDDLE_ROW and col == self.LENGTH_BOARD - 1:
                    temp_row_lst.append("_")

            self.__board_lst.append(temp_row_lst)

        self.__car_dict = {}
        self.__car_orientation = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        final_str = ""
        for row in range(len(self.__board_lst)):
            for col in range(len(self.__board_lst[row])):
                if row == self.LENGTH_BOARD - 1 and col == self.LENGTH_BOARD \
                        - 1:
                    final_str += self.__board_lst[row][col]
                elif col == self.LENGTH_BOARD:
                    final_str += self.__board_lst[row][col] + "\n"
                elif col == self.LENGTH_BOARD - 1 and row != self.MIDDLE_ROW:
                    final_str += self.__board_lst[row][col] + "\n"
                else:
                    final_str += self.__board_lst[row][col] + " "
        return final_str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board.
        :return: list of coordinates
        """
        coord_lst = [(row, col) for row in range(len(self.__board_lst)) for
                     col in range(len(self.__board_lst[row]))]

        return coord_lst

    def __check_direction_vertical(self, direction_dict, top_point,
                                   bottom_point):
        """ A helper function for check_directions. This function checks for
            vertical cars, if they can move up and down in the board. The
            function checks if the next move will be out of the borders
            of the board or taken by other cars, and returns a list with the
            valid directions. """
        direction_dict[MOVE_RIGHT] = False
        direction_dict[MOVE_LEFT] = False
        if top_point[0] == 0 or self.cell_content((top_point[0] - 1,
                                                   top_point[1])) is not None:
            direction_dict[MOVE_UP] = False
        if bottom_point[0] == self.target_location()[1] - 1 or \
                self.cell_content((bottom_point[0] + 1, bottom_point[1])) \
                is not None:
            direction_dict[MOVE_DOWN] = False

        pos_direction = [direction for direction, bools in
                         direction_dict.items() if bools]
        return pos_direction

    def __check_direction_horizontal(self, direction_dict, top_point,
                                     bottom_point):
        """ A helper function for check_directions. This function checks for
            horizontal cars, if they can move right and left in the board. The
            function checks if the next move will be out of the borders
            of the board or taken by other cars, and returns a list with the
            valid directions """

        direction_dict[MOVE_UP] = False
        direction_dict[MOVE_DOWN] = False

        if top_point[1] == 0 or self.cell_content((top_point[0],
                                                   top_point[1] - 1)) \
                is not None:
            direction_dict[MOVE_LEFT] = False
        if bottom_point == self.target_location() or bottom_point[1] == \
                self.target_location()[1] - 1 or \
                self.cell_content((bottom_point[0], bottom_point[1] + 1)) \
                is not None:
            if bottom_point != (self.target_location()[0],
                                self.target_location()[1] - 1):
                direction_dict[MOVE_RIGHT] = False

        pos_direction = [direction for direction, bools in
                         direction_dict.items() if bools]
        return pos_direction

    def __check_directions(self, orientation, car):
        """ This function checks which direction can the car move. It gets
            the name of the car and its orientation as parameters and returns a
            list of possible directions. The function calls the
            check_direction_vertical and check_direction_horizontal
            functions to check which directions are valid. The function
            returns a list with the valid directions. """

        top_point = min(self.__car_dict[car])
        bottom_point = max(self.__car_dict[car])

        direction_dict = {MOVE_UP: True, MOVE_DOWN: True, MOVE_RIGHT: True,
                          MOVE_LEFT: True}

        if orientation == VERTICAL:
            return self.__check_direction_vertical(direction_dict,
                                                   top_point, bottom_point)

        elif orientation == HORIZONTAL:
            return self.__check_direction_horizontal(direction_dict, top_point,
                                                     bottom_point)

        return []

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board. It
            calls the check_directions function in order to 'filter' the
            possible directions.
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves.
        """
        res_lst = []
        for car, orientation in self.__car_orientation.items():
            direction_lst = self.__check_directions(orientation, car)

            for direction in direction_lst:
                description = str(car) + " can move " + str(direction)
                res_lst.append((car, direction, description))

        return res_lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
         filled for victory. In this board, returns (3,7).
        :return: (row,col) of goal location.
        """
        return self.MIDDLE_ROW, self.LENGTH_BOARD

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if self.__board_lst[coordinate[0]][coordinate[1]] == "_":
            return None
        else:
            return self.__board_lst[coordinate[0]][coordinate[1]]

    def __check_valid_car(self, car, coords):
        """ This function checks if the car can be added to the game. The
            function will not add a car if:
            - There is already a car in the same name. (prints a message-
              already in)
            - Couldn't get the orientation of the car object. (coords will
                be empty list)
            - The coordinates of the car are out of the board.
            - There is another car in the wanted coordinates already."""

        if car.get_name() in self.__car_dict:
            print(car.get_name(), "already in")
            return False

        if not coords:
            print(car.get_name(), "orientation is not known")
            return False

        for i in coords:
            if i not in self.cell_list():
                print(car.get_name(), "coordinates out of board")
                return False

        for i in coords:
            if self.cell_content(i) is not None:
                print(car.get_name(), "coordinates are taken")
                return False

    def add_car(self, car):
        """
        This function adds car to the board(or not).It calls the
        check_valid_car function in order to check if the car can be added
        to the board. this function also adds the name of the car and its
        coordinates to the car_dict and the name of the car and its
        orientation to the car_orientation dictionary.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        coords = car.car_coordinates()

        if self.__check_valid_car(car, coords) is False:
            return False

        for i in range(len(coords)):
            self.__board_lst[coords[i][0]][coords[i][1]] = car.get_name()

        self.__car_dict[car.get_name()] = coords

        for direction in car.possible_moves().keys():
            if direction == MOVE_UP or direction == MOVE_DOWN:
                self.__car_orientation[car.get_name()] = VERTICAL
            elif direction == MOVE_RIGHT or direction == MOVE_LEFT:
                self.__car_orientation[car.get_name()] = HORIZONTAL

        return True

    def __check_valid_move(self, name, movekey):
        """ This function checks if the wanted move is valid according to
            the car orientation."""
        moves_lst = self.possible_moves()
        for i in range(len(moves_lst)):
            if name in moves_lst[i]:
                if movekey in moves_lst[i]:
                    return True
        return False

    def __move_car_helper(self, movekey, new_coord, coords, name):
        """ A helper function for move_car. This function updates the
            coordinates of the car according to the movekey, updates the board
            list and the car_dict. if the new coordinate not valid(not in
            the cell_list it return False."""

        if new_coord not in self.cell_list():
            return False

        if movekey == MOVE_UP or movekey == MOVE_LEFT:
            coords.insert(0, new_coord)
            row, col = coords.pop()
            self.__board_lst[row][col] = "_"
            self.__car_dict[name] = coords

        elif movekey == MOVE_DOWN or movekey == MOVE_RIGHT:
            coords.insert(len(coords), new_coord)
            row, col = coords.pop(0)
            self.__board_lst[row][col] = "_"
            self.__car_dict[name] = coords
        return True

    def move_car(self, name, movekey):
        """
            moves car one step in given direction. Calls the
            check_valid_move function in order to see if the move is valid,
            then calls the move_car_helper function to update the car
            coordinates(or not). Finally the function updates the board
            according to the new coordinates.
            :param name: name of the car to move
            :param movekey: Key of move in car to activate
            :return: True upon success, False otherwise
            """

        if self.__check_valid_move(name, movekey) is False:
            return False

        coords = self.__car_dict[name]

        if movekey == MOVE_UP:
            new_coord = coords[0][0] - 1, coords[0][1]
            if not self.__move_car_helper(MOVE_UP, new_coord, coords, name):
                return False

        elif movekey == MOVE_DOWN:
            new_coord = coords[-1][0] + 1, coords[-1][1]
            if not self.__move_car_helper(MOVE_DOWN, new_coord, coords, name):
                return False

        elif movekey == MOVE_RIGHT:
            new_coord = coords[-1][0], coords[-1][1] + 1
            if not self.__move_car_helper(MOVE_RIGHT, new_coord, coords, name):
                return False

        elif movekey == MOVE_LEFT:
            new_coord = coords[0][0], coords[0][1] - 1
            if not self.__move_car_helper(MOVE_LEFT, new_coord, coords, name):
                return False

        # updates the board
        for car, coords in self.__car_dict.items():
            for coor in range(len(coords)):
                self.__board_lst[coords[coor][0]][coords[coor][1]] = car

        return True
