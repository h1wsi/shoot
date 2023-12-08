
import pygame
import pygame.locals


pygame.init()

# константы кода
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PADDING_Y = 50
FPS = 60

# создание игрового окна
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Класс для создания модели игрока
class Player(pygame.sprite.Sprite):
    pass

# Класс для создания выстрела
class Core(pygame.sprite.Sprite):
    pass

# Класс для создания персонажей типа Bird
class Bird(pygame.sprite.Sprite):
    pass

# Создание групп персонажей
player_grp = pygame.sprite.Group()
core_grp = pygame.sprite.Group()
bird_grp = pygame.sprite.Group()

# Создание цикла игры
run_game = True
while run_game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            run_game = False
    
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()


