"""Standard Gomoku"""

from .rule import Rule
from error import GameWon
from typing import List, Tuple, Dict

class Standard(Rule):
    """Standard Gomoku"""

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Free style only check wins
        Check the pieces in each direction every click

        Free style won if pieces JUST EQUAL to 5.
        """
        for pieces in situation.values():
            if len(pieces) == self.VJC:
                raise GameWon(pieces)

