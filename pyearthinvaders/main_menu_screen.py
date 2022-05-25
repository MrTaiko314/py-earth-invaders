from tkinter import ttk

from pyearthinvaders.game import Game


class MainMenuScreen(ttk.Frame):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.game = game
        self.game.title('Menu Principal - Py Earth Invaders')

        play_game_button = ttk.Button(
            self, text='Jogar', command=self.play_game)

        play_game_button.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def play_game(self) -> None:
        from pyearthinvaders.game_screen import GameScreen
        self.game.set_screen(GameScreen(self.game))
