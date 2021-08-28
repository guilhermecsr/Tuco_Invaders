from menu import *
from jogo import *
from ranking import *
from dificuldade import *
from PPlay.window import *
from PPlay.gameimage import *

janela = Window(1300, 865)
janela.set_title("Tuco Invaders")

fundo = GameImage("assets/fundo_1300x865.png")

# ranking = Rank(janela, fundo)
dificuldade = Dificuldade(janela, fundo)
game = Game(janela, fundo)
menu = Menu(janela, fundo, game, dificuldade)

menu.menu_loop()
