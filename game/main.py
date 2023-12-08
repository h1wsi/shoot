
import pygame
import pygame.mixer
import random
import time
from pygame.locals import K_UP, K_DOWN, K_SPACE, K_y, K_n, K_LEFT, K_RIGHT, K_ESCAPE

pygame.init()

# константы кода
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# отступы от верхней и нижей частей экрана
PADDING_X = 10
PADDING_Y = 50
FPS = 60
# установка минимальной разницы во времени между двумя выстрелами
CORE_TIMER = 500

# wav
core_sound = pygame.mixer.Sound("src/wav/shoot.wav")
game_sound = pygame.mixer.Sound("src/wav/game_wav.wav")
gameover_sound = pygame.mixer.Sound("src/wav/game_over.wav")

core_sound.set_volume(0.9)
game_sound.set_volume(0.6)

last_core = pygame.time.get_ticks()
new_bird = pygame.time.get_ticks()
new_rocket = pygame.time.get_ticks()

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

# Обработка изображений самолета
rocket_image = pygame.image.load('src/rocket.png').convert_alpha()
rocket_image = resize(rocket_image, 60)

plane_images = []

plane_primary = pygame.image.load('src/plane1.png').convert_alpha()
plane_secondary = pygame.image.load('src/plane2.png').convert_alpha()
plane_primary = resize(plane_primary, 70)
plane_secondary = resize(plane_secondary, 70)

plane_images.append(plane_primary)
plane_images.append(plane_secondary)

# Обработка изображений птиц
colors = ['pink', 'grey', 'yellow']
bird_images = {}

for bird in colors:
    bird_images[bird] = []

    for i in range(1, 3):
        bird_image = pygame.image.load(f'src/{bird}{i}.png').convert_alpha()
        bird_image = resize(bird_image, 50)

        bird_image = pygame.transform.flip(bird_image, True, False)
        bird_images[bird].append(bird_image)

# Обработка изображений сердечек
heart_images = []
heart_image_index = 0

