
import pygame
from pygame.locals import K_UP, K_DOWN, K_SPACE

pygame.init()

# константы кода
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# отступы от верхней и нижей частей экрана
PADDING_Y = 50
FPS = 60
# установка минимальной разницы во времени между двумя выстрелами
CORE_TIMER = 500

last_core = pygame.time.get_ticks()
clock = pygame.time.Clock()

# функция для изменения размера изображения
def resize(image, new_width):
    temp_image = new_width / image.get_rect().width
    new_height = image.get_rect().height * temp_image
    new_size = (new_width, new_height)

    return pygame.transform.scale(image, new_size)


# создание игрового окна
screen = pygame.display.set_mode(SIZE)
background = pygame.image.load('src/background.png').convert_alpha()
background_scroll = 0

plane_images = []

plane_primary = pygame.image.load('src/plane1.png').convert_alpha()
plane_secondary = pygame.image.load('src/plane2.png').convert_alpha()
plane_primary = resize(plane_primary, 70)
plane_secondary = resize(plane_secondary, 70)

plane_images.append(plane_primary)
plane_images.append(plane_secondary)

# Класс для создания модели игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):

        pygame.sprite.Sprite.__init__(self)
        self.x_position = x_position
        self.y_position = y_position

        self.lives = 3
        self.score = 0
        self.image_index = 0
        self.image_angle = 0
    
    # обновление состояния объекта 
    def update(self):
        self.image_index += 1
        if self.image_index >= len(plane_images):
            self.image_index = 0
        
        self.image = plane_images[self.image_index]
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, self.image_angle)
        self.rect.x= self.x_position
        self.rect.y= self.y_position

        # проверка столкновения персонажа с птицей
        if pygame.sprite.spritecollide(self, bird_grp, True):
            self.lives -= 1

# Класс для создания выстрела
class Core(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):

        pygame.sprite.Sprite.__init__(self)
        self.x_position = x_position
        self.y_position = y_position

        self.radius = 5
        self.rect = pygame.rect.Rect(x_position, y_position, 10, 10)

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.x_position, self.y_position), self.radius)

    # реализация движения пули и удаления ее при достижении края игрового окна
    def update(self):
        self.x_position += 2
        self.rect.x = self.x_position
        self.rect.y = self.y_position

        if self.x_position > SCREEN_WIDTH:
            self.kill()

# Класс для создания персонажей типа Bird
class Bird(pygame.sprite.Sprite):
    pass

# Создание групп персонажей
player_grp = pygame.sprite.Group()
core_grp = pygame.sprite.Group()
bird_grp = pygame.sprite.Group()

# Инициализация персонажа
x_player_position = 30
y_player_position = SCREEN_HEIGHT // 2

player = Player(x_player_position, y_player_position)
player_grp.add(player)

# Создание цикла игры
run_game = True
while run_game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    
    keys = pygame.key.get_pressed()

    # взаимодействие с моделькой игрока через клавиатуру
    if keys[K_UP] and player.rect.top > PADDING_Y:
        player.y_position -= 2
        player.image_angle = 15
    elif keys[K_DOWN] and player.rect.bottom < SCREEN_HEIGHT - PADDING_Y:
        player.y_position += 2
        player.image_angle = -15

    # выстрел посредством нажатия на пробел, реализация движения  пули
    if keys[K_SPACE] and last_core + CORE_TIMER < pygame.time.get_ticks():
        x_core_position = player.x_position + player.image.get_width()
        y_core_position = player.y_position + player.image.get_height() // 2
        core = Core(x_core_position, y_core_position)
        core_grp.add(core)

        last_core = pygame.time.get_ticks()

    # создание подвижного игрового фона
    screen.blit(background, (0 - background_scroll, 0))
    screen.blit(background, (SCREEN_WIDTH - background_scroll, 0))
    background_scroll += 1

    if background_scroll == SCREEN_WIDTH:
        background_scroll = 0

    # изображение персонажа
    player_grp.update()
    player_grp.draw(screen)
    
    # отображение пули
    core_grp.update()
    for core in core_grp:
        core.draw()

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()


