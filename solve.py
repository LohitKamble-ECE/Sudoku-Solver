from typing import Tuple, List


class Sudoku:
    def __init__(self, string: str) -> None:
        """Create and initialize the Sudoku puzzle that can be solve later.

        Args:
            string (str): Total 81 numeric character string representating
            puzzle. The order of digits is left-to-right and top-to-bottom with
            0's representing blank cells in the puzzle.
        """
        self._puzzle = self._create_puzzle_grid(string)

    def _create_puzzle_grid(self, string: str) -> List[List[int]]:
        """Create a puzzle grid out of string provided.

        Args:
            string (str): Use this string to create puzzle.

        Returns:
            List[List[int]]: This is puzzle string.
        """
        puzzle = []
        for string_digits in self._split_string_interval(string, 9):
            puzzle.append(list(map(int, self._split_string_interval(string_digits, 1))))
        return puzzle

    def _split_string_interval(self, string: str, n: int) -> List[str]:
        """Split a string at regular interval.

        Args:
            string (str): A string that need to be splitted.
            n (int): An interval at which string should be splitted.

        Returns:
            List[str]: Return list of string splitted at regular interval.
        """
        return [string[x : x + n] for x in range(0, len(string), n)]

    def __str__(self):
        """Implements str(self)."""
        output = ""
        for row in self._puzzle:
            output += " ".join(map(str, row)) + "\n"
        return output

    def _next_location(self, i: int, j: int) -> Tuple[int, int] | None:
        """Compute the next location for cell in puzzle grid to solve for that
        particular cell.

        Args:
            i (int): current location i.e. x in (x, y)
            j (int): current location i.e. y in (x, y)

        Returns:
            Tuple[int, int] | None: Next location in the form (x, y). None if
            there is no next location available to solve.
        """
        next_j = (j + 1) % 9
        if next_j == 0:
            next_i = (i + 1) % 9
            if next_i != 0:
                return next_i, next_j
        else:
            return i, next_j
        return None

    def _is_valid_guess(self, i: int, j: int, guess: int) -> bool:
        """Returns True, if our guess will be valid guess for the puzzle grid in
        particular location, False otherwise.

        Args:
            i (int): current location i.e. x in (x, y)
            j (int): current location i.e. y in (x, y)
            guess (int): the integer in the range(1, 10) that we have guess

        Returns:
            bool: True when guess will be good fit in puzzle, False otherwise.
        """
        for var_col in range(9):
            if self._puzzle[i][var_col] == guess:
                return False

        for var_row in range(9):
            if self._puzzle[var_row][j] == guess:
                return False

        start_x, start_y = (i // 3) * 3, (j // 3) * 3
        for var_row in range(start_x, start_x + 3):
            for var_col in range(start_y, start_y + 3):
                if self._puzzle[var_row][var_col] == guess:
                    return False
        return True

    def solve(self, i: int = 0, j: int = 0) -> bool:
        """Solve the puzzle.

        Approach: Recursion and Backtracking.

        Time complexity: O(n^2)

        Args:
            i (int, optional): The beginning position. Defaults to 0.
            j (int, optional): The beginning position. Defaults to 0.

        Returns:
            bool: Return True when puzzle successfully get solved, False
            otherwise.
        """
        if self._puzzle[i][j] != 0:
            positions = self._next_location(i, j)
            if positions is None:
                return True  # Base case: no more cell location to solve.
            else:
                next_i, next_j = positions
                return self.solve(next_i, next_j)
        else:
            for guess in range(1, 10):
                if self._is_valid_guess(i, j, guess):
                    self._puzzle[i][j] = guess
                    positions = self._next_location(i, j)
                    if positions is None:
                        return True  # Base case: no more cell location to solve.
                    else:
                        next_i, next_j = positions
                        if self.solve(next_i, next_j):
                            return True  # Current guess has worked!
        self._puzzle[i][j] = 0  # restore to default
        return False