for i in range(8):
    heart_image = pygame.image.load(f"src/lives/heart{i}.png").convert_alpha()
    heart_image = resize(heart_image, 30)
    heart_images.append(heart_image)


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

        if pygame.sprite.spritecollide(self, rocket_grp, True):
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
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.x_position = SCREEN_WIDTH

        # определение рандомной координаты появления птицы и рандомного цвета
        self.y_position = random.randint(PADDING_Y, SCREEN_HEIGHT - PADDING_Y * 2)
        self.color = random.choice(colors)

        self.image_index = 0
        self.image = bird_images[self.color][self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_position
        self.rect.y = self.y_position

    def update(self):

        self.x_position -= 2
        # анимирование птицы за счет индекса
        self.image_index += 0.25

        if self.image_index >= len(bird_images[self.color]):
            self.image_index = 0

        self.image = bird_images[self.color][int(self.image_index)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_position
        self.rect.y = self.y_position

        # проверка столкновения пули и птицы
        if pygame.sprite.spritecollide(self, core_grp, True):
            self.kill()
            player.score += 10

        if self.x_position < 0:
            self.kill()

class Rocket(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.x_position = SCREEN_WIDTH
        # определение рандомной координаты появления ракеты 
        self.y_position = random.randint(PADDING_Y, SCREEN_HEIGHT - PADDING_Y * 2)

        self.image = rocket_image
        self.rect = self.image.get_rect()
        self.rect.x = self.x_position
        self.rect.y = self.y_position

        # определение рандомной скорости ракеты
        self.speed = random.randint(3, 5)

    def update(self):
        self.x_position -= self.speed
        self.rect = self.image.get_rect()
        self.rect.x = self.x_position
        self.rect.y = self.y_position

        # проверка столкновения пули и ракеты
        if pygame.sprite.spritecollide(self, core_grp, True):
            self.kill()
            player.score += 20
        if self.x_position < 0:
            self.kill()

# создани  паузы
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Создание групп персонажей
player_grp = pygame.sprite.Group()
core_grp = pygame.sprite.Group()
bird_grp = pygame.sprite.Group()
rocket_grp = pygame.sprite.Group()

# Инициализация персонажа
x_player_position = 30
y_player_position = SCREEN_HEIGHT // 2

player = Player(x_player_position, y_player_position)
player_grp.add(player)

# Создание цикла игры
run_game = True
while run_game:

    game_sound.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    
    keys = pygame.key.get_pressed()

    if keys[K_ESCAPE]: 
        pause()
        
    # взаимодействие с моделькой игрока через клавиатуру
    if keys[K_UP] and player.rect.top > PADDING_Y:
        player.y_position -= 2
        player.image_angle = 15
    elif keys[K_DOWN] and player.rect.bottom < SCREEN_HEIGHT - PADDING_Y:
        player.y_position += 2
        player.image_angle = -15

    elif keys[K_RIGHT] and player.rect.right < SCREEN_WIDTH - PADDING_X: 
        player.x_position += 2 
        player.image_angle = 0 
    elif keys[K_LEFT] and player.rect.left > PADDING_X: 
        player.x_position -= 2 
        player.image_angle = 0

    # выстрел посредством нажатия на пробел, реализация движения  пули
    if keys[K_SPACE] and last_core + CORE_TIMER < pygame.time.get_ticks():
        
        core_sound.play()
        x_core_position = player.x_position + player.image.get_width()
        y_core_position = player.y_position + player.image.get_height() // 2
        core = Core(x_core_position, y_core_position)
        core_grp.add(core)

        last_core = pygame.time.get_ticks()
    
    # создание птицы и реализация рандомного появления 
    # в промежутке от 0 до 1 секунд

    if new_bird < pygame.time.get_ticks():
        bird = Bird()
        bird_grp.add(bird)
    new_bird = random.randint(pygame.time.get_ticks(), pygame.time.get_ticks() + 1000)

    # создание ракеты и реализация рандомного появления 
    # в промежутке от 2 до 5 секунд
    if new_rocket < pygame.time.get_ticks():
        rocket = Rocket()
        rocket_grp.add(rocket)
    new_rocket = random.randint(pygame.time.get_ticks() + 2000, pygame.time.get_ticks() + 5000)

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
    
    # изображение птицы
    bird_grp.update()
    bird_grp.draw(screen)

    # изображение ракеты
    rocket_grp.update()
    rocket_grp.draw(screen)

    # отображение жизней
    for i in range(player.lives):
        heart_image = heart_images[int(heart_image_index)]
        heart_x_position = 10 + i * (heart_image.get_width() + 10)
        heart_y_position = 10
        screen.blit(heart_image, (heart_x_position, heart_y_position))

    # эффект блеска
    heart_image_index += 0.049
    if heart_image_index >= len(heart_images):
        heart_image_index = 0

    # отображение очков
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    score_text = font.render(f'Score: {player.score}', True, 'white')

    text_rect = score_text.get_rect()
    text_rect.center = (200, 25)
    screen.blit(score_text, text_rect)

    # проверка того, что игра закончена
    while player.lives == 0:
        game_sound.stop()
        gameover_sound.play()
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill('black')
        gameover_str = 'Play again (print Y or N)?'
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        end_text = font.render(gameover_str, True, 'white')
        text_rect = end_text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(end_text, text_rect)

        pygame.display.flip() # обновляем экран

        keys = pygame.key.get_pressed()
        if keys[K_y]:
            # clear the sprite groups
            player_grp.empty()
            core_grp.empty()
            bird_grp.empty()

            # сброс игрока
            player = Player(x_player_position, y_player_position)
            player_grp.add(player)

        elif keys[K_n]:

            screen.fill('black')
            font = pygame.font.Font(pygame.font.get_default_font(), 20)
            score_text = font.render(f"Your score result: {player.score}", True, 'white')

            text_rect = score_text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(score_text, text_rect)

            pygame.display.flip()
            time.sleep(3)

            run_game = False
            break
    
    pygame.display.update()

pygame.quit()
