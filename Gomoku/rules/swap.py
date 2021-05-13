"""Swap and Swap2 Rules"""


from player import Player
from error import GameWon, RuleException, SwapRequest
from .rule import Rule
from typing import List, Tuple, Dict


class Swap(Rule):
    """Swap Rule"""

    def swapping(self, players: Dict[bool, Player]) -> bool:
        """Swap players"""
        black, white = players[True], players[False]

        # Swap player name
        black._color = False
        white._color = True

        # Swap player color
        players[True] = white
        players[False] = black

        return True

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Swap Rule:
            After third piece has been played, 
            Ask the white players if he want to swap
            After that using Gomoku Standard
        """

        # Ask swapping
        if step == 3:
            request = SwapRequest(("Selection for White player: ",), {
                ("Take Black", ): lambda _o: self.swapping(_o),
                ("Hold White", ): lambda _o: False
            })
            raise request

        # Check winning
        for pieces in situation.values():
            if len(pieces) == self.VJC:
                raise GameWon(pieces)


class Swap2(Swap):
    """Swap2 Rule"""

    def __init__(self) -> None:
        """Initialize Swapped flag to False"""
        self._swapped = False

    def swapping(self, players: Dict[bool, Player]) -> bool:
        """After swapped set flag"""
        self._swapped = True
        return super().swapping(players)

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Swap Rule:
            After third piece has been played, 
            Ask the white players if he want to swap
                1. Swap
                2. Not swap
                3. Wait for 6th times selection
            After that using Gomoku Standard
        """

        # Ask swapping for step == 3
        if step == 3:
            request = SwapRequest(("Selection for White player: ",), {
                ("Take Black", ): lambda _o: self.swapping(_o),
                ("Hold White", ): lambda _o: False,
                ("No decision yet", ): lambda _o: False
            })
            raise request

        # Ask swapping for step == 6
        if step == 6 and not self._swapped:
            request = SwapRequest(("Selection for White player: ",), {
                ("Take Black", ): lambda _o: self.swapping(_o),
                ("Hold White", ): lambda _o: False
            })
            raise request

        # Check winning
        for pieces in situation.values():
            if len(pieces) == self.VJC:
                raise GameWon(pieces)
