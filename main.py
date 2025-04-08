from pygame import *
import random

# Инициализация Pygame
init()
mixer.init()

# Окно игры
window = display.set_mode((700, 500))
display.set_caption('Пинг Понг')

# Шрифты
font = font.SysFont(None, 52)

# Фон
background = transform.scale(image.load("Ping.png"), (700, 500))

# Глобальные переменные
missed_ufos = 0
destroyed_ufos = 0
game_result = None  # None, "win", "lose"
score1 = 0
score2 = 0


class GameSprite(sprite.Sprite):
    def __init__(self, image_path, x, y, speed, size=(30, 120)):
        super().__init__()
        self.image = transform.scale(image.load(image_path), size)
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y))

    def reset(self):
        window.blit(self.image, self.rect.topleft)


class Player(GameSprite):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed)
        self.bullet_available = True

    def update1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 430:
            self.rect.y += self.speed

    def update2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self, image_path, x, y, speed_x, speed_y):
        super().__init__(image_path, x, y, speed=0,size=(100, 80))  # Скорость не используется в GameSprite
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        # Двигаем мяч
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Проверка на столкновение со стенами
        if self.rect.top <= 0 or self.rect.bottom >= 500:  # Верхняя и нижняя границы окна
            self.speed_y *= -1  # Изменяем направление по Y

        # Проверка выхода за границы экрана по X (для подсчета очков)
        if self.rect.left <= 0:  # Если мяч выходит за левую границу (игрок 2 забивает)
            global score2
            score2 += 1
            self.reset_position()  # Сброс позиции мяча

        if self.rect.right >= 700:  # Если мяч выходит за правую границу (игрок 1 забивает)
            global score1
            score1 += 1
            self.reset_position()  # Сброс позиции мяча

    def reset_position(self):
        # Сбрасываем позицию мяча в центр экрана и задаем случайную скорость
        self.rect.center = (350, 250)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


player1 = Player("Redrocket.png", 30, 250, 5)
player2 = Player("Bluerocket.png", 670, 250, 5)
ball = Ball("Ball.png", 350, 250, random.choice([-5, 5]), random.choice([-5, 5]))

clock = time.Clock()
running = True

while running:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            running = False

    player1.update1()
    player2.update2()
    ball.update()

    # Проверка на столкновение мяча с ракетками
    if sprite.collide_rect(ball, player1) or sprite.collide_rect(ball, player2):
        ball.speed_x *= -1

    player1.reset()
    player2.reset()
    ball.reset()

    # Отображение счета на экране
    score_text = font.render(f"{score1}:{score2}", True,(255 ,255 ,255))
    text_x = (700 - score_text.get_width()) // 2  # Центрируем по ширине окна
    text_y = (500 - score_text.get_height()) // 2  # Центрируем по высоте окна
    window.blit(score_text, (text_x, text_y))


    display.update()
    clock.tick(60)

# Экран окончания игры
game_over = True
while game_over:
    for e in event.get():
        if e.type == QUIT:
            game_over = False

    window.blit(background,(0 ,0))

    display.update()
    clock.tick(60)
