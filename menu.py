import ranking
from PPlay.sprite import *
from PPlay.mouse import *
from ranking import *


class Menu:
    def __init__(self, janela, fundo, game, difficultySet):
        self.janela = janela
        self.fundo = fundo
        self.game = game
        self.ranking = ranking.Rank(janela, fundo)
        self.difficultySet = difficultySet
        self.button = Sprite("assets/button_1.jpg")
        self.button_start = Sprite("assets/start_button_1.jpg")
        self.button_difficulty = Sprite("assets/difficulty_button_1.jpg")
        self.button_rank = Sprite("assets/rank_button_1.jpg")
        self.button_exit = Sprite("assets/sair_button_1.jpg")
        self.mouse = Mouse()

        # posicionamento
        menu_x = janela.width / 2 - self.button.width / 2
        menu_y = janela.height / 2 - self.button.height / 2

        self.button_start.x = menu_x
        self.button_start.y = menu_y - self.button.height * 2 - 50

        self.button_difficulty.x = menu_x
        self.button_difficulty.y = menu_y - self.button.height - 25

        self.button_rank.x = menu_x
        self.button_rank.y = menu_y

        self.button_exit.x = menu_x
        self.button_exit.y = menu_y + self.button.height + 25

    def menu_loop(self):
        while True:

            # cliques
            if self.mouse.is_over_object(self.button_exit) and self.mouse.is_button_pressed(1):
                break

            if self.mouse.is_over_object(self.button_start) and self.mouse.is_button_pressed(1):
                self.game.tiros = []
                self.game.cronometro, self.game.pontos = 0, 0
                self.game.aliens.cria_invaders()
                self.game.nave.health = 5
                self.game.game_loop()

            if self.mouse.is_over_object(self.button_difficulty) and self.mouse.is_button_pressed(1):
                self.difficultySet.difficulty_loop()

            if self.mouse.is_over_object(self.button_rank) and self.mouse.is_button_pressed(1):
                self.ranking.ranking_loop()


            self.fundo.draw()

            self.button_start.draw()
            self.button_difficulty.draw()
            self.button_rank.draw()
            self.button_exit.draw()

            self.janela.update()
