#########################################################
# FILE : nonogram.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex8 2021
# DESCRIPTION: This program simulates the nonogram game.
#########################################################
import copy


def remove_list_insides(input_lst):
    """ This function gets a list that contains sublists inside a sublists,
        and 'cleans' it so in the end we get a list of lists. """
    final_lst = []
    for i in input_lst:
        temp = []
        for j in i:
            temp += j
        final_lst.append(temp)

    return final_lst


def make_first_list(blocks):
    """ This functions create the basic list that contains the blocks in
        form of ones, separated by zeros (except for the last number)"""
    lst_const = []
    for i in blocks:
        add_ones = [1] * i
        lst_const.append(add_ones)
        if not len(lst_const) == len(blocks) + len(blocks) - 1:
            lst_const.append([0])
    return lst_const


def rec_const_sat(n, lst_possible, free_spaces, ind, final_lst, init_length):
    """ This recursive function returns the list of all the possible
        combinations. Each 'iteration' it subtracts one from the ind variable.
        The function starts with a list of the basic placements of ones
        according to the blocks and zeros at the end. Each time the function
        checks if the item before the current item contains ones- if it is
        the function moves the zero in front of the one item and deletes the
        old zero, then adding the new list to the final list each time, until
        the ind is 0 and the last item in the list contains 1's- that's how we
        know we moved all the zeros."""
    if ind <= 0:
        if 1 not in lst_possible[-1]:
            rec_const_sat(n, lst_possible, free_spaces, len(lst_possible) - 1,
                          final_lst, init_length)
        return final_lst

    if 1 in lst_possible[ind - 1]:
        lst_possible.insert(ind - 1, lst_possible[ind])
        del lst_possible[ind + 1]

        if lst_possible not in final_lst:
            final_lst.append(copy.deepcopy(lst_possible))
        rec_const_sat(n, lst_possible, free_spaces, ind - 1, final_lst,
                      init_length)
    else:
        rec_const_sat(n, lst_possible, free_spaces, ind - 1, final_lst,
                      init_length)

    return final_lst


def constraint_satisfactions(n, blocks):
    """ This function gets a number that represent the length of a row and a
        list of 'blocks' that contains the constrains of the row. The
        function returns a list with all the possible combinations. First
        it checks if there is even a possible solution- if not returns an
        empty list, if the blocks list is empty there is only one solution-
        list of zeros. In any other case the function, creates a basic list by
        calling the make_first_list function, then calculates the number of
        'free spaces' there is in the row. If there is zero there is only one
        solution - the basic list we created. If there is more then 0 free
        spaces the function calls the rec_const_set function. In the end the
        function calls the remove_list_insides function in order to 'clean'
        the final list from all the sublists inside. """
    if sum(blocks) + len(blocks) - 1 > n:
        return []

    elif not blocks:
        return [[0] * n]

    else:
        lst_const = make_first_list(blocks)
        free_spaces = n - sum(blocks) - (len(blocks) - 1)

        if free_spaces == 0:
            final_lst = []
            for i in lst_const:
                final_lst += i
            return [final_lst]

        else:
            for i in range(free_spaces):
                lst_const.append([0])  # add zeros to the end of the list

            final_lst = [copy.deepcopy(lst_const)]
            res = rec_const_sat(n, lst_const, free_spaces, len(lst_const) - 1,
                                final_lst, len(lst_const))
            return remove_list_insides(res)


def check_if_fine(row, block):
    """ This function gets a row_list and a block list and counts the
        number of consistent (followed by each other) 1's. In the end it
        gets a list and it compares it to the block_list. If both the list
        are the same- it means the row list is fine and returns True. And if
        not- it returns False."""
    counter_list = []
    counter_one = 0
    for i in range(len(row)):
        if row[i] == 1:
            counter_one += 1
            if not i == len(row) - 1:
                continue
        if counter_one > 0:
            counter_list.append(counter_one)
            counter_one = 0
    if counter_list == block:
        return True
    else:
        return False


