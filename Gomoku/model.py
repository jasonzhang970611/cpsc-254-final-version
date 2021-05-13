"""
Game data manager
Use None for unfilled, False for black, and True for white.
The manager provides related access interfaces.
"""

from error import InvalidGridError, SettedGridError
from collections import defaultdict
from typing import List, Tuple, Union, Iterator, Set, Dict, Optional


class Manager:
    """
    Game data manager
    Use a two-dimensional array matrix to represent the game board.
    """

    def __init__(self, size: int) -> None:
        """
        Initialize a new game data manager.
        Parameters:
            size: int - length and width of the game board (same)
        """
        self._ended = False
        self._size = size
        self._records: List[Tuple[int, int]] = list()
        self._board: List[List[Union[None, bool]]] = [
            [None for _index in range(size)]
            for _index in range(size)
        ]

    @property
    def size(self) -> int:
        """Return size of game board"""
        return self._size

    def undo(self) -> Tuple[int, int]:
        """Undo the last step"""
        row, column = self._records.pop()
        self._board[row][column] = None
        return row, column

    @property
    def steps(self) -> int:
        """Return steps count"""
        return len(self._records)

    @property
    def turn(self) -> bool:
        """Return which turn"""
        return len(self._records) % 2 == 0

    @property
    def ended(self) -> bool:
        """Return if game ended"""
        return self._ended

    def end(self) -> None:
        """Set end flag"""
        self._ended = True

    def reset(self) -> None:
        """Reset game status"""
        self._records.clear()
        self._ended = False
        self._board: List[List[Union[None, bool]]] = [
            [None for _index in range(self._size)]
            for _index in range(self._size)
        ]

    def _around(self, _x: int, _y: int) -> Iterator[Tuple[int, int]]:
        """Return all grids's indexs around specific grid"""
        if _x >= self._size or _y >= self._size:
            raise InvalidGridError(
                "Invalid index for ({x}, {y})".format(x=_x, y=_y))

        for i in (_x - 1, _x, _x + 1):
            for j in (_y - 1, _y, _y + 1):
                if (i, j) == (_x, _y):
                    continue
                if i < 0 or j < 0:
                    continue
                if i >= self._size or j >= self._size:
                    continue
                yield (i, j)

    def find(self, row: int, column: int,
             paths: Optional[Dict[int, Set[Tuple[int, int]]]] = None,
             direction: Optional[int] = None) -> Dict[int, Set[Tuple[int, int]]]:
        """
        Try to continuously find the specified amount
        of continuously set data in any direction
        Parameters:
            row, column: position or grid
            paths: path for all directions
            directions:
            1   2   3
              ↖ ↑ ↗
            4 ← · → 4
              ↙ ↓ ↘
            3   2   1
        """
        target = self[row, column]
        if paths is None:
            paths = {1: set(), 2: set(), 3: set(), 4: set()}

        # Find all grids aorund current one
        around = self._around(row, column)
        classified = defaultdict(list)
        for nrow, ncolumn in around:

            # Filter all invalid grid
            if not self[nrow, ncolumn] == target:
                continue

            # Filter non-set grid
            if self[nrow, ncolumn] == None:
                continue

            # Define direction
            if (nrow - row) * (ncolumn - column) == 1:
                classified[1].append((nrow, ncolumn))
            if nrow - row == 0:
                classified[2].append((nrow, ncolumn))
            if (nrow - row) * (ncolumn - column) == -1:
                classified[3].append((nrow, ncolumn))
            if ncolumn - column == 0:
                classified[4].append((nrow, ncolumn))

        # If direction has not been specified
        if direction is None:
            for ndirection, grids in classified.items():
                for nrow, ncolumn in grids:
                    paths[ndirection].add((row, column))
                    paths[ndirection].add((nrow, ncolumn))
                    self.find(nrow, ncolumn, paths, ndirection)

        # If direction has been sprcified
        else:
            grids = classified[direction]
            for nrow, ncolumn in grids:
                if (nrow, ncolumn) in paths[direction]:
                    continue
                paths[direction].add((nrow, ncolumn))
                self.find(nrow, ncolumn, paths, direction)

        # If all directional recursions break before condition satisfied
        return paths

    def __setitem__(self, index: Tuple[int, int], value: Union[None, bool]) -> None:
        """Set status for specific index of grid"""
        _x, _y = index
        if _x > self._size or _x < 0 or _y > self._size or _y < 0:
            raise InvalidGridError(
                "Invalid index for ({x}, {y})".format(x=_x, y=_y))

        # Check for grid if grid has been set
        if isinstance(self._board[_x][_y], bool) and not value is None:
            raise SettedGridError("Cannot set grid which has already been set")

        self._board[_x][_y] = value
        if value is None:
            self._records.remove(index)
        else:
            self._records.append(index)

    def __getitem__(self, index: Tuple[int, int]) -> Union[None, bool]:
        """Return status for specific index of grid"""
        _x, _y = index
        if _x > self._size or _x < 0 or _y > self._size or _y < 0:
            raise IndexError("Invalid index for ({x}, {y})".format(x=_x, y=_y))
        return self._board[_x][_y]

    def show(self) -> None:
        """Show all grids status"""
        status = list()
        for row in self._board:
            for column in row:
                if column is None:
                    status.append('x ')
                if column is True:
                    status.append('Y ')
                if column is False:
                    status.append('N ')
            status.append('\n')
        print(''.join(status))


# Test case
if __name__ == "__main__":
    size = 10

    # Test for size property
    manager = Manager(size)
    assert(manager.size == size)

    # Boundary conditions testing of private function _around
    assert(set(manager._around(0, 0)) == {(0, 1), (1, 0), (1, 1)})
    assert(set(manager._around(0, size - 1)) == {
        (0, size - 2), (1, size - 1), (1, size - 2)})
    assert(set(manager._around(1, 1)) == {(0, 0), (0, 1), (0, 2),
                                          (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)})
    assert(set(manager._around(size - 1, 0)) == {
        (size - 2, 0), (size - 2, 1), (size - 1, 1)})
    assert(set(manager._around(size - 1, size - 1)) == {
        (size - 1, size - 2), (size - 2, size - 2), (size - 2, size - 1)})

    # Test setitem and getitem function
    manager[0, 0] = True
    assert(manager[0, 0] == True)
    assert(manager[0, 1] == None)
    try:
        manager[0, 0] = False
    except SettedGridError as _error:
        pass
    else:
        raise AssertionError("Setitem function test failed!")

    # Test step count function
    assert(manager.steps == 1)

    # Test find function
    manager[0, 1] = True
    manager[1, 0] = False
    manager[1, 1] = True
    manager[3, 0] = True
    manager[2, 2] = False
    assert(manager.find(0, 0) == {
        1: {(1, 1), (0, 0)}, 2: {(0, 1), (0, 0)},
        3: set(), 4: set()
    })

    # Test show function
    manager.show()
