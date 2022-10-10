import numpy as np
import matplotlib.pyplot as plt
import timeit


def check_that_number_fit_trial_and_error(grid, horizontally, perpendicularly, check_number):
    """
    The function used to check a number that matches the given place
    for trial and error in compliance with the basic rules
    :param grid: sudoku to solve
    :param horizontally: place position on the horizontal axis
    :param perpendicularly: place position on the perpendicularly axis
    :param check_number: check that the specific number matches this position
    :return:
    """
    # Check if there is already a number in the horizontally
    for position_in_line in range(0, 9):
        if grid[horizontally][position_in_line] == check_number:
            return False
    # Check if there is already a number in the perpendicularly
    for position_in_line in range(0, 9):
        if grid[position_in_line][perpendicularly] == check_number:
            return False
    # Check if there is already number in the square
    position_x0_for_check_square = (horizontally // 3) * 3
    position_y0_for_check_square = (perpendicularly // 3) * 3
    for delta_x in range(0, 3):
        for delta_y in range(0, 3):
            if grid[position_x0_for_check_square + delta_x][position_y0_for_check_square + delta_y] == check_number:
                return False

    return True


def check_that_number_fit_deduction(grid, x_square_number, y_square_number, check_number):
    """
    Function used that number fit in specific place for Trial and error method
    :param grid: sudoku to solve
    :param x_square_number: square position on the horizontal axis
    :param y_square_number: square position on the perpendicularly axis
    :param check_number: check that the specific number matches this position
    :return:
    """
    check_square = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
    possible_position_for_number_in_check_square = 0
    x_position_in_grid = x_square_number * 3
    y_position_in_grid = y_square_number * 3

    # Check that in square is already check_number
    for delta_y in range(0, 3):
        for delta_x in range(0, 3):
            if grid[y_position_in_grid + delta_y][x_position_in_grid + delta_x] == check_number:
                return

    # Check that in square is already number
    for delta_y in range(0, 3):
        for delta_x in range(0, 3):
            if grid[y_position_in_grid + delta_y][x_position_in_grid + delta_x] != 0:
                check_square[delta_y][delta_x] = 1

    # check line for specific number for y
    for delta_y in range(0, 3):
        for position in range(0, 9):
            if grid[y_position_in_grid + delta_y][position] == check_number:
                for x_position_in_square in range(0, 3):
                    check_square[delta_y][x_position_in_square] = 1

    # check line for specific number for x
    for delta_x in range(0, 3):
        for position in range(0, 9):
            if grid[position][x_position_in_grid + delta_x] == check_number:
                for y_position_in_square in range(0, 3):
                    check_square[y_position_in_square][delta_x] = 1

    for delta_y in range(0, 3):
        for delta_x in range(0, 3):
            if check_square[delta_y][delta_x] == 0:
                possible_position_for_number_in_check_square += 1

    if possible_position_for_number_in_check_square == 1:
        for delta_y in range(0, 3):
            for delta_x in range(0, 3):
                if check_square[delta_y][delta_x] == 0:
                    x_possible_position = x_position_in_grid + delta_x
                    y_possible_position = y_position_in_grid + delta_y
                    grid[y_possible_position][x_possible_position] = check_number
    return


def trial_and_error_method_solve(grid, debug):
    """
    Trial and error method with basic rules is used to solve sudoku
    :param debug: show count details
    :param grid: sudoku to solve
    :return:
    """
    every_possible_position_in_grid = 81
    for horizontally in range(0, 9):
        for perpendicularly in range(0, 9):
            if grid[horizontally][perpendicularly] == 0:
                # Check that in sudoku still leave any 0
                for check_number in range(1, 10):
                    if check_that_number_fit_trial_and_error(grid, horizontally, perpendicularly, check_number):
                        grid[horizontally][perpendicularly] = check_number
                        trial_and_error_method_solve(grid, debug)
                        # When function get stuck
                        grid[horizontally][perpendicularly] = 0
                return
    if debug:
        print(np.matrix(grid))


def deduction_solve(grid, debug):
    """
    Deduction method is used to solve sudoku
    Deduction method get stuck when in sudoku not exist place where only one number fit
    :param debug: show count details
    :param grid: sudoku to solve
    :return: True if method solve sudoku and false id can't
    """
    every_possible_position_in_grid = 81
    fill_number_list = []
    while np.count_nonzero(grid) < every_possible_position_in_grid:
        fill_number_list.append(np.count_nonzero(grid))
        if len(fill_number_list) >= 2:
            # check that deduction method get stuck
            if fill_number_list[-1] == fill_number_list[-2]:
                if debug:
                    print("deduction method can't solve this problem")
                break
        for x_square_number in range(0, 3):
            for y_square_number in range(0, 3):
                for check_number in range(1, 10):
                    check_that_number_fit_deduction(grid, x_square_number, y_square_number, check_number)
    if debug:
        print(np.matrix(grid))
    if np.count_nonzero(grid) == every_possible_position_in_grid:
        return True
    return False


def deduction_and_trial_and_error_solve(grid, debug):
    """
    Deduction and if deduction method fail trial and error method is used to solve sudoku
    Deduction method get stuck when in sudoku not exist place where only one number fit.
    If that happen to continue solve sudoku get used trial and error method with basic rules
    :param debug: show count details
    :param grid: sudoku to solve
    :return:
    """
    every_position_in_grid = 81
    fill_number_list = []

    # deduction method
    while np.count_nonzero(grid) < every_position_in_grid:
        fill_number_list.append(np.count_nonzero(grid))
        if len(fill_number_list) >= 2:
            # check that deduction method get stuck
            if fill_number_list[-1] == fill_number_list[-2]:
                if debug:
                    print("deduction method can't solve this problem and change on trail and error method")
                break
        for x_square_number in range(0, 3):
            for y_square_number in range(0, 3):
                for check_number in range(1, 10):
                    check_that_number_fit_deduction(grid, x_square_number, y_square_number, check_number)

    # trail and error method if deduction fail
    for horizontally in range(0, 9):
        for perpendicularly in range(0, 9):
            if grid[horizontally][perpendicularly] == 0:
                # Check that in sudoku still leave any 0
                for check_number in range(1, 10):
                    if check_that_number_fit_trial_and_error(grid, horizontally, perpendicularly, check_number):
                        grid[horizontally][perpendicularly] = check_number
                        trial_and_error_method_solve(grid, debug)
                        # When function get stuck
                        grid[horizontally][perpendicularly] = 0
                return
    if debug:
        print(np.matrix(grid))


def get_sudoku(sudoku_difficult_level):
    if sudoku_difficult_level == 1:
        grid = [[4, 0, 3, 0, 2, 0, 0, 7, 1],
                [2, 6, 0, 0, 5, 0, 0, 4, 9],
                [9, 0, 8, 4, 0, 0, 0, 5, 6],
                [0, 4, 2, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 9, 1, 5],
                [1, 0, 9, 5, 0, 0, 0, 0, 7],
                [3, 8, 0, 2, 0, 9, 7, 0, 0],
                [0, 2, 1, 0, 3, 0, 5, 0, 8],
                [7, 9, 0, 0, 0, 0, 0, 0, 0]]
        return grid
    elif sudoku_difficult_level == 2:
        grid = [[0, 0, 6, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 5, 0, 7, 3, 0, 0],
                [0, 0, 3, 6, 0, 0, 0, 8, 4],
                [0, 4, 0, 7, 5, 2, 0, 3, 0],
                [8, 0, 7, 0, 0, 0, 5, 4, 0],
                [0, 0, 0, 0, 0, 9, 0, 0, 0],
                [9, 6, 2, 0, 0, 0, 0, 0, 5],
                [1, 0, 0, 0, 2, 4, 0, 6, 3],
                [0, 7, 0, 0, 0, 0, 0, 2, 0]]
        return grid
    elif sudoku_difficult_level == 3:
        grid = [[0, 9, 0, 7, 0, 1, 0, 0, 0],
                [0, 0, 0, 4, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 6, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 9, 5, 0, 0, 7],
                [6, 0, 8, 0, 4, 0, 0, 9, 0],
                [8, 0, 0, 3, 0, 0, 7, 0, 0],
                [0, 0, 4, 0, 5, 0, 0, 0, 2],
                [0, 2, 9, 0, 0, 0, 0, 5, 8]]
        return grid
    elif sudoku_difficult_level == 4:
        grid = [[0, 4, 0, 0, 0, 5, 8, 7, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 0, 2],
                [0, 0, 0, 0, 7, 0, 4, 0, 0],
                [0, 5, 1, 3, 0, 0, 0, 0, 7],
                [0, 0, 3, 0, 0, 6, 0, 0, 0],
                [0, 0, 5, 0, 0, 2, 0, 9, 0],
                [0, 0, 0, 5, 0, 8, 6, 0, 0],
                [0, 0, 0, 0, 6, 4, 0, 0, 0]]
        return grid


def check_performance_for_methods(sudoku_difficult_level, debug=False):
    """
    :param debug: check count details
    :param sudoku_difficult_level:
    1 - easy
    2 - medium
    3 - hard
    4 - very hard
    """
    # sudoku_difficult_level valid
    if sudoku_difficult_level not in [1, 2, 3, 4]:
        return print("wrong value for sudoku_difficult_level")

    function_trial_and_error = []
    function_deduction = []
    function_deduction_and_trial_and_error = []
    count_time = []

    for count_function_time in range(1, 6):
        count_time.append(count_function_time)
        grid = get_sudoku(sudoku_difficult_level)

        start_time = timeit.default_timer()
        trial_and_error_method_solve(grid, debug)
        end_time = timeit.default_timer()
        function_trial_and_error.append(end_time-start_time)

        start_time = timeit.default_timer()
        deduction_and_trial_and_error_solve(grid, debug)
        end_time = timeit.default_timer()
        function_deduction_and_trial_and_error.append(end_time-start_time)

        start_time = timeit.default_timer()
        if deduction_solve(grid, debug):
            end_time = timeit.default_timer()
            function_deduction.append(end_time-start_time)

    if debug:
        print('function_trial_and_error:', function_trial_and_error)
        print('function_deduction_and_trial_and_error:', function_deduction_and_trial_and_error)
        print('function_deduction', function_deduction)

    font = {'family': 'Arial',
            'weight': 'normal',
            'size': 20}

    plt.rc('font', **font)
    plt.xlabel('Function run count')
    plt.ylabel('Overall processing time (ms)')

    fix, ax = plt.subplots(figsize=(14, 8))
    ax.plot(count_time, function_trial_and_error, 'o', linewidth=1)
    ax.plot(count_time, function_deduction_and_trial_and_error, 'o', linewidth=1)
    if len(function_deduction) == 5:
        ax.plot(count_time, function_deduction, 'o', linewidth=1)
    ax.legend(['Trial and error', 'Deduction and trail and error', 'Deduction'])
    plt.show()


check_performance_for_methods(1, debug=False)

