###########################################################
# FILE : wordsearch.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex5 2021
# DESCRIPTION:  This program is a word search "game".
###########################################################
import sys
import os.path

POSSIBLE_DIRECTIONS = "durlwxyz"


def read_wordlist(filename):
    """ This function gets a file name and returns a list that contains all
        the words in the file. If there is no words in the file -the function
        returns an empty list. """
    with open(filename, "r") as words_file:
        words = words_file.read()
        if words == "":
            return []

        else:
            words_list = words.split("\n")
            if "" in words_list:
                words_list.remove("")
    return words_list


def read_matrix(filename):
    """ This function gets a file name and returns a list that represents our
        matrix. This list contains lists, in each list there are letters and
        every list is a row in the matrix. If the file is empty- the
        function returns an empty list. """
    with open(filename, "r") as mat_file:
        matrix = []
        mat_data = mat_file.readlines()
        if mat_data == []:
            return matrix
        else:
            for line in mat_data:
                line = line.strip("\n")
                matrix.append(line.split(","))
        return matrix


def make_downwards_list(matrix):
    """ This function gets the matrix and returns a new list that
        contains the columns from the matrix(downwards). """
    down_list = []

    for p in range(len(matrix[0])):
        s = ""
        for i in range(len(matrix)):
            s += matrix[i][p]
        down_list.append(s)
    return down_list


def make_upwards_list(matrix):
    """ This function gets the matrix and returns a new list that contains
        the columns from the matrix(upwards). The function first calls the
        make_downwards_list function in order to get a list that contains
        the columns, then reverse each item in that list and adds it to a
        new list- the up_list. """
    down_list = make_downwards_list(matrix)
    up_list = []
    for i in down_list:
        up_list.append(i[::-1])
    return up_list


def make_right_list(matrix):
    """ This function gets the matrix and returns a new list that contains
        the lines in the matrix (just 'breaks' the sub-lists in the
        original matrix) """
    right_list = []
    for lst in matrix:
        right_list.append("".join(lst))
    return right_list


def make_left_list(matrix):
    """ This function gets the matrix and returns a new list that contains
        the lines from the matrix(reversed). The function first calls the
        make_right_list function in order to get the list of lines,
        then reverse each item in that list and adds it to a new list-
        the left_list. """
    right_list = make_right_list(matrix)
    left_list = []
    for i in right_list:
        left_list.append(i[::-1])
    return left_list


def diagonal_up_right_list(matrix):
    """ This function gets a matrix and returns a list that contains
        strings- each string is a diagonal in the matrix (up right direction).
        First the function creates a new_list- that contains number_of_diagonal
        lists, then to each list the function appends the letters at the same
        diagonal, after that, the function converts that list of lists to a
        simple list of string, each string is a diagonal in the matrix. """
    num_of_diagonals = len(matrix) + len(matrix[0]) - 1
    new_list = [[] for _ in range(num_of_diagonals)]
    for l in range(len(matrix)):
        for i in range(len(matrix[0])):
            new_index = i + l
            new_list[new_index].insert(0, matrix[l][i])

    diagonal_up_right_lst = []
    for lst in new_list:
        diagonal_up_right_lst.append("".join(lst))
    return diagonal_up_right_lst


def diagonal_down_left_list(matrix):
    """ This function gets the matrix and returns a list of strings that
        represent the diagonals in the matrix (down left direction). The
        function first calls the diagonal_up_right_list function in order to
        get the list of the opposite direction and reverse the items in that
        list, adds it to a new list(diagonal_down_left_lst) and returns it. """
    diagonal_up_right_lst = diagonal_up_right_list(matrix)
    diagonal_down_left_lst = []
    for i in diagonal_up_right_lst:
        diagonal_down_left_lst.append(i[::-1])
    return diagonal_down_left_lst


def diagonal_up_left_list(matrix):
    """ This function gets the matrix and returns a list of strings that
        represent the diagonals in the matrix(up left direction). First, this
        function reverse the original matrix, then calls the
        diagonal_up_right_list function with the reversed_matrix in order to
        get the wanted list (does the same action- just on a different matrix)
        """
    reversed_matrix = []
    for i in matrix:
        reversed_matrix.append(i[::-1])

    diagonal_up_left_lst = diagonal_up_right_list(reversed_matrix)
    return diagonal_up_left_lst


def diagonal_down_right_list(matrix):
    """ This function gets the matrix and returns a list of strings that
        represents the diagonals in the matrix(down right direction). The
        function first calls the diagonal_up_left_list function in
        order to get a list of diagonals in that direction then reverse
        the items in that list in order to get the wanted list. """
    diagonal_up_left = diagonal_up_left_list(matrix)
    diagonal_down_right_lst = []
    for i in diagonal_up_left:
        diagonal_down_right_lst.append(i[::-1])
    return diagonal_down_right_lst


