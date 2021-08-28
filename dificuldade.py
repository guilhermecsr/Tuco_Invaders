from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
import variaveis as var


class Dificuldade:
    def __init__(self, janela, fundo):
        self.janela = janela
        self.fundo = fundo
        self.button = Sprite("assets/button_1.jpg")
        self.button_easy = Sprite("assets/easy_button_1.jpg")
        self.button_medium = Sprite("assets/medium_button_1.jpg")
        self.button_hard = Sprite("assets/hard_button_1.jpg")
        self.mouse = Mouse()
        self.teclado = Keyboard()

        # posicionamento
        menu_x = janela.width / 2 - self.button.width / 2
        menu_y = janela.height / 2 - self.button.height / 2

        self.button_easy.y = menu_y
        self.button_medium.y = menu_y
        self.button_hard.y = menu_y

        self.button_easy.x = menu_x - self.button.width - 25
        self.button_medium.x = menu_x
        self.button_hard.x = menu_x + self.button.width + 25

    def difficulty_loop(self):
        while True:
            if self.teclado.key_pressed("ESC"):
                break
            if self.mouse.is_over_object(self.button_easy) and self.mouse.is_button_pressed(1):
                var.difficultySet = 1.5
                break
            if self.mouse.is_over_object(self.button_medium) and self.mouse.is_button_pressed(1):
                var.difficultySet = 1
                break
            if self.mouse.is_over_object(self.button_hard) and self.mouse.is_button_pressed(1):
                var.difficultySet = 0.8
                break
            self.fundo.draw()

            self.button_easy.draw()
            self.button_medium.draw()
            self.button_hard.draw()
            self.janela.update()
