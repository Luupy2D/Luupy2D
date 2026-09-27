import pygame
import luupy2d

pygame.init()

#inicializando variáveis padrões do jogo (classe game.py)
WIDTH = 480
HEIGHT = 270
# o SCALED tenta manter o jogo corretamente escalonado.
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.Clock()
loop = True
dt = 0.0

# objetos do jogo
#player (classe player.py)
player_pos = pygame.Vector2(64,64)
player_rect = pygame.Rect(64,64,32,64)
player_speed = 128
player_dir = 1 # 1: Direita   -1: Esquerda

# TODO: Usar o módulo Path pra gerar paths que tem compatibilidades com vários OS.
# Talvez seja legal criar uma classe sprite.py para lidar com manipulação de imagens.
player_sprite_r = pygame.image.load("assets/graphics/man.png").convert_alpha()
player_sprite_l = pygame.transform.flip(player_sprite_r, True,False)
player_sprite = player_sprite_r

#monstro (classe enemy.py)
monstro_pos = pygame.Vector2(240,96)
monstro_rect = pygame.Rect(240,96,32,32)
monstro_sprite = pygame.image.load("assets/graphics/monstro.png").convert_alpha()

while loop:
    #fila de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()



    #parte lógica
    ##player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= player_speed * dt
        player_dir = -1
    if keys[pygame.K_RIGHT]:
        player_pos.x += player_speed * dt  
        player_dir = 1    

    player_rect.x = round(player_pos.x)
    if player_rect.colliderect(monstro_rect):
        impacto = pygame.Vector2(100,0)
        player_pos -= impacto

    player_sprite = player_sprite_r if player_dir == 1 else player_sprite_l

    #parte gráfica
    screen.fill("purple")

    #desenhar objetos
    screen.blit(player_sprite, player_rect)
    screen.blit(monstro_sprite, monstro_rect)

    #atualiza a tela por completo
    pygame.display.flip()

    #garante que o jogo rode a 60fps
    dt = clock.tick(60) / 1000