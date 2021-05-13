"""Rule for Gomoku Pro"""

from .rule import Rule
from error import RuleException, InvalidPosition, GameWon
from typing import List, Tuple, Dict


class Pro(Rule):
    """Gomoku Pro"""

    def __init__(self, size: int) -> None:
        """Gomoku Pro request size of board for first step"""
        self._centre = size // 2
        if size <= 5:
            raise RuleException("Board too small playing Gomoku Pro")

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Gomoku Pro:
            1. Black must play at centre for first step
            2. White could play any position
            3. Black play at any position except centre size 5x5
            4. After that as Standard Gomoku
        """
        # Check first step
        if step == 1 and position != (self._centre, self._centre):
            raise InvalidPosition("Centre required",
                                  "First step must play in centre")

        # Check third step
        if step == 3:
            row, column = position
            if (self._centre - 2 <= row <= self._centre + 2) and \
               (self._centre - 2 <= column <= self._centre + 2):
                raise InvalidPosition("Non-Centre required",
                                      "Third step must not play at centre 5x5 area")
        
        # Check win like Gomoku Standard
        for pieces in situation.values():
            if len(pieces) == self.VJC:
                raise GameWon(pieces)
