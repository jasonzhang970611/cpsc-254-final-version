"""
Draw game interface
Use Tkinter and Canvas to draw interface
Provide a way to draw pieces
"""

from core.algorithm import transpose
from error import GameSettingError
from settings import ViewSettings

import tkinter
from tkinter import ttk
import tkinter.messagebox as msgbox
from collections import OrderedDict as odict
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union, OrderedDict


class Board:
    """
    Gaming Board Interface
    Use canvas to draw horizontal and vertical lines
    Handle mouse click events, generate click
    position parameters and pass them to the middle layer

    Return value:
        True - Black
        False - White
    """
    # White space between the edge of the
    # window and the main interface of the game
    PADDING = ViewSettings.PADDING
    ICONMAP = ViewSettings.ICONMAP
    TITLE = ViewSettings.TITLE  # Game window title

    BLACK = ViewSettings.BLACK  # Black player
    WHITE = ViewSettings.WHITE  # White player
    BWIN = ViewSettings.BWIN  # Win color black
    WWIN = ViewSettings.WWIN  # Win color white

    BGCOLOR = ViewSettings.BGCOLOR  # Background color for game board
    BHINT = ViewSettings.BHINT  # Black hinter
    WHINT = ViewSettings.WHINT  # White hinter

    LOCATINGR = 5  # Radius of location point
    OUTLINEMARG = 3  # Pixels margin of outline

    SELECT_PANEL_BGC = "#ECECEC"  # Default selection panel background color

    def __init__(self, root: tkinter.Tk, size: int, grids: int) -> None:
        """
        Instantiate a new game board object.
        Draw on the given parent Tk object.
        Parameters:
            root: in which window you want to draw
            size: total game window size
            grids: number of grids (usually 15 or 19)
            user: who are player:
                True: black
                False: white
                * If mpmode is False it will change by click

            mpmode: active multiplayer mode
        """
        # Check for grids number
        if (grids % 2 != 1):
            raise GameSettingError("Invalid grids number")

        # Patch for invalid size and grids
        self._root = root
        self._root.resizable(False, False)
        self._root.title(self.TITLE)
        self._grids, self._size = grids, size
        if self._size % (grids - 1) != 0:
            self._size = (self._size // (grids - 1)) * (grids - 1)

        # Draw canvas
        self._root = root
        self._board = tkinter.Canvas(
            root, width=self._size + self.PADDING * 2,
            height=self._size + self.PADDING * 2, bg=self.BGCOLOR)
        self._board.pack(anchor=tkinter.CENTER)
        self._unit = self._size // (grids - 1)
        self._board.focus_set()

        # Draw hint piece
        piece = int(self._unit / 3.0)
        self._hinter = self._board.create_oval(
            0, 0, -piece * 2, -piece * 2,
            fill=self.BHINT, outline="")

        # Bind left key and moving
        self._board.bind("<Button-1>", self._click)
        self._board.bind("<Motion>", self._moving)

        # Handle left key function
        self._click_handler = None
        self._restart_handler = None
        self._undo_handler: Optional[Callable[[], Tuple[int, int]]] = None

        # Initial menubar
        menubar = tkinter.Menu(self._root)
        other = tkinter.Menu(menubar)

        controller = tkinter.Menu(menubar)
        menubar.add_cascade(label="Game", menu=controller)
        menubar.add_cascade(label="Other", menu=other)

        # TODO: New Game selection bar
        controller.add_command(label="Undo step", command=self._undo)
        controller.add_command(label="Restart Game", command=self._restart)
        controller.add_separator()
        controller.add_command(label="Exit Game", command=self._exit)

        # TODO: Add statistics
        other.add_command(label="Statistics", command=lambda: msgbox.showinfo(
            "Step Count", "Game has been played for {0} steps.".format(len(self._pieces))
        ))
        other.add_separator()
        other.add_command(label="Help", command=self._help)
        other.add_command(label="About", command=self._about)
        root.configure(menu=menubar)

        # Configure icon
        root.iconbitmap(self.ICONMAP)

        # Record pieces
        self._pieces: OrderedDict[Tuple[int, int], int] = odict()

    @staticmethod
    def _help() -> None:
        """Show help dialog"""
        msgbox.showinfo("Help", (
            "Please choose the appropriate location.\n"
            "The color of the chess piece following the "
            "prompt of the mouse is the color of the "
            "upcoming chess piece."
        ))

    @staticmethod
    def _about() -> None:
        """Show about info"""
        msgbox.showinfo("About", (
            "This is a simple Gomoku.\n"
            "Wish you a happy game!\n"
            "Author: guiqiqi187@gmail.com"
        ))

    def win(self, who, pieces: Iterable[Tuple[int, int]]) -> None:
        """Show congratulations"""

        # Pieces to mark the winning side.
        color = self.WWIN if not bool(who) else self.BWIN
        for row, column in pieces:
            piece = self._pieces.get((row, column), None)
            self._board.itemconfig(piece, fill=color)

        msgbox.showinfo("Congratulations",
                        "{player} win!\nExiting game.".format(player=str(who)))
        self._root.destroy()

    @property
    def click(self) -> Union[Callable[[int, int], None], None]:
        """Return leftkey function"""
        return self._click_handler

    @click.setter
    def click(self, func: Union[Callable[[int, int], None], None]) -> None:
        """Set leftkey handler"""
        self._click_handler = func

    @property
    def restart(self) -> Union[Callable[[], None], None]:
        """Return restart function"""
        return self._restart_handler

    @restart.setter
    def restart(self, func: Union[Callable[[], None], None]) -> None:
        """Set restart handler"""
        self._restart_handler = func

    @property
    def fundo(self) -> Optional[Callable[[], Tuple[int, int]]]:
        """Return undo handler"""
        return self._undo_handler

    @fundo.setter
    def fundo(self, func: Optional[Callable[[], Tuple[int, int]]]) -> None:
        """Set undo handler"""
        self._undo_handler = func

    def _click(self, position: tkinter.Event) -> None:
        """Handle for left key click event"""
        _x, _y = position.x - self.PADDING, position.y - self.PADDING
        if _x < 0 or _y < 0:
            return
        _x -= self._unit // 2
        _y -= self._unit // 2
        row, column = _x // self._unit + 1, _y // self._unit + 1
        if row > self._grids - 1 or column > self._grids - 1:
            return

        # Send row and column data to handler
        if not self._click_handler is None:
            self._click_handler(row, column)

    @staticmethod
    def showmsg(title, msg) -> None:
        """Show message"""
        msgbox.showinfo(title, msg)

    def hint(self, color: bool) -> None:
        """Toogle hint color to specific one"""
        target = self._hinter
        hintcolor = self.BHINT if color else self.WHINT
        self._board.itemconfig(target, fill=hintcolor)

    def _restart(self) -> None:
        """Restart game"""
        if msgbox.askyesno("Confirm", "Do you really want restart this game?"):
            self._board.destroy()

            # Retstart handlers and board view
            handlers = self._restart_handler, self._click_handler, self._undo_handler
            self.__init__(self._root, self._size, self._grids)
            self._restart_handler, self._click_handler, self._undo_handler = handlers
            self.draw()

            if not self._restart_handler is None:
                self._restart_handler()

    def _moving(self, position: tkinter.Event) -> None:
        """Handle moving event"""
        target = self._hinter
        xa, ya, xb, yb = self._board.coords(target)
        nx, ny = (xa + xb) / 2, (ya + yb) / 2
        dx, dy = position.x - nx, position.y - ny
        self._board.move(target, dx, dy)

    def _undo(self) -> None:
        """Undo the last step"""
        if not msgbox.askyesno("Confirm", "Do you really want undo the last step?"):
            return
        if not self._undo_handler or not self._pieces:
            return
        x, y = self._undo_handler()
        self.undo(x, y)

    def _exit(self) -> None:
        """Destory window and exit game"""
        if msgbox.askyesno("Confirm", "Do you really want exit this game?"):
            self._root.destroy()
            __import__("sys").exit(0)

    def play(self, row: int, column: int, color: bool) -> None:
        """Drop off at the specified position"""
        # Calc fillcolor
        fillcolor = self.BLACK if color else self.WHITE

        # Position and radius calculation
        _x = row * self._unit + self.PADDING
        _y = column * self._unit + self.PADDING
        radius = int(self._unit / 3.0)
        position = _x - radius, _y - radius, _x + radius, _y + radius

        # Create canvas oval
        if (row, column) in self._pieces:
            return
        piece = self._board.create_oval(*position, fill=fillcolor, outline="")
        self._pieces[(row, column)] = piece

    def undo(self, row: int, column: int) -> None:
        """Undo canvas draw"""
        piece = self._pieces.get((row, column), None)
        if piece:
            self._pieces.pop((row, column))
            self._board.delete(piece)

    def draw(self) -> None:
        """Draw vertical and horizontal lines as the game board"""
        for index in range(self._grids):
            # Draw horizontal
            startx = self.PADDING, self.PADDING + self._unit * index
            endx = self.PADDING + self._size, self.PADDING + self._unit * index
            self._board.create_line(*startx, *endx)

            # Draw vertical
            starty = self.PADDING + index * self._unit, self.PADDING
            endy = self.PADDING + index * self._unit, self.PADDING + self._size
            self._board.create_line(*starty, *endy)

        # Draw locating point
        for row, column in {
            (3, 3), (self._grids - 4, self._grids - 4),
            (3, self._grids - 4), (self._grids - 4, 3),
                (self._grids // 2, self._grids // 2)}:
            _x = row * self._unit + self.PADDING
            _y = column * self._unit + self.PADDING
            positions = _x - self.LOCATINGR, _y - self.LOCATINGR, \
                _x + self.LOCATINGR, _y + self.LOCATINGR
            self._board.create_oval(*positions, fill=self.BLACK)

        # Draw outline
        self._board.create_rectangle(
            self.PADDING - self.OUTLINEMARG,
            self.PADDING - self.OUTLINEMARG,
            self._size + self.PADDING + self.OUTLINEMARG,
            self._size + self.PADDING + self.OUTLINEMARG)

    def selpanel(self, title: str, labels: Tuple[str, ...],
                 options: Dict[Tuple[str, ...], Callable],
                 callbacks: Dict[bool, Callable]
        ) -> None:
        """
        Draw a selection panel:
        options is callback vectors, which options is key of Dict:
        {
            ("Local", "FreeStyle"): Callback,
            ("Internet", "FreeStyle"): Callback,
            ("AI", "FreeStyle"): Callback,
            ...
        },
        which label assigned to layer index of options.keys():
        [
            "Game Type", "Rule"
        ].

        Callbacks:
        {
            True: Call if callback function return True
            False: Call if callback function return False
        }
        """
        toplevel = tkinter.Toplevel(
            self._root, background=self.SELECT_PANEL_BGC)       
        toplevel.title(title)
        layers = transpose(options.keys())
        menus: List[Tuple[tkinter.StringVar, ttk.OptionMenu]] = list()

        for index, layer in enumerate(layers):
            value = tkinter.StringVar(toplevel)
            ops = list(set(layer))
            menu = ttk.OptionMenu(toplevel, value, ops[0], *ops)
            ttk.Label(toplevel, text=labels[index]).grid(
                column=0, row=index, padx=10)
            menu.grid(column=1, row=index, padx=10, pady=10, sticky=tkinter.EW)
            menus.append((value, menu))

        def select():
            """Check selection"""
            selection: List[str] = list()
            for value, _menu in menus:
                selection.append(value.get())

            handler = options.get(tuple(selection), None)
            if callable(handler):

                # Check callback function ret value
                ret = handler()
                callback = callbacks.get(ret, None)
                if callable(callback):
                    callback()

                toplevel.destroy()

        ttk.Button(toplevel, text="Confirm", command=select).grid(
            column=0, columnspan=2, row=len(layers), pady=10)
        toplevel.resizable(False, False)
        toplevel.grab_set()

        # Disable click when not selecting
        self._root.wait_window(toplevel)


# Test game viewing
if __name__ == "__main__":

    root = tkinter.Tk()
    size = 650
    grids = 15

    value = 0
    checked = set()

    # Test click handler
    def test(row, column):
        global value, checked
        if (row, column) in checked:
            raise ValueError("Checked!")
        value += 1
        checked.add((row, column))

    board = Board(root, size, grids)
    board.click = test
    board.draw()
    root.focus_get()
    root.mainloop()
