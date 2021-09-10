import ranking
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *
import variaveis as var
import aliens


class Game:
    def __init__(self, janela, fundo):
        self.janela = janela
        self.fundo = fundo
        self.teclado = Keyboard()

        # player
        self.nave = Sprite("assets/nave_player_white.png", 3, 5)
        self.nave.set_sequence_time(0, 3, 200)
        self.nave.y = self.janela.height - self.nave.height - 50
        self.nave.x = self.janela.width/2 - self.nave.width/2
        self.tiros = []
        self.cooldown = 2
        self.nave.play()


        self.game_over = GameImage("assets/game_over.png")

        # invaders
        self.aliens = aliens.Aliens(self.janela, self)

        # ranking
        self.ranking = ranking.Rank(self.janela, self.fundo)

        # attributes
        self.vel = 700 * var.difficultySet
        self.pontos = 0
        self.cronometro = 0
        self.duracao = 0
        self.invencivel = False
        self.invencivel_time = 0

        # framerate
        self.fps = 0
        self.frames = 0
        self.relogio = 0
        self.media = 0
        self.medias = []
        self.aux = 0

    def mata_player(self):
        for i in range(len(self.aliens.disparos)):
            try:
                if self.aliens.disparos[i].y >= self.janela.height - self.nave.height - 50:
                    if self.nave.collided(self.aliens.disparos[i]) and not self.invencivel:
                        self.nave.health -= 1
                        self.aliens.disparos.pop(i)
                        self.nave.x = self.janela.width/2 - self.nave.width/2
                        self.invencivel = True
                        self.invencivel_time = 0
            except IndexError:
                pass
        if self.invencivel_time >= 2:
            self.invencivel = False
            self.nave.set_curr_frame(0)
        else:
            for j in range(10):
                self.nave.update()

    def fim(self):
        self.aliens.grid.clear()
        self.aliens.disparos.clear()
        while True:
            self.game_over.draw()
            if self.teclado.key_pressed("ESC"):
                break
            self.janela.update()

    def game_loop(self):
        while True:
            if self.teclado.key_pressed("ESC"):
                self.aliens.grid.clear()
                self.aliens.disparos.clear()
                break

            # movimentacao
            if self.teclado.key_pressed("LEFT") and self.nave.x > 0:
                self.nave.x = self.nave.x - self.vel * self.janela.delta_time()

            if self.teclado.key_pressed("RIGHT") and self.nave.x < self.janela.width - self.nave.width:
                self.nave.x = self.nave.x + self.vel * self.janela.delta_time()

            # ataque
            if self.teclado.key_pressed("SPACE"):
                shot = Sprite("assets/shot.png")
                shot.x = self.nave.x + self.nave.width/2 - shot.width/2
                shot.y = self.nave.y
                if self.cooldown >= 1/3 and not var.LOW_ENERGY:
                    self.tiros.append(shot)
                    if not var.DISPAROS >= 10:
                        self.cooldown = 0
                        var.DISPAROS += 1

            if var.DISPAROS >= 10:
                self.nave.set_curr_frame(2)
                var.LOW_ENERGY = True
                var.COOLDOWN += self.janela.delta_time()
            if var.COOLDOWN >= 3:
                self.nave.set_curr_frame(0)
                var.LOW_ENERGY = False
                var.COOLDOWN = 0
                var.DISPAROS = 0

            # ranking
            if self.pontos >= 45:
                self.duracao = self.cronometro
                self.ranking.end_loop(self.pontos, self.duracao)
                self.cronometro, self.pontos = 0, 0
                break


            self.fundo.draw()

            self.nave.draw()

            # hit poinst
            self.janela.draw_text("{}{}{}{}{}".format('*' if self.nave.health == 5 else "-",
                                                  '*' if self.nave.health >= 4 else "-",
                                                  '*' if self.nave.health >= 3 else "-",
                                                  '*' if self.nave.health >= 2 else "-",
                                                  '*' if self.nave.health >= 1 else "-"),
                                  self.nave.x + 5,
                                  self.nave.y + 60,
                                  20,
                                  (255, 255, 255))
            if self.nave.health == 0:
                self.fim()

            for i in self.tiros:
                i.draw()
                i.y -= self.vel * self.janela.delta_time()

            for k in range(len(self.tiros)):
                try:
                    if self.tiros[k].y <= 0:
                        self.tiros.pop(k)
                except IndexError:
                    pass

            self.aliens.desenha_invaders()
            self.aliens.movimenta_invaders_x()

            # ataque dos aliens
            self.aliens.ataque_aliens()
            self.aliens.cooldown_dos_aliens(self.janela.delta_time())
            self.aliens.movimenta_desenha_disparos()
            self.mata_player()

            # acerto
            self.pontos = self.aliens.mata_invader(self.tiros, self.pontos)
            
            self.cooldown += self.janela.delta_time()
            self.invencivel_time += self.janela.delta_time()

            # framerate
            self.janela.draw_text("fps: {}; média: {}".format(self.fps, int(self.media/(10 + self.aux))), 50, 10, 30, (255, 255, 255))
            self.relogio += self.janela.delta_time()
            self.frames += 1

            var.salto += self.janela.delta_time()

            # pontuação
            self.cronometro += self.janela.delta_time()
            self.janela.draw_text("Time: {:.1f}".format(self.cronometro), self.janela.width - 200, 10, 30, (255, 255, 255))
            self.janela.draw_text("Death Match: {}".format(self.pontos), self.janela.width/2 - 100, 10, 30, (255, 255, 255))


            if self.relogio >= 1:
                self.relogio = 0
                self.fps = self.frames
                self.medias.append(self.fps)
                self.frames = 0

            if len(self.medias) >= 10 + self.aux:
                if self.aux < 50: self.aux += 1
                self.medias.pop(0)
                self.media = 0
                for i in range(len(self.medias)):
                    self.media += self.medias[i]

            self.janela.update()
