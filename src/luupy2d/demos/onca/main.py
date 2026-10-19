import pygame
import os
#import luupy2d

class Camera2D:
    def __init__(self, viewport_width, viewport_height, stage_width, stage_height):
        self.rect = pygame.Rect(0, 0, viewport_width, viewport_height)
        self.world_width = stage_width
        self.world_height = stage_height

    def seguir(self, target_rect):
        x = target_rect.centerx - (self.rect.width // 2)
        y = target_rect.centery - (self.rect.height // 2)

        # restringe a câmera aos limites do mundo (clamping)
        x = max(0, min(x, self.world_width - self.rect.width))
        y = max(0, min(y, self.world_height - self.rect.height))

        self.rect.x = x
        self.rect.y = y

    def aplicar(self, target_rect):
        #converte as coordenadas absolutas da fase para a posição da tela (viewport)
        return target_rect.move(-self.rect.x, -self.rect.y)

    def visivel(self, target_rect):
        return self.rect.colliderect(target_rect)



## Animações
def carregar_quadros(path):
    quadros = []

    imagens = sorted([
        f for f in os.listdir(path)
        if f.lower().endswith(('.png', '.bmp', '.jpg', '.jpeg'))
    ])

    for imagem in imagens:
        path_imagem = os.path.join(path, imagem)
        imagem = pygame.image.load(path_imagem)

        quadros.append(imagem)

    return quadros


def criar_dic_animacoes(path):
    animacoes = {}

    for subpasta in os.listdir(path):
        path_subpasta = os.path.join(path, subpasta)

        if os.path.isdir(path_subpasta):
            animacoes[subpasta] = carregar_quadros(path_subpasta)

    return animacoes

pygame.init()

#inicializando variáveis padrões do jogo (classe game.py)
WIDTH = 480
HEIGHT = 270
# o SCALED tenta manter o jogo corretamente escalonado.
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.Clock()
loop = True
dt = 0.0
gravidade = 9.8
font = pygame.Font(size=16)
DEBUG = False
TILE = 32

###TESTE Catedral###
##cenário movimento:
fator = 0.3
offset = 0
catedral = pygame.image.load("assets/graphics/catedral.png").convert_alpha()

# objetos do jogo
#player (classe player.py)
#animações player
player_sprites = criar_dic_animacoes("assets/graphics/onca")
player_index = 0.0
player_anim_vel = 0.15
player_anim = player_sprites["parado"][0]
player_anim_flip = 1
####

player_pos = pygame.Vector2(64,64)
player_rect = pygame.Rect(64,64,64,64)
player_chao = pygame.Rect(33, player_rect.bottom, player_rect.width - 1,4) #sensor que ajuda a detectar se o player está no chão
player_speed = pygame.Vector2(0,0)
player_dir = 1 # 1: Direita   -1: Esquerda
player_otg = False

#define a animação
player_estado = "parado"

# TODO: Usar o módulo Path pra gerar paths que tem compatibilidades com vários OS.
# Talvez seja legal criar uma classe sprite.py para lidar com manipulação de imagens.
#TESTANDO SPRITE DA ONÇA, PORTANTO PARALIZAMOS.
player_sprite_r = pygame.image.load("assets/graphics/man.png").convert_alpha()
player_sprite_l = pygame.transform.flip(player_sprite_r, True,False)
player_sprite = player_sprite_r



#monstro (classe enemy.py)
monstro_pos = pygame.Vector2(232,96)
monstro_rect = pygame.Rect(196,188,32,32)
monstro_sprite = pygame.image.load("assets/graphics/monstro.png").convert_alpha()

#testador de animações
anim = criar_dic_animacoes("assets/graphics/onca")
anim_index = 0.0
anim_vel = 0.15
anim_state = "agachado"
anim_frames = anim[anim_state]

#coisas relacionadas ao chao
def gerar_chao(coords):
    offset = 0
    chao = []
    try:
        for coord in coords:
            if coord[0] == 0:
                offset += (coord[1] * TILE)
                #TODO: se geramos um buraco, seria util gerar junto um detector q cause a morte do player tmb.

            elif coord[0] > 0:
                for i in range(coord[0]):
                    chao.append(pygame.Rect(offset, coord[1], TILE, TILE))
                    offset += TILE

            #podemos testar outros casos: numeros negativos para gerar telhado!        
            else: 
                raise IndexError("Problema ao processar as coordenadas!")
    except IndexError as e:
        print(f"Erro ao gerar o chao: {e}")

    return chao



## como funciona: o primeiro valor é o número de tiles de chão a serem colocados em sequência
## o segundo valor é a posição y aonde colocar estes chãos.

## se o primeiro valor for zero, geramos um buraco, de tamanho x = segundo valor (em tiles).
coordenadas_chao = [
    (0, 1),
    (4,260),
    (2,220),
    (0,2),
    (12, 200),
    (10,250),
    (0,4),
    (4,190),
    (18,260)
]

blocos_chao = gerar_chao(coordenadas_chao)
terra1 = pygame.image.load("assets/graphics/terra.png",).convert_alpha()
chao_imagem = terra1.subsurface(pygame.Rect(TILE, 0, TILE, TILE))
chao_imagem2 = terra1.subsurface(pygame.Rect(TILE, TILE, TILE, TILE))

#configurações de camera
stage_width = blocos_chao[-1].x + 32
stage_height = 270
camera = Camera2D(WIDTH, HEIGHT,stage_width,stage_height)


while loop:
    #fila de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

            if event.key == pygame.K_SPACE:
                player_pos = pygame.Vector2(64,64)

            if event.key == pygame.K_z and player_otg:
                player_speed.y = -300
                player_otg = False
                                    

    ###PARTE LÓGICA###
    ##player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_dir = -1
        player_estado = "andando"
    elif keys[pygame.K_RIGHT]:
        player_dir = 1
        player_estado = "andando"
    elif keys[pygame.K_DOWN]:
        player_dir = 0
        if player_otg:            
            player_estado = "agachado"
    else:
        player_dir = 0
        player_estado = "parado"

    if player_dir != 0:
        player_anim_flip = player_dir
    
    #camera, siga o player!
    camera.seguir(player_rect)
    


    #movimentação - EIXO X:
    player_speed.x = 196 * player_dir
    player_pos.x += player_speed.x * dt
    player_rect.x= round(player_pos.x)

    for bloco in blocos_chao:
        if player_rect.colliderect(bloco):
            if player_speed.x > 0:
                player_rect.right = bloco.left
                player_speed.x = 0
            if player_speed.x < 0:
                player_rect.left = bloco.right
                player_speed.x = 0

    #atualização - eixo x:
        player_pos.x = player_rect.x
    


    #movimentação - EIXO Y:
    if not player_otg:
        player_speed.y += gravidade
    player_pos.y += player_speed.y * dt
    player_rect.y= round(player_pos.y)

    #testes colisão eixo y
    for bloco in blocos_chao:
        if player_rect.colliderect(bloco):
            if player_speed.y > 0:
                player_rect.bottom = bloco.top
                player_speed.y = 0
                player_otg = True
            elif player_speed.y < 0:
                player_rect.top = bloco.bottom
                player_speed.y = 0

        #atualização: eixo y    
        player_pos.y = player_rect.y    


    player_chao.centerx = player_rect.centerx
    player_chao.top = player_rect.bottom

    if player_rect.colliderect(monstro_rect):
        #impacto = pygame.Vector2(100,0)
        #player_pos -= impacto
        pass

    player_otg = False
    for bloco in blocos_chao:
        if player_chao.colliderect(bloco):
            player_otg = True
            break




    ###PARTE GRÁFICA##
    
    #desenhar fundo
    offset = -(camera.rect.x * fator) % WIDTH
    screen.blit(catedral, (offset - WIDTH, 0))
    screen.blit(catedral, (offset, 0))
    #screen.fill((175,230,250))


    ##DESENHAR PLAYER  
    
    player_index += player_anim_vel
    if player_index > len(player_sprites[player_estado]):
        player_index = 0.0

    player_anim = player_sprites[player_estado][int(player_index)]
    if player_anim_flip == -1:
        player_anim = pygame.transform.flip(player_anim, True, False)

    screen.blit(player_anim, camera.aplicar(player_rect))
    ##

    #desenha monstro
    if camera.visivel(monstro_rect):
        screen.blit(monstro_sprite, camera.aplicar(monstro_rect))

    


    #debug
    if DEBUG:
        pygame.draw.rect(screen, "blue", camera.aplicar(player_rect), width=1)
        pygame.draw.rect(screen, "green", camera.aplicar(player_chao), width=1)

        debug_text = [
            f"No chão: {player_otg}",
            f"XVel: {player_speed.x}",
            f"YVel: {player_speed.y}",
            f"Stage_width: {stage_width}"
        ]
        for i, line in enumerate(debug_text):
            text = font.render(line, True, "black")
            screen.blit(text, (0, i*16))

        ##TESTE DEBUG ANIMAÇÃO
        anim_index += anim_vel
        if anim_index > len(anim_frames):
            anim_index = 0.0
    
        #screen.blit(anim_frames[int(anim_index)], (64,64))

    #desenhar chao
    for bloco in blocos_chao:
        #pygame.draw.rect(screen,"black",bloco)
        if camera.visivel(bloco):
            screen.blit(chao_imagem, camera.aplicar(bloco))

            #um 'hackzinho' pra gerar blocos abaixo até a borda da tela, não gera colisão!!!
            for i in range(bloco.bottom, HEIGHT, TILE):
                screen.blit(chao_imagem2, camera.aplicar(pygame.Rect(bloco.x, i, TILE, TILE)))

    #atualiza a tela por completo
    pygame.display.flip()

    #garante que o jogo rode a 60fps
    dt = clock.tick(60) / 1000