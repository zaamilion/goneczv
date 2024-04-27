
import pygame
import random

#инициализация Pygame
pygame.init()

#константы-параметры окна
WIDTH = 800
HEIGHT = 600
#константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

#класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #создание изображения для спрайта
        self.images_right = [pygame.image.load(f'{name}') for name in ['char.png', 'char1.png']]
        self.images_left = [pygame.image.load(f'{name}') for name in ['chal.png', 'chal1.png']]
        self.current_images = self.images_right
        self.image = self.current_images[0]
        self.image_index = 0
        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #компоненты скорости по оси X и Y
        self.x_velocity = 0
        self.y_velocity = 0

        #переменная-флаг для отслеживания в прыжке ли спрайт
        self.on_ground = False

        # на коне ли
        self.on_horse = False 
        self.health = 3

    def update(self):
        # Обновление позиции игрока
        if not self.on_horse:
            self.image_index %= len(self.current_images)
            if self.x_velocity > 0 and self.current_images != self.images_left:
                self.current_images = self.images_left
                self.image_index = 0
                self.image = self.current_images[0]
            elif self.x_velocity < 0 and self.current_images != self.images_right:
                self.current_images = self.images_right
                self.image_index = 0 
                self.image = self.current_images[0]
            elif self.x_velocity != 0:
                self.image = self.current_images[self.image_index]

#класс коня
class Horse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #создание изображения для спрайта
        self.images_right = [pygame.transform.scale(pygame.image.load(f'{name}'), (150, 120)) for name in ['коньр1.png', 'коньр.png']]
        self.images_left = [pygame.transform.scale(pygame.image.load(f'{name}'), (150, 120)) for name in ['коньр.png', 'коньр.png']]
        self.current_images = self.images_right
        self.image = self.current_images[0]
        self.image_index = 0
        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #компоненты скорости по оси X и Y
        self.x_velocity = 0
        self.y_velocity = 0

        #переменная-флаг для отслеживания в прыжке ли спрайт
        self.on_ground = False
    
    def update(self):
        # Обновление позиции horse
        self.image_index %= len(self.current_images)
        if self.x_velocity > 0 and self.current_images != self.images_left:
            self.current_images = self.images_left
            self.image_index = 0
            self.image = self.current_images[0]
        elif self.x_velocity < 0 and self.current_images != self.images_right:
            self.current_images = self.images_right
            self.image_index = 0 
            self.image = self.current_images[0]
        elif self.x_velocity != 0:
            self.image = self.current_images[self.image_index]
#класс для патрулирующих врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #создание изображения для спрайта
        self.image = pygame.Surface((32, 32))
        self.image.fill(RED)

        #начальная позиция по Х, нужна для патрулирования
        self.x_start = x
        #выбор направления начального движения
        self.direction = random.choice([-1, 1])

        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #компоненты скорости по оси Х и Y
        self.x_velocity = 1
        self.y_velocity = 0
    
    def update(self):
        #если расстояние от начальной точки превысило 50
        #то меняем направление
        if abs(self.x_start - self.rect.x) > 50:
            self.direction *= -1

        #движение спрайта по оси Х
        self.rect.x += self.x_velocity * self.direction

#класс для поднимаемых предметов
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #создание изображения для спрайта
        self.image = pygame.Surface((16, 16))
        self.image.fill(GOLD)

        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#класс для платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        #создание изображения для спрайта
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)

        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#функция для проверки коллизий c платформой
def check_collision_platforms(object, platform_list):
    #перебираем все платформы из списка (не группы спрайтов)
    for platform in platform_list:
        if object.rect.colliderect(platform.rect):
            if object.y_velocity > 0: # Если спрайт падает
                #меняем переменную-флаг
                object.on_ground = True
                #ставим его поверх платформы и сбрасываем скорость по оси Y
                object.rect.bottom = platform.rect.top
                object.y_velocity = 0
            elif object.y_velocity < 0: # Если спрайт движется вверх
                #ставим спрайт снизу платформы
                object.rect.top = platform.rect.bottom
                object.y_velocity = 0
            elif object.x_velocity > 0: # Если спрайт движется вправо
                #ставим спрайт слева от платформы
                object.rect.right = platform.rect.left
            elif object.x_velocity < 0: # Если спрайт движется влево
                #ставим спрайт справа от платформы
                object.rect.left = platform.rect.right

def check_collision_enemies(player, enemies_list):
    # running здесь больше не нужен
    global score

    # При столкновении игрока с врагом
    for enemy in enemies_list:
        if player.rect.colliderect(enemy.rect):
            # Уменьшаем здоровье игрока
            player.health -= 1
            # Удаляем врага из списка и всех групп
            enemy.kill()
            enemies_list.remove(enemy)
            # Если здоровье игрока равно 0, завершаем игру
            if player.health <= 0:
                running = False

#функция проверки коллизии выбранного объекта с объектами Enemies
def check_collision_enemies(object, enemies_list):
    global running, death_frame, death_last_frame
    #running делаем видимой внутри функции чтобы было возможно
    #завершить игру
    #в списке проверяем
    for enemy in enemies_list:
        #при коллизии
        if object.rect.colliderect(enemy.rect) and death_last_frame + 10 < death_frame:
            death_last_frame = 10
            death_frame = 0
            object.health -= 1
            if object.health < 1:
                object.kill()
                running = False
            return None
def draw_health(player):
    heart_image = pygame.transform.scale(pygame.image.load('heart.png'), (20,20))  # Загружаем изображение для сердца
    for i in range(player.health):
        screen.blit(heart_image, (10 + i * 30, 10))  # Выводим сердца в левом верхнем углу экрана

