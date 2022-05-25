from tkinter import ttk

from pyearthinvaders.game import Game


class Screen(ttk.Frame):

    def __init__(self, game: Game) -> None:
        self.game = game
