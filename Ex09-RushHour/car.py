###################################################################
# FILE : car.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex9 2021
# DESCRIPTION: This program contains the car class for the
#              game rush hour.
###################################################################
# Constant variables
VERTICAL = 0
HORIZONTAL = 1

MOVE_UP = "u"
MOVE_DOWN = "d"
MOVE_RIGHT = "r"
MOVE_LEFT = "l"


class Car:
    """
    This class creates car objects. Each car has its own name, length,
    location and orientation.
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object.
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
                         location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """

        self.__name = name

        self.__length = length

        self.__location = location

        if orientation == VERTICAL:
            self.__orientation = VERTICAL

        elif orientation == HORIZONTAL:
            self.__orientation = HORIZONTAL
        else:
            self.__orientation = -1

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coor_list = [self.__location]

        if self.__orientation == VERTICAL:
            for n in range(1, self.__length):
                new_cor = (self.__location[0] + n, self.__location[1])
                coor_list.append(new_cor)

        elif self.__orientation == HORIZONTAL:
            for n in range(1, self.__length):
                new_cor = (self.__location[0], self.__location[1] + n)
                coor_list.append(new_cor)
        else:
            return []

        return coor_list

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
                 permitted by this car.
        """
        if self.__orientation == VERTICAL:
            dict_vertical = {MOVE_UP: "cause the car drive upwards",
                             MOVE_DOWN: "cause the car drive downwards"}
            return dict_vertical

        elif self.__orientation == HORIZONTAL:
            dict_horizontal = {MOVE_RIGHT: "cause the car drive to the right",
                               MOVE_LEFT: "cause the car drive left"}
            return dict_horizontal
        else:
            return {}

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
                 move to be legal.
        """
        if self.__orientation == VERTICAL:
            if movekey == MOVE_UP:
                return [(self.__location[0] - 1, self.__location[1])]

            elif movekey == MOVE_DOWN:
                return [
                    (self.__location[0] + self.__length, self.__location[1])]
            else:
                return []
        elif self.__orientation == HORIZONTAL:
            if movekey == MOVE_LEFT:
                return [(self.__location[0], self.__location[1] - 1)]
            elif movekey == MOVE_RIGHT:
                return [
                    (self.__location[0], self.__location[1] + self.__length)]
            else:
                return []
        else:
            return []

    def __check_valid_move(self, movekey):
        """ This method checks if the wanted move is valid-  if the movekey is
            not ok according to the car orientation the function returns False.
            Otherwise, return True """

        if movekey not in self.possible_moves().keys():
            return False
        else:
            return True

    def move(self, movekey):
        """
        This function changes the location of the car according to the
        movekey(if its valid). It calls the check_valid_move method to check
        if the move is valid.
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        next_cell = self.movement_requirements(movekey)

        if not self.__check_valid_move(movekey):
            return False

        else:
            if movekey == MOVE_UP:
                self.__location = next_cell[0]
            elif movekey == MOVE_DOWN:
                self.__location = (self.__location[0] + 1, self.__location[1])
            elif movekey == MOVE_RIGHT:
                self.__location = (self.__location[0], self.__location[1] + 1)
            elif movekey == MOVE_LEFT:
                self.__location = next_cell[0]

            return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
