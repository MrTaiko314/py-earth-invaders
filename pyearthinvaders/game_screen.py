import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

from pyearthinvaders.cannon import Cannon
from pyearthinvaders.entity import Entity
from pyearthinvaders.game import Game
from pyearthinvaders.laser import Laser
from pyearthinvaders.missile import Missile
from pyearthinvaders.rocket import Rocket
from pyearthinvaders.vec2 import Vec2


UPDATE_RATE_IN_MS = 30
ROCKETS_BASE_SPEED = 50
CANNON_FIRE_MIN_DELAY_IN_SECONDS = 0.3
CANNON_HORIZONTAL_SPEED = 200
LASER_VERTICAL_SPEED = 1000
MISSILE_VERTICAL_SPEED = 300
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
START_LIFE_COUNT = 3


class GameScreen(ttk.Frame):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.game = game
        self.game.title('Py Earth Invaders')

        self.background_image = tk.PhotoImage(file='./assets/background.png')
        self.cannon_image = tk.PhotoImage(file='./assets/cannon.png')
        self.laser_image = tk.PhotoImage(file='./assets/laser.png')
        self.missile_image = tk.PhotoImage(file='./assets/missile.png')
        self.rocket1_image = tk.PhotoImage(file='./assets/rocket1.png')
        self.rocket2_image = tk.PhotoImage(file='./assets/rocket2.png')
        self.rocket3_image = tk.PhotoImage(file='./assets/rocket3.png')
        self.special_ship_image = tk.PhotoImage(
            file='./assets/special_ship.png')

        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

        # Posicionamento da interface

        self.canvas.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Criação dos objetos

        self.game_over = False
        self.life_count = START_LIFE_COUNT
        self.last_cannon_fire_time = 0.0

        self.canvas.create_image(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=self.background_image)

        cannon_x = (CANVAS_WIDTH - self.cannon_image.width()) // 2
        cannon_y = CANVAS_HEIGHT - 70
        cannon_start_position = Vec2(cannon_x, cannon_y)
        self.cannon_requesting_fire = False
        cannon_speed = Vec2.zero()
        self.cannon = Cannon(
            cannon_start_position, self.cannon_image.width(),
            self.cannon_image.height(), cannon_speed)

        self.cannon_id = self.canvas.create_image(
            self.cannon.position.x, self.cannon.position.y,
            image=self.cannon_image, anchor='nw')

        self.lasers: list[Laser] = []
        self.lasers_ids = []

        self.rocket_group_position = Vec2(20, 60)
        self.rockets_speed = Vec2(ROCKETS_BASE_SPEED, 0)
        self.rockets_images_ids = []
        self.rockets: list[Rocket] = []
        for row in range(5):
            rocket_image = (
                self.rocket3_image if row < 2
                else self.rocket2_image if row < 4
                else self.rocket1_image)
            for column in range(11):
                x = self.rocket_group_position.x + column*30
                y = self.rocket_group_position.y + row*30
                position = Vec2(x, y)
                speed = Vec2.zero()
                rocket = Rocket(
                    position, rocket_image.width(), rocket_image.height(),
                    speed, column, row)
                self.rockets.append(rocket)

                rocket_image_id = self.canvas.create_image(
                    x, y, image=rocket_image, anchor='nw')
                self.rockets_images_ids.append(rocket_image_id)

        firing_rocket = self.select_firing_rocket()
        self.rocket_fire(firing_rocket)

        self.render(0)

    def draw_hitbox(self, entity: Entity) -> None:
        """Método para debugar apenas."""
        x0 = entity.position.x
        y0 = entity.position.y
        x1 = x0 + entity.width
        y1 = y0 + entity.height
        self.canvas.create_rectangle(x0, y0, x1, y1, outline='red')

    def cannon_fire(self) -> None:
        width = self.laser_image.width()
        height = self.laser_image.height()
        x = self.cannon.position.x + (self.cannon.width - width)//2
        y = self.cannon.position.y - height
        position = Vec2(x, y)
        speed = Vec2(0, -LASER_VERTICAL_SPEED)
        laser = Laser(position, width, height, speed)
        self.lasers.append(laser)

        laser_id = self.canvas.create_image(x, y, image=self.laser_image, anchor='nw')
        self.lasers_ids.append(laser_id)

    def get_rockets_front_line(self) -> list[Rocket]:
        columns: list[int] = []
        result: list[Rocket] = []
        # Percorremos do final para o início porque as naves finais são as que
        # são inseridas por último na array, fazendo-as ficarem nas últimas
        # linhas.
        for rocket in reversed(self.rockets):
            if len(columns) == 11:
                # Temos 11 colunas apenas
                break

            if rocket.column not in columns:
                result.append(rocket)
                columns.append(rocket.column)

        return result

    def select_firing_rocket(self) -> Rocket:
        front_line = self.get_rockets_front_line()
        if len(front_line) == 0:
            raise RuntimeError('No rockets!')

        return random.choice(front_line)

    def rocket_fire(self, rocket: Rocket) -> None:
        width = self.missile_image.width()
        height = self.missile_image.height()
        position = Vec2(rocket.left + (rocket.width - width)//2, rocket.bottom)
        speed = Vec2(0, MISSILE_VERTICAL_SPEED)
        self.missile = Missile(position, width, height, speed)
        self.missile_image_id = self.canvas.create_image(
            self.missile.position.x, self.missile.position.y,
            image=self.missile_image, anchor='nw')

    def render(self, delta: float) -> None:
        """delta é a quantidade de segundos passada desde a última chamada a esta função."""
        now = time.time()

        self.handle_input()
        self.update_cannon(delta)
        self.update_rockets(delta)
        self.update_rockets_speed()
        self.update_missile(delta)
        self.update_lasers(delta)

        if not self.game_over:
            self.after(UPDATE_RATE_IN_MS, lambda: self.render(time.time() - now))

    def handle_input(self) -> None:
        self.cannon.speed.x = 0

        if self.game.is_key_pressed('Right'):
            self.cannon.speed.x += CANNON_HORIZONTAL_SPEED

        if self.game.is_key_pressed('Left'):
            self.cannon.speed.x -= CANNON_HORIZONTAL_SPEED

        self.cannon_requesting_fire = self.game.is_key_pressed('Up')

    def update_cannon(self, delta: float) -> None:
        self.cannon.update(delta)

        if self.cannon.position.x < 0:
            self.cannon.position.x = 0
        elif self.cannon.right > CANVAS_WIDTH:
            self.cannon.position.x = CANVAS_WIDTH - self.cannon.width

        self.canvas.moveto(
            self.cannon_id, self.cannon.position.x, self.cannon.position.y)

        if (self.cannon_requesting_fire
                and (time.time() - self.last_cannon_fire_time >= CANNON_FIRE_MIN_DELAY_IN_SECONDS)):
            self.cannon_fire()
            self.last_cannon_fire_time = time.time()

    def update_lasers(self, delta: float) -> None:
        for laser_index in range(len(self.lasers) - 1, -1, -1):
            laser = self.lasers[laser_index]
            laser_id = self.lasers_ids[laser_index]

            laser.update(delta)
            self.canvas.moveto(laser_id, laser.position.x, laser.position.y)

            if laser.bottom < 0:
                # Laser saiu da tela
                self.canvas.delete(self.lasers_ids[laser_index])
                self.lasers.pop(laser_index)
                self.lasers_ids.pop(laser_index)
                continue

            for rocket_index, rocket in enumerate(self.rockets):
                if laser.overlaps(rocket):
                    self.canvas.delete(self.rockets_images_ids[rocket_index])
                    self.rockets.pop(rocket_index)
                    self.rockets_images_ids.pop(rocket_index)

                    self.canvas.delete(self.lasers_ids[laser_index])
                    self.lasers.pop(laser_index)
                    self.lasers_ids.pop(laser_index)

                    if len(self.rockets) == 0:
                        messagebox.showinfo('Fim de jogo!', 'Você destruiu todos os foguetes!')
                        self.game_over = True
                        return

                    break

    def update_missile(self, delta: float) -> None:
        self.missile.update(delta)
        self.canvas.moveto(self.missile_image_id, self.missile.position.x, self.missile.position.y)
        if self.missile.position.y > CANVAS_HEIGHT:
            self.canvas.delete(self.missile_image_id)
            firing_rocket = self.select_firing_rocket()
            self.rocket_fire(firing_rocket)
        elif self.missile.overlaps(self.cannon):
            self.life_count -= 1
            if self.life_count <= 0:
                messagebox.showinfo('Fim de jogo!', 'Você perdeu todas as vidas!')
                self.game_over = True
                return

            self.canvas.delete(self.missile_image_id)
            firing_rocket = self.select_firing_rocket()
            self.rocket_fire(firing_rocket)

    def update_rockets(self, delta: float) -> None:
        dx = int(delta * self.rockets_speed.x)
        dy = int(delta * self.rockets_speed.y)
        self.rocket_group_position.x += dx
        self.rocket_group_position.y += dy

        for rocket, rocket_image_id in zip(self.rockets, self.rockets_images_ids):
            rocket.update(delta)
            self.canvas.moveto(rocket_image_id, rocket.position.x, rocket.position.y)

    def update_rockets_speed(self) -> None:
        if self.rockets_speed.x > 0:
            if self.rocket_group_position.x > 60:
                self.rockets_speed.x = -ROCKETS_BASE_SPEED
                self.rockets_speed.y = 0
            elif self.rocket_group_position.x > 50:
                self.rockets_speed.x = ROCKETS_BASE_SPEED
                self.rockets_speed.y = ROCKETS_BASE_SPEED
        else:
            if self.rocket_group_position.x < 20:
                self.rockets_speed.x = ROCKETS_BASE_SPEED
                self.rockets_speed.y = 0
            elif self.rocket_group_position.x < 30:
                self.rockets_speed.x = -ROCKETS_BASE_SPEED
                self.rockets_speed.y = ROCKETS_BASE_SPEED

        for rocket in self.rockets:
            rocket.speed = self.rockets_speed
