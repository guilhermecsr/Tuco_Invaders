from PPlay.keyboard import *
import variaveis as var
from PPlay.keyboard import *
import aliens
import csv


class Rank:
    def __init__(self, janela, fundo):
        self.pontos = self
        self.duracao = self
        self.janela = janela
        self.fundo = fundo
        self.teclado = Keyboard()
        self.aliens = aliens.Aliens(self.janela)
        self.rank_r = open('rank.csv', 'r', encoding='utf-16')
        self.reader = csv.reader(self.rank_r)
        self.temp = open('temp.csv', 'w', encoding='utf-16')
        self.writer = csv.writer(self.temp)
        self.ranking = []

    def end_loop(self, pontos, duracao):
        self.duracao = duracao
        self.pontos = ((pontos*10)/var.difficultySet)-self.duracao

        while True:
            if self.teclado.key_pressed("ENTER"):
                self.ranking = self.define_pontuacao(self.pontos, self.writer)
                self.ranking_loop()
                break

            self.fundo.draw()

            self.janela.draw_text("Sua pontuação: {:.2f}".format(self.pontos),
                                  self.janela.width/2 - 400,
                                  self.janela.height/2 - 50,
                                  80,
                                  (255, 255, 255))
            self.janela.draw_text("Pressione Enter para eternizar",
                                  self.janela.width/2 - 380,
                                  self.janela.height/2 + 50,
                                  50,
                                  (255, 255, 255))
            self.janela.draw_text("sua posição no ranking",
                                  self.janela.width/2 - 380,
                                  self.janela.height/2 + 105,
                                  50,
                                  (255, 255, 255))

            self.janela.update()


    def define_pontuacao(self, pontos, escrever):
        self.ranking = self.le_rank()
        self.escreve_rank(self.ranking, pontos, escrever)
        self.rank_r.close()
        self.temp.close()
        self.le_temp()
        return self.ranking


    def le_rank(self):
        rank_r = open('rank.csv', 'r', encoding='utf-16')
        reader = csv.reader(rank_r)
        for i in reader:
            self.ranking.append(i)
        return self.ranking

    def escreve_rank(self, ranking, pontos, escrever):
        temp = open('temp.csv', 'w', encoding='utf-16')
        writer = csv.writer(temp)
        nome = input("Diga seu vulgo: ")
        if len(ranking[0]) > 0:
            for i in ranking:
                writer.writerow([int(float(i[0])), i[1]])
            writer.writerow([int(pontos), nome])
        else:
            writer.writerow([int(pontos), nome])

    def le_temp(self):
        rank_w = open('rank.csv', 'w', encoding='utf-16')
        rank_w = csv.writer(rank_w)
        temp = open('temp.csv', 'r', encoding='utf-16')
        temp = csv.reader(temp)
        for i in temp:
            rank_w.writerow(i)

    def ranking_loop(self):
        rank_r = open('rank.csv', 'r', encoding='utf-16')
        reader = csv.reader(rank_r)
        array = []
        for i in reader:
            array.append(i)
        array.sort(reverse=True)
        while True:
            self.fundo.draw()
            for i in range(5):
                self.janela.draw_text(f"#{i+1}    {array[i][0]}pts    {array[i][1]}",
                                      self.janela.width/3,
                                      (50 + i*100),
                                      60,
                                      (255, 255, 255))

            if self.teclado.key_pressed("ESC"):
                break

            self.janela.update()
