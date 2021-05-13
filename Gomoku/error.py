"""All error definition"""

from typing import Any, Callable, Iterable, Tuple, Dict, Any


class GameError(Exception):
    """General game error"""


class GameSettingError(Exception):
    """Error occured during initialization"""


class RuleException(Exception):
    """Basic Rule Exception"""


class InvalidPosition(RuleException):
    """Invalid position played"""

    def __init__(self, title: str, msg: str) -> None:
        self.title = title
        self.msg = msg


class SwapRequest(RuleException):
    """Request swap"""

    SwapSelectionPanelTitle = "Swap"

    def __init__(self, hint: Tuple[str, ...],
                 callbacks: Dict[Tuple[str, ...], Callable[
                     [Dict[bool, Any]], bool
                 ]]) -> None:
        self.hint = hint
        self.options = callbacks


class InvalidGridError(GameError):
    """Invalid piece index"""


class SettedGridError(GameError):
    """Cannot set Grid has been set"""


class GameWon(GameError):
    """Game won"""

    def __init__(self, pieces: Iterable[Tuple[int, int]]) -> None:
        """Initialize this error"""
        self.pieces: Iterable[Tuple[int, int]] = pieces


class GameEnded(GameError):
    """Raise when game has already ended"""
