
import pygame
import pygame.locals


pygame.init()

# константы кода
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PADDING_Y = 50
FPS = 60

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
    pass

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
    
    # создание подвижного игрового фона
    screen.blit(background, (0 - background_scroll, 0))
    screen.blit(background, (SCREEN_WIDTH - background_scroll, 0))
    background_scroll += 1

    if background_scroll == SCREEN_WIDTH:
        background_scroll = 0

    # изображение персонажа
    player_grp.update()
    player_grp.draw(screen)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()


