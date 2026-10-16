import pygame as pg

pg.init()

## Constantes

#CORES
CEU = (200,23,65)
GRAMA = (46,139,87)
PRETO = (0,0,0)
BRANCO = (255,255,255)

#Dimensoes da tela
LARGURA = 480
ALTURA = 270

#Quadros por segundo (FPS)
FPS = 60

#Escolhas de roteiro
ORIENTACAO = 'H'

#Posicao inicial do protagonista (PLAYER)

PLAYER_X = 64
PLAYER_Y = 50

## ASSETS

#Player
PLAYER = pg.image.load('assets/graphics/man.png').convert_alpha()
#PLAYER = pg.image.load('assets/players/loboguara.png').convert_alpha()
#PLAYER = pg.image.load('assets/players/mucura.png').convert_alpha()

#Obstaculos (OBx)
#OB1 = pg.image.load('assets/obstacles/pedra.png').convert_alpha()
#OB2 = pg.image.load('assets/obstacles/arbusto.png').convert_alpha()
#Confira o catalogo de assets

# Inimigos (ENEMIES)
ENEMY01 = pg.image.load('assets/graphics/monstro.png').convert_alpha()
#ENEMY02 = pg.image.load('assets/enemies/fogo.png').convert_alpha()

#Demais elementos gráficos (ELEMENTS)
#NUVEM = pg.image.load('assets/elements/nuvem.png').convert_alpha()

#Preparando o jogo
relogio = pg.time.Clock()
tela = pg.display.set_mode((LARGURA, ALTURA), pg.SCALED | pg.RESIZABLE)
pg.display.set_caption("Meu jogo")

loop_do_jogo = True
frame_inicial = 0

while loop_do_jogo:
    #Carregando cenário
    tela.fill(CEU)
    pg.draw.rect(tela, GRAMA, [0, ALTURA/2, LARGURA, ALTURA/2])


    #Relógio
    relogio.tick(60)