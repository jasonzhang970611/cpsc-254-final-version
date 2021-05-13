"""Free Style Gomoku Rule"""

from .rule import Rule
from error import GameWon
from typing import List, Tuple, Dict

class FreeStyle(Rule):
    """Free Style"""

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Free style only check wins
        Check the pieces in each direction every click

        Free style won if pieces GREATER or EQUAL than 5.
        """
        for pieces in situation.values():
            if len(pieces) >= self.VJC:
                raise GameWon(pieces)
