import pygame, sys
from pygame.locals import *
import os
from random import randint
pygame.init()

#ARQUIVOS USADOS
icon = pygame.image.load(os.path.join("arquivos","icon.png"))
fundo_img = pygame.image.load(os.path.join("arquivos","fundo.png"))
nave_img = pygame.image.load(os.path.join("arquivos","nave.png"))
alienB1_img = pygame.image.load(os.path.join("arquivos","alienB1.png"))
alienB2_img = pygame.image.load(os.path.join("arquivos","alienB2.png"))
ost = pygame.mixer.music.load(os.path.join("arquivos","ost.mp3"))
alien_atingido = pygame.mixer.Sound(os.path.join("arquivos", "alien_atingido.wav"))
nave_atingida = pygame.mixer.Sound(os.path.join("arquivos", "nave_atingida.wav"))
tiro_nave_som = pygame.mixer.Sound(os.path.join("arquivos", "nave_tiro.wav"))

#TELA DO GAME
largura_tela, altura_tela = 1024 , 720
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)
janela = pygame.display.set_mode((largura_tela,altura_tela))
jogando = True
count = 0
rodada = 1

#SONS
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)
tiro_nave_som.set_volume(0.01)
nave_atingida.set_volume(0.02)
alien_atingido.set_volume(0.02)

#CLASSES
class Jogador: #classe do player
    def __init__(self, x, y): #metodo construtor com os atributos X e Y
        self.x = x
        self.y = y

    def draw(self): #metodo para desenhar a nave na tela, de acordo com o x e y
        janela.blit(nave_img, (self.x, self.y))
    
class Inimigo: #classe do inimigo
    def __init__(self, x, y, vel): #metodo construtor do inimigo com os atributos x, y e vel(velocidade de descida do inimigo)
        self.x = x
        self.y = y
        self.vel = vel

    def draw(self): #metodo para desenhar o inimigo na tela, de acordo com o x e y e sua vel(velocidade)
        inimigos = [alienB1_img,alienB2_img]
        janela.blit(inimigos[randint(0,1)], (self.x, self.y))
        self.y += self.vel 

    def colisao(self): #metodo para detectar a colisao do laser com os inimigos
        for laser in lasers:
            if laser.x > self.x and laser.x < self.x + 64 and laser.y > self.y and laser.y < self.y + 64:
                lasers.remove(laser)
                inimigos.remove(self)

    def spawn_inimigos_wave(x_spawn, y_spawn, vel): #metodo para spawnar os inimigos
        for x in range(1, x_spawn): 
            for y in range(1, y_spawn): 
                inimigos.append(Inimigo(x * 50, y * 50, vel)) #*50 para separar e não nascerem na mesma posição

class Laser: #classe do laser do jogador
    def __init__(self, x, y): #metodo construtor com os atributos x e y
        self.x = x+45 #(+45) para o laser sair exatamente do bico da nave
        self.y = y

    def draw(self): #metodo para desenhar o laser na tela, de acordo com o x e y
        pygame.draw.rect(janela, (254, 71, 110), pygame.Rect(self.x, self.y, 2, 5))
        self.y -= 2

jogador = Jogador(largura_tela/2, altura_tela - 100) #criando o objeto do jogador

inimigos = [] #lista para spawnar os inimigos
lasers = []  

def text(text): #função para escrever na tela
    font = pygame.font.SysFont('Arial', 50)
    message = font.render(text, False, (255, 255, 255))
    janela.blit(message, ((largura_tela/2)-110, (altura_tela/2)-100))

#MAIN
while jogando:
    janela.blit(fundo_img, (0, 0)) #colocando a imagem de fundo
    jogador.draw() #desenha o jogador na tela
    pressed = pygame.key.get_pressed() #alocando botão pressionado em váriavel
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]: #movimentação para a esquerda tanto pelo botao A, tanto pela seta para esquerda
        if jogador.x > 20: #condição para manter o jogador dentro da tela
            jogador.x -= 2
    elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]: #movimentação para a direita tanto pelo botao D, tanto pela seta para direita
        if jogador.x < largura_tela - 40: #condição para manter o jogador dentro da tela
            jogador.x += 1

    for event in pygame.event.get(): #for para percorrer pelos eventos
        if event.type == pygame.QUIT: #evento de tipo QUIT para parar o while e fechar o jogo
            jogando = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #para fazer o jogador conseguir atirar com a tecla espaco
            lasers.append(Laser(jogador.x, jogador.y))
            tiro_nave_som.play()

    for inimigo in inimigos: #percorre pelos inimigos e aplica o metodo draw() para desenhar e o colisao() para detectar a colisao
        inimigo.draw()
        inimigo.colisao()
        if inimigo.y > altura_tela-100: #condicao para o GAME OVER
            text("GAME OVER")
            if count == 0:
                count += 1
                nave_atingida.play()

    for laser in lasers:
        laser.draw()

    #condicoes para cada round e dar sequencia ao jogo
    if len(inimigos) <= 0 and rodada == 1: 
        rodada += 1
        Inimigo.spawn_inimigos_wave(10,4,0.05)

    if len(inimigos) <= 0 and rodada == 2:
        rodada += 1
        Inimigo.spawn_inimigos_wave(12,4,0.08)

    if len(inimigos) <= 0 and rodada == 3:
        rodada += 1
        Inimigo.spawn_inimigos_wave(14,4,0.10)

    if len(inimigos) <= 0 and rodada == 4:
        rodada += 1
        Inimigo.spawn_inimigos_wave(16,4,0.12)

    if len(inimigos) <= 0 and rodada == 5:
        rodada += 1
        Inimigo.spawn_inimigos_wave(18,4,0.12)

    if len(inimigos) <= 0 and rodada == 6:
        rodada += 1

    if len(inimigos) <= 0 and rodada == 7:
        text("Parabéns, você venceu!")
        
    pygame.display.update()