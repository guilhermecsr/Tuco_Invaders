from PPlay.sprite import *
import variaveis as var
import random as rd


class Aliens:
    def __init__(self, janela, jogo=False):
        self.grid = []
        self.janela = janela
        self.vel = var.difficultySet * 100
        self.direcao = 1
        self.void = Sprite("assets/void.png")
        self.alien_x = []
        self.alien_y = []
        self.cooldown_aliens = 0
        self.disparos = []
        self.jogo = jogo

    def cooldown_dos_aliens(self, time):
        self.cooldown_aliens += time

    def ataque_aliens(self):
        if self.cooldown_aliens >= 2:
            try:
                i = rd.randrange(0, 9)
                j = rd.randrange(0, 5)
                shot = Sprite("assets/disparo.png")
                shot.x = self.grid[i][j].x + self.grid[i][j].width / 2 - shot.width / 2
                shot.y = self.grid[i][j].y
                self.disparos.append(shot)
                self.cooldown_aliens = 0
            except IndexError:
                pass
        for k in range(len(self.disparos)):
            try:
                if self.disparos[k].y >= self.janela.height:
                    self.disparos.pop(k)
            except IndexError:
                pass

    def movimenta_desenha_disparos(self):
        for i in self.disparos:
            i.draw()
            i.y += self.vel / var.difficultySet * 5 * self.janela.delta_time()

    def cria_invaders(self):
        self.grid = [[] for x in range(9)]
        for i in range(len(self.grid)):
            for j in range(5):
                self.alien = Sprite("assets/invader_red.png", 1, 3)
                self.alien.x = 10 + i * self.alien.width * 1.5
                self.alien.y = 10 + j * self.alien.width * 1.5
                self.grid[i].append(self.alien)

    def desenha_invaders(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].draw()
                self.janela.draw_text("{}{}{}".format('*' if self.grid[i][j].health == 3 else "-",
                                                      '*' if self.grid[i][j].health >= 2 else "-",
                                                      '*' if self.grid[i][j].health >= 1 else "-"),
                                      self.grid[i][j].x+10,
                                      self.grid[i][j].y,
                                      20,
                                      (255, 255, 255))

    def movimenta_invaders_x(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                # self.alien_x.append(self.grid[i][j].x)
                # self.alien_y.append(self.grid[i][j].y)
                try:
                    if self.grid[i][j].x >= self.janela.width - 60:
                        self.direcao *= -1
                        self.reposiciona_invaders()
                        self.movimenta_invaders_y()
                    if self.grid[i][j].x <= 0:
                        self.direcao *= -1
                        self.reposiciona_invaders()
                        self.movimenta_invaders_y()

                    if var.salto >= var.difficultySet*0.8:
                        # self.alien_x = []
                        for k in range(len(self.grid)):
                            for l in range(len(self.grid[k])):
                                self.grid[k][l].x += self.direcao * 50 / var.difficultySet
                                var.salto = 0
                                # self.alien_x.append(self.grid[k][l].x)
                                # self.alien_y.append(self.grid[k][l].y)
                except IndexError:
                    pass

    def movimenta_invaders_y(self):
        self.alien_y = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].y += self.alien.height/(var.difficultySet)
                if self.grid[i][j].y >= 730:
                    self.jogo.fim()
                # self.alien_y.append(self.grid[i][j].y)

    def reposiciona_invaders(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].x > self.janela.width/2:
                    self.grid[i][j].x -= 50
                else:
                    self.grid[i][j].x += 50

    def box_de_testes(self, tiros):
        self.tiros = tiros
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                for k in range(len(self.tiros)):
                    if max(self.alien_x) >= self.tiros[k].x >= min(self.alien_x) + self.alien.width or max(self.alien_y) >= self.tiros[k].y >= min(self.alien_y):
                        return True
                    else:
                        return False

    def mata_invader(self, tiros, pontos):
        self.tiros = tiros
        self.pontos = pontos
        try:
            # if self.box_de_testes(self.tiros):
            for i in range(len(self.grid)-1, -1, -1):
                for j in range(len(self.grid[i])-1, -1, -1):
                    for k in range(len(self.tiros)):
                        if self.tiros[k].collided(self.grid[i][j]):
                            self.grid[i][j].health -= 1
                            self.tiros.pop(k)
                            if self.grid[i][j].health == 0:
                                self.grid[i].pop(j)
                                self.pontos += 1
                                break
        except IndexError:
            pass
        return self.pontos