def rec_row_variation(row, block, final_lst, i):
    """ This function returns a list of all the possible combinations of
        coloring. Each 'iteration', the function goes over the indexes of
        the row list, until it finds a '-1'. Then it tries to put 1 instead
        of the -1  and call itself again(and after that it tries to put 0
        instead of the -1 and then again calls itself recursively) until it
        gets to the end of the row. Then it checks it the current list that was
        created is fine by calling the check_if_fine function and if it is- it
        appends it to the final list and returns it back. """
    if i >= len(row):
        if check_if_fine(row, block):
            final_lst.append(copy.deepcopy(row))
        return final_lst

    if row[i] == -1:
        row[i] = 1
        rec_row_variation(row[:], block, final_lst, i + 1)
        row[i] = 0
        rec_row_variation(row[:], block, final_lst, i + 1)
    else:
        rec_row_variation(row, block, final_lst, i + 1)
    return final_lst


def row_variations(row, blocks):
    """ This function gets a row list and a block list and by calling the
        rec_row_variation function it returns a list of all the possible
        coloring. If there is no solution (or the function recognizes that
        there is no possible combinations) it returns an empty list."""
    white = row.count(0)
    if len(row) - white < sum(blocks):  # not possible
        return []
    else:
        return rec_row_variation(row[:], blocks, [], 0)


def intersection_row(rows):
    """ This function gets a list of rows and checks for all the same
        indexes in all the lists if they are equal- if they are, the function
        add to the new_list the number they equal to and if not it adds -1. """
    new_list = []
    if len(rows) == 1:
        return rows[0]
    else:
        for j in range(len(rows[0])):
            temp_list = []
            for i in range(len(rows)):
                temp_list.append(rows[i][j])

            if temp_list.count(0) > 0 and temp_list.count(1) > 0:  # both 0 1
                new_list.append(-1)
            elif temp_list.count(0) > 0:  # zero dominate
                new_list.append(0)
            elif temp_list.count(1) > 0:  # one dominates
                new_list.append(1)
            elif temp_list.count(-1) > 0:  # -1
                new_list.append(-1)

        return new_list


def matrix_update_col(matrix, col, ind):
    """ This function updates the matrix according to the new values in the
        given column """
    for c in range(len(col)):
        matrix[c][ind] = col[c]
    return matrix


def must_be_colored_rows(matrix, rows):
    """ This function 'colors' the blocks that must be 'colored'. First,
        the function checks if there is even a need to update the row (if it
        isn't full already) by looking for any neutrals in it (-1). By calling
        the row_variations and intersection_row functions- it looks for an
        intersection between all the variations that are possible in the
        current state of the matrix. Then the function updates the matrix if
        there is need to. Finally, returns the matrix """
    for i in range(len(rows)):
        if -1 not in matrix[i]:
            if check_if_fine(matrix[i], rows[i]):
                continue
            else:
                return None
        else:
            new_row = intersection_row(row_variations(matrix[i], rows[i]))
            if matrix[i] != new_row:
                matrix[i] = new_row
    return matrix


def must_be_colored_cols(matrix, cols):
    """ This function 'colors' the blocks that must be 'colored'. This
        function builds a new list that represent the column values, then it
        checks if there is even a need to update the row (if it isn't full
        already) by looking for any neutrals in it (-1). By calling the
        row_variations and intersection_row functions- it looks for an
        intersection between all the variations that are possible in the
        current state of the matrix. Then the function updates the matrix if
        there is need to by calling the matrix_update_col function. Finally,
        returns the matrix """
    for i in range(len(cols)):
        col_list = []
        for k in range(len(matrix)):
            col_list.append(matrix[k][i])
        if -1 not in col_list:
            if check_if_fine(col_list, cols[i]):
                continue
            else:
                return None
        else:
            col_val = intersection_row(row_variations(col_list, cols[i]))
            if col_val != col_list:
                matrix = matrix_update_col(matrix, col_val, i)

    return matrix


