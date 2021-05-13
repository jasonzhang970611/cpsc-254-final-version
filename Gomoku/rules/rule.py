"""Rule abstract class"""

from abc import abstractmethod
from typing import List, Set, Tuple, Dict, Type


class Rule:
    """Abstract Rule class"""

    VJC = 5  # Gomoku

    @abstractmethod
    def __init__(self) -> None:
        """
        Usually do not need implement this method
        Initialize additonal swapped flag when using Swap* Rules:
            flag: bool - have player been swaped
        """
        self._swapped = False
        ...

    def __repr__(self) -> str:
        """Console entity name"""
        return "<Rule {name}>".format(name=str(self))

    def __str__(self) -> str:
        """Return name of rule"""
        return type(self).__name__

    @staticmethod
    def rules() -> List[Type["Rule"]]:
        """Return all subclasses of Rule using reflection"""
        return Rule.__subclasses__()

    @abstractmethod
    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, Set[Tuple[int, int]]]) -> None:
        """
        The instantiated class needs to support this
        __call__ function so that the upper-level 
        click callback function can be successfully called.

        Function signature:
            __call__(self, position: Tuple[int, int], step: int,
                     situation: Iterable[Tuple[int, int]]) -> None
            position: The position of piece of this round
            step: Total step count
            situation: The situation of consecutive pieces 
                       around the current position.

        Function does not need to return a value,
        relevant process is determined by the exception thrown:
            GameWon(
                pieces: Iterable[Tuple[int, int]]
            ) - current player won this game
            InvalidPosition() - player could not play in this pos
            SwapRequest(
                options: Dict[str, Callable[[Dict[bool, Player]], Callable]]
                    Callback method vectors
            ) - Request swap player this turn
            ...
        """