def count_words(word, lst):
    """ This function gets a word and a list((which represents the matrix) and
        counts how many times a word appears in the given list. """
    count = 0
    for line in lst:
        for i in range(0, len(line) - len(word) + 1):
            if word in line[i:i + len(word)]:
                count = count + 1
    return count


def check_word(words_list, lst, dict_words):
    """ This function gets a words_list and another list (that represent the
        matrix in the wanted direction) and the current dict_words. The
        function search for each word from the words list in the 'matrix'
        list and counts how many times the word repeats itself in every item of
        the list by calling the count_words function. Then it updates the
        dict_words and Finally, returns it. """

    for word in words_list:
        count = count_words(word, lst)

        if count > 0:
            if word in dict_words:
                dict_words[word] += count
            else:
                dict_words[word] = count

    return dict_words


def write_output(results, filename):
    """ This function gets the list of results and a file name and write to
        the file those results. That is the final results of the search the
        program made. """
    with open(filename, "w") as output_file:
        for tup in results:
            word, count = tup
            output_file.write(word + "," + str(count) + "\n")


def check_duplicate_direction(direction):
    """ This function gets a string- the wanted directions, and check if
        it contains duplicates. If it is- the function returns a new
        string that contains the directions without duplicates and if there
        isn't, the function returns the original direction string. """
    for d in direction:
        if direction.count(d) > 1:
            new_direction = "".join(set(direction))
            return new_direction
    return direction


def find_words(word_list, matrix, direction):
    """ This function gets a word list, a matrix and a direction and returns a
        list of tuples that shows the words from the wordlist that were
        found in the matrix in that direction, and how many times were they
        found. First, the function create the dict_words dictionary. Then it
        calls the check_duplicate_direction function in order to remove
        duplicates from the direction string- if there are any. According to
        the given direction the function calls the wanted function that
        returns a list of strings (that represents the lines in the matrix
        in the wanted direction) and give it to the check_word function (
        along with the word-list and the dict_words). By doing that the
        dict_words is updated and in the end the function converts it to a
        list of tuples and returns it. If the word list or matrix are empty
        the function returns an empty list. """

    if word_list == [] or matrix == []:
        return []

    dict_words = {}
    directions = check_duplicate_direction(direction)

    for d in directions:
        if d == "d":
            check_word(word_list, make_downwards_list(matrix), dict_words)
        elif d == "u":
            check_word(word_list, make_upwards_list(matrix), dict_words)
        elif d == "r":
            check_word(word_list, make_right_list(matrix), dict_words)
        elif d == "l":
            check_word(word_list, make_left_list(matrix), dict_words)
        elif d == "w":
            check_word(word_list, diagonal_up_right_list(matrix), dict_words)
        elif d == "x":
            check_word(word_list, diagonal_up_left_list(matrix), dict_words)
        elif d == "y":
            check_word(word_list, diagonal_down_right_list(matrix), dict_words)
        elif d == "z":
            check_word(word_list, diagonal_down_left_list(matrix), dict_words)
    list_of_tuples = [(k, v) for k, v in dict_words.items()]
    return list_of_tuples


def check_valid_input(args):
    """ This function gets a list of the input arguments (without the path
        to this file- so args[0] represents the word file, args[1]
        represents the matrix file, args[2] represents the output file and
        args[3] represents the directions) and checks if they are valid.
        The function returns False and an informative message if they are
        not and True if they are. The input will be considered not valid if
        one of this options are True:
        - If the user typed in more then 4 arguments
        - If the input files doesnt exist.
        - If the directions are not valid- not d/u/r/l/w/x/y/z """

    if len(args) != 4:
        print("You typed in more then 4 arguments!")
        return False

    elif not os.path.exists(args[0]) or not os.path.exists(args[1]):
        if not os.path.exists(args[1]) and os.path.exists(args[0]):
            print("The matrix file not exist!")
        else:
            print("Word file does not exist!")
        return False

    else:
        for i in args[3]:
            if i not in POSSIBLE_DIRECTIONS:
                print("Directions are not valid!")
                return False
    return True


def main():
    """ This is the main functions that calls all the other functions and
        start the search for words. First it saves the argument in
        variables. Then the function checks if the input arguments
        are valid (by calling the check_valid_input function), if they are-
        the function calls the find_words function to search for words,
        then calls the write_output function to write the results to the
        output file. If the input arguments are not valid- the program
        finishes to run."""

    arguments = sys.argv
    word_file = arguments[1]
    matrix_file = arguments[2]
    output_file = arguments[3]
    directions = arguments[4]

    if check_valid_input(arguments[1:]) is True:
        results = find_words(read_wordlist(word_file),
                             read_matrix(matrix_file),
                             directions)
        write_output(results, output_file)


if __name__ == "__main__":
    """ Here we call the main function. """
    main()
