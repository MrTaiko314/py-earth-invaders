import tkinter as tk
from tkinter import ttk


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600


class Game(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        self.title('Py Earth Invaders')

        x = (self.winfo_screenwidth() - CANVAS_WIDTH) // 2
        y = (self.winfo_screenheight() - CANVAS_HEIGHT) // 2
        self.geometry(f'{CANVAS_WIDTH}x{CANVAS_HEIGHT}+{x}+{y}')

        self._mainframe: ttk.Frame | None = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._key_pressed_dict: dict[str, bool] = {}
        self.bind('<KeyPress>', self._on_key_press)
        self.bind('<KeyRelease>', self._on_key_release)

        from pyearthinvaders.main_menu_screen import MainMenuScreen
        self.set_screen(MainMenuScreen(self))

    def set_screen(self, screen: ttk.Frame) -> None:
        if self._mainframe is not None:
            self._mainframe.grid_remove()

        self._mainframe = screen
        self._mainframe.grid(column=0, row=0, sticky='nswe')

    def is_key_pressed(self, keysym: str) -> bool:
        return self._key_pressed_dict.get(keysym, False)

    def _on_key_press(self, event) -> None:
        self._key_pressed_dict[event.keysym] = True

    def _on_key_release(self, event) -> None:
        self._key_pressed_dict[event.keysym] = False
