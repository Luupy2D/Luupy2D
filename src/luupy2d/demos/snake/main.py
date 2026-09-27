import pygame
import random

random.seed()

class Snake:    
    segments = []   #lista de rects, [0] eh a cabeca da cobra
    direction = []  #direcao q a cobra se movimenta no formato [x, y]
    def __init__(self,startx=128, starty=128, size=3):
        for i in range(size):
            self.segments.append(pygame.Rect(startx-(i*GRID_SIZE), starty ,GRID_SIZE,GRID_SIZE))
        self.direction = [GRID_SIZE, 0]
    
    @property
    def head(self):
        return self.segments[0]

    def draw(self):
        for seg in self.segments:
            pygame.draw.rect(screen,"green",seg)
            if DEBUG:
                pygame.draw.rect(screen,"red",seg,2)

    def move(self, grow=False):
        newx = self.head.x + self.direction[0]
        newy = self.head.y + self.direction[1]
        new_head = pygame.Rect(newx, newy, GRID_SIZE, GRID_SIZE)
        self.segments.insert(0, new_head)
        if not grow:
            self.segments.pop()

    def is_dead(self):
        if self.head.x < (GRID_SIZE) or self.head.x >= (WIDTH - GRID_SIZE):
            return True
        elif self.head.y < (GRID_SIZE) or self.head.y >= (HEIGHT - GRID_SIZE):
            return True
        i = 0
        for rect in self.segments:
            if i == 0:
                i += 1
                continue           
            if self.head.colliderect(rect):
                return True
        return False

class Food:
    points = 300
    def __init__(self):
        x = random.randrange(GRID_SIZE,(WIDTH-GRID_SIZE),GRID_SIZE)
        y = random.randrange(GRID_SIZE,(HEIGHT-GRID_SIZE),GRID_SIZE)
        self.rect = pygame.Rect(x, y, GRID_SIZE,GRID_SIZE)
        
        if DEBUG:
            print(f"New food generated at {x}, {y}")

    def draw(self):
        pygame.draw.circle(screen, "yellow", (self.rect.centerx, self.rect.centery) ,GRID_SIZE/2)

    def __update__(self):
        pass


pygame.init()
#variaveis do pygame
DEBUG = True
scaler=1
WIDTH = 480*scaler
HEIGHT = 416*scaler
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.Clock()
font = pygame.Font(size = 50)
running = True
game_over = False
dt = 0.0

score = 0

#funcionalidades do jogo

#checa se a comida vai spawnar em cima da cobra.
def spawn_food():
    newfood = Food()
    if newfood.rect.collidelist(snake.segments) == -1:
        return newfood
    else:
        del newfood
        return spawn_food()
    
#desenha grid: by Gemini
def draw_grid(surface, width, height, grid_size):
    grid_color = (40, 40, 40)  # Dark gray so it doesn't distract from the game

    # Draw vertical lines (X axis)
    for x in range(0, width, grid_size):
        pygame.draw.line(surface, grid_color, (x, 0), (x, height))

    # Draw horizontal lines (Y axis)
    for y in range(0, height, grid_size):
        pygame.draw.line(surface, grid_color, (0, y), (width, y))

#constantes do jogo
GRID_SIZE = 32
timer1 = 0.0

#inicializar objetos
snake = Snake()

food = spawn_food()


while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction[1] == 0:
                snake.direction = [0, -GRID_SIZE]
            if event.key == pygame.K_DOWN and snake.direction[1] == 0:
                snake.direction = [0, GRID_SIZE]
            if event.key == pygame.K_LEFT and snake.direction[0] == 0:
                snake.direction = [-GRID_SIZE, 0]
            if event.key == pygame.K_RIGHT and snake.direction[0] == 0:
                snake.direction = [GRID_SIZE, 0]

            if event.key == pygame.K_SPACE and game_over == True:
                snake.head.x=128
                snake.head.y=128
                score = 0
                game_over = False  
    
    #parte logica
    #processar o game over:

    if snake.is_dead() == True:
        game_over = True

    #colisao da cobra com a comida
    #BUG: a cobra move 1 vez a mais quando come
    if snake.segments[0].colliderect(food.rect):
        score += food.points
        del food
        snake.move(grow=True)
        food = spawn_food()

    #timer1: atualiza movimento da cobra
    timer1 += dt
    if timer1 >= 0.15 and not game_over:
        snake.move()
        timer1 = 0

    #parte grafica
    #pintar fundo de azul
    screen.fill("blue")

    #desenha um grid
    if DEBUG:
        draw_grid(screen, WIDTH, HEIGHT, GRID_SIZE)

    #draw dos objetos
    snake.draw()

    food.draw()

    if DEBUG == True:
        pygame.draw.rect(screen,"red",food.rect,2)
    #draw dos textos
    surface_score = font.render(f"SCORE: {score}", True, "green")
    screen.blit(surface_score)

    if game_over:
        surface_gameover = font.render("GAME OVER", True, "red")
        screen.blit(surface_gameover, (WIDTH/2-60 ,HEIGHT/2))

   #essa funcao joga tudo que foi desenhado na tela para o usuario ver.
    pygame.display.flip()

    #dt: o tempo em segundos de um frame
    dt = clock.tick(60) / 1000