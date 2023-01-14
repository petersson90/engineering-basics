# pylint: disable=missing-docstring

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def validation_groups(self):
        groups_to_check = list()

        # Add all values from each row
        rows = [row for row in self.grid]
        groups_to_check += rows

        # Add all values from each column
        columns = [[row[column] for row in self.grid] for column in range(9)]
        groups_to_check += columns

        # for column in range(9):
        #     group = list()
        #     for row in self.grid:
        #         group.append(row[column])
        #     groups_to_check.append(group)

        # Add all values from each area
        sudoku_areas = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for columns in sudoku_areas:
            for rows in sudoku_areas:
                group = list()

                for column in columns:
                    for row in rows:
                        group.append(self.grid[row][column])

                groups_to_check.append(group)

        # Return all number sequences as list of lists
        return groups_to_check


    def is_valid(self):
        valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Check if each group is valid
        for group in self.validation_groups():
            if not sorted(group) == valid_numbers:
                print(group)
                return False

        return True


if __name__ == "__main__":
    test_grid = [
        [7,8,4,  1,5,9,  3,2,6],
        [5,3,9,  6,7,2,  8,4,1],
        [6,1,2,  4,3,8,  7,5,9],

        [9,2,8,  7,1,5,  4,6,3],
        [3,5,7,  8,4,6,  1,9,2],
        [4,6,1,  9,2,3,  5,8,7],

        [8,7,6,  3,9,4,  2,1,5],
        [2,4,3,  5,6,1,  9,7,8],
        [1,9,5,  2,8,7,  6,3,4]
    ]

    sudoku = SudokuSolver(test_grid)

    print(sudoku.is_valid())