def make_matrix(rows, cols):
    """ This function creates the initial matrix at the size of the
        length of the two items in the constrains list (n*m), with -1 in all
        the matrix."""
    matrix = []
    for j in range(cols):
        row_lst = []
        for i in range(rows):
            row_lst.append(-1)
        matrix.append(row_lst)
    return matrix


def helper_solver_easy(matrix, rows, columns):
    """ This function colors the matrix by only coloring the blocks that
        must be colored. It calls the must_be_colored_rows and cols functions
        until there is no further solution- nothing changes in the matrix
        (it knows it by checking the not_done 'flag'). """

    old_matrix = []
    not_done = True
    while not_done:
        matrix = must_be_colored_rows(matrix, rows)
        if matrix is None:
            return None
        matrix = must_be_colored_cols(matrix, columns)
        if matrix is None:
            return None
        if old_matrix != matrix:
            old_matrix = matrix[:]
            continue
        else:
            not_done = False
    return matrix


def solve_easy_nonogram(constraints):
    """ This function gets constrains list and returns the most solved
        matrix that can be only by 'concluding' from the constrains. The
        function first initializes the matrix it will work on (full of -1),
        then calls and returns the helper_solver_easy function that returns
        the solved matrix."""
    n_rows = len(constraints[1])
    n_columns = len(constraints[0])

    matrix = make_matrix(n_rows, n_columns)
    rows = constraints[0]
    columns = constraints[1]

    return helper_solver_easy(matrix, rows, columns)


def rec_solve_nonogram(constraints, matrix, final_res_lst, ind):
    """ This recursive function gets constraints, matrix, a list which will
        contain the possible results to the game, and an index- which makes the
        function go over the matrix. The function looks for -1 in the
        current position (the index) it is in the matrix. If it isn't -1 the
        function will continue to the next index, until it gets to the last
        one- that means it finished its job, the whole matrix should be
        full and it adds it to the final_res_lst if it isn't there already.
        If the index is -1 the function changes it to 1 first, then updates the
        matrix as much as possible by calling the helper_solver_easy function
        and if it isn't none- continues and calls itself recursively and
        adds one to index. Then tries to do the same with 0 and
        and in the end changes it back to -1 (so the process could continue)"""

    if ind == len(constraints[0]) * len(constraints[1]):
        if matrix not in final_res_lst and matrix is not None:
            final_res_lst.append(matrix)
        return final_res_lst

    row, col = ind // len(matrix[0]), ind % len(matrix[0])

    if matrix[row][col] != -1:
        rec_solve_nonogram(constraints, matrix, final_res_lst, ind + 1)
        return final_res_lst

    # Try to put 1
    matrix[row][col] = 1
    new_matrix = copy.deepcopy(matrix)
    new_matrix = helper_solver_easy(new_matrix, constraints[0], constraints[1])
    if new_matrix is not None:
        rec_solve_nonogram(constraints, new_matrix, final_res_lst, ind + 1)

    # Try to put 0
    matrix[row][col] = 0
    another_new_matrix = matrix[:]
    another_new_matrix = helper_solver_easy(another_new_matrix, constraints[0],
                                            constraints[1])
    if another_new_matrix is not None:
        rec_solve_nonogram(constraints, another_new_matrix, final_res_lst,
                           ind + 1)
    # Put -1 back
    matrix[row][col] = -1

    return final_res_lst


def solve_nonogram(constraints):
    """ This function gets a list of constraints and returns a list of all
        the possible solutions to that nonogram game. The function first
        calls the solve_easy_nonogram function in order to get the most
        solved matrix by only concluding, then calls the rec_solve_nonogram
        function in order to complete the matrix9if there is any -1 left)
        and to get the list that contains all the solutions to that nonogram
        game. If there is no solution to the game, the function returns
        an empty list """
    matrix = solve_easy_nonogram(constraints)
    if matrix is None:
        return []
    else:
        final_res_list = rec_solve_nonogram(constraints, matrix, [], 0)
        return final_res_list