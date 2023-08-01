###################################################################
# FILE : game.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex9 2021
# DESCRIPTION: This program contains the game class and runs the
#              game rush hour.
###################################################################

from board import Board
from car import Car
import helper
import sys

# Constant variables
POSSIBLE_NAMES = ["R", "G", "W", "O", "B", "Y"]
POSSIBLE_LENGTH = [2, 3, 4]
VERTICAL = 0
HORIZONTAL = 1
POSSIBLE_ORIENTATION = [0, 1]
MOVE_UP = "u"
MOVE_DOWN = "d"
MOVE_RIGHT = "r"
MOVE_LEFT = "l"
POSSIBLE_MOVES = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]


class Game:
    """
    This class creates a game object. This class is familiar with board
    objects which has cars objects on it. When the game is played it waits
    for input from the user, checks if it is valid and updates the board (by
    moving the cars on it) the game is over when the user presses '!' or some
    car got to the target point.
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board
        self.__cars = []
        self.__cars = [board.cell_content(cell) for cell in board.cell_list()
                       if board.cell_content(cell) is not None if
                       board.cell_content(cell) not in self.__cars]

    def check_input(self, input_lst):
        """ This function checks if the user input is valid, if it is-
        returns True, if it isn't returns False. It will return False if:
        - Got more then two characters (not including the ','.
        - Got unknown movekey.
        - Trying to move a car that wasn't added to the game.
        - Got invalid movekey according to the car possible moves."""

        if len(input_lst) != 2:
            return False
        if input_lst[1] not in POSSIBLE_MOVES:
            return False
        if input_lst[0] not in self.__cars:
            return False

        for tup in self.__board.possible_moves():
            if input_lst[0] in tup:
                if input_lst[1] in tup:
                    return True
        return False

    def __check_if_won(self):
        """ This function checks if there is a winning car- a car in the
            target location in the board."""
        if self.__board.cell_content(self.__board.target_location()) is not None:
            print(self.__board.cell_content(self.__board.target_location()), "won!")
            return True
        return False

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what
                direction to move it. If the user wants to end the game he
                has to type '!', and if he wants to see the possible moves
                in the board he can type '?'.

            2. Check if the input is valid. by calling the check_input
                function.

            3. Try moving car according to user's input.
        if something is invalid the function prints a message to the screen
        and waits for another input.
        """
        user_input = input("Enter the name of the car and the wanted "
                           "direction ,! to finish the game or ? for "
                           "possible moves: ")
        # To end the game
        if user_input == "!":
            return True
        # To get 'hints'
        elif user_input == "?":
            for tup in self.__board.possible_moves():
                print(tup)
            return False
        else:
            # To move a car
            input_lst = user_input.split(",")
            if self.check_input(input_lst) is False:
                print("invalid input!")
                return False
            else:
                if not self.__board.move_car(input_lst[0], input_lst[1]):
                    print("cant move the car like that!")
                return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        until the end flag is not True the game keeps running. The flag will
        be True when there will be some car on the target location or the user
        pressed '!' .
        :return: None
        """
        end = False
        while not end:
            if len(self.__cars) == 0:  # __cars_lst
                break
            if self.__check_if_won():
                break
            end = self.__single_turn()
            print(self.__board)


def check_valid_car(car_name, length, location, orientation):
    """ This function checks if the car has valid properties and can be
        added to the game. It checks the name, the length, the location and
        the orientation. If it found something not valid returns False,
        else True."""

    if car_name not in POSSIBLE_NAMES:
        return False
    elif length not in POSSIBLE_LENGTH:
        return False
    elif location not in board1.cell_list():
        return False
    elif orientation not in POSSIBLE_ORIENTATION:
        return False

    return True


if __name__ == "__main__":
    """ First the program reads the JSON file using sys.argv and the 
        load_json function from helper. Then creates a board object, 
        and adds valid cars to it (using the check_valid_car function). The 
        program prints a message- which cars can't be added to the game. 
        Then creates game object and calls the play method in order to start 
        playing. In the end print Game over."""

    # Get the json file
    arguments = sys.argv
    json_file = arguments[1]
    dict_cars = helper.load_json(json_file)

    # Create a board object and adds cars on it
    board1 = Board()
    car_lst = []
    for name, settings in dict_cars.items():
        car = Car(name, settings[0], tuple(settings[1]), settings[2])
        if check_valid_car(name, settings[0], tuple(settings[1]), settings[2]):
            if board1.add_car(car) is False:
                print("couldn't add car ", car.get_name())
            else:
                car_lst.append(name)

        else:
            print("couldn't add car ", car.get_name())

    # Print the board, create and starts a game
    print(board1)
    new_game = Game(board1)
    new_game.play()
    print("Game over")