#проверка 
def check_collision_collectibles(object):
    #делаем видимыми объекты для подбора в игре и очки
    global collectibles_list
    global score
    #если object касается collictible 
    for collectible in collectibles_list:
        if object.rect.colliderect(collectible.rect):
            #убираем этот объект из всех групп
            collectible.kill()
            #убираем этот объект из списка (чтобы не было проверки коллизии)
            collectibles_list.remove(collectible)
            #прибавляем одно очко
            score += 1


#создаем экран, счетчик частоты кадров и очков
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
score = 0
frame = 0
#создаем игрока, платформы, врагов и то, что будем собирать в игре
player = Player(50, 50)
platforms_list = [Platform(0, HEIGHT-25, WIDTH, 50), Platform(50, 150, 100, 20), Platform(100, 350, 100, 20), Platform(250, 170, 100, 20)]
enemies_list = [Enemy(120, 315)]
collectibles_list = [Collectible(280, 135)]
horse = Horse(500,100)
#счёт игры
font = pygame.font.Font(None, 36) # создание объекта, выбор размера шрифта
score_text = font.render("Счёт: 0", True, BLACK) # выбор цвета и текст
score_rect = score_text.get_rect() # создание хитбокса текста
score_rect.topleft = (WIDTH // 2, 100) # расположение хитбокса\текста на экране

#создаем групп спрайтов
player_and_platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

#в трех циклах добавляем объекты в соответствующие группы
for i in enemies_list:
    enemies.add(i)

for i in platforms_list:
    player_and_platforms.add(i)

for i in collectibles_list:
    collectibles.add(i)
player_and_platforms.add(horse)

background_sprite = pygame.image.load('back.png')
#отдельно добавляем игрока
player_and_platforms.add(player)
camera_x, camera_y = -3600,0
#игровой цикл
running = True
frame = 0
click_frame = 0
death_frame = 0
death_last_frame = 0
last_click_frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #проверяем нажатие на клавиши для перемещения
    click_frame = (click_frame + 0.1)
    death_frame += 1
    keys = pygame.key.get_pressed()
    player.x_velocity = 0
    horse.x_velocity = 0
    last_click_frame = 0
    if keys[pygame.K_a]:
        if not player.on_horse:
            if player.on_ground == False:
                player.x_velocity = -2
            else:
                player.x_velocity = -3
        else:
            if horse.on_ground == False:
                horse.x_velocity = -4
            else:
                horse.x_velocity = -6
    if keys[pygame.K_d]:
        if not player.on_horse:
            if player.on_ground == False:
                player.x_velocity = 2
            else:
                player.x_velocity = 3
        else:
            if horse.on_ground == False:
                horse.x_velocity = 4
            else:
                horse.x_velocity = 6
    if keys[pygame.K_e]:
        if -80 < player.rect.x - horse.rect.x < 80 and -80 < player.rect.y - horse.rect.y < 80:
            print(last_click_frame + 6, click_frame)
            if not player.on_horse and last_click_frame + 6 < click_frame:
                last_click_frame = click_frame
                click_frame = 0
                player.on_horse = True
                print(player.on_horse)
                player.rect.x = horse.rect.x + 50
                player.rect.y = horse.rect.y + 20
            elif player.on_horse and last_click_frame + 6 < click_frame:
                last_click_frame = 0
                click_frame = 0
                player.on_horse = False
                player.rect.x = horse.rect.x + 20
                player.rect.y = horse.rect.y
    #условие прыжка более сложное
    if keys[pygame.K_SPACE]:
        if player.on_horse and horse.on_ground:
            horse.y_velocity = -15
            horse.on_ground = False
        elif not player.on_horse and player.on_ground:
            player.y_velocity = -9
            player.on_ground = False

    #гравитация для игрока
    horse.y_velocity += 0.5
    player.y_velocity += 0.5
    frame = (frame + 1) % 60
    if frame % 10 == 0:
        player.image_index += 1
        horse.image_index += 1
    #обновляем значения атрибутов игрока и врагов
    player.update()
    enemies.update()
    horse.update()

    #отрисовываем фон, платформы, врагов и собираемые предметы
    if player.rect.x > screen.get_width() * 0.9 and (player.x_velocity > 0 if not player.on_horse else horse.x_velocity > 0):
        camera_x -= player.x_velocity if not player.on_horse else horse.x_velocity
        player.x_velocity = 0
        horse.x_velocity = 0
    elif player.rect.x < screen.get_width() / 10 and (player.x_velocity < 0 if not player.on_horse else horse.x_velocity < 0):
        camera_x -= player.x_velocity if not player.on_horse else horse.x_velocity
        player.x_velocity = 0
        horse.x_velocity = 0
    
    horse.rect.y += horse.y_velocity
    horse.rect.x += horse.x_velocity
    if not player.on_horse:
        player.rect.x += player.x_velocity
        player.rect.y += player.y_velocity
    else:
        player.rect.x = horse.rect.x + 50
        player.rect.y = horse.rect.y + 20
    screen.blit(background_sprite, (camera_x, camera_y))
    player_and_platforms.draw(screen)
    enemies.draw(screen)
    collectibles.draw(screen)
    #проверяем все возможные коллизии
    check_collision_platforms(horse, platforms_list)
    check_collision_platforms(player, platforms_list)
    check_collision_enemies(player, enemies_list)
    check_collision_collectibles(player)
    draw_health(player)
    #обновление счёта на экране
    score_text = font.render("Счёт: " + str(score), True, BLUE)
    screen.blit(score_text, score_rect)

    #обновление экрана и установка частоты кадров
    pygame.display.update()
    clock.tick(60)

pygame.quit()