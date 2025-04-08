from pygame import *
import random

# Инициализация Pygame
init()
mixer.init()

# Окно игры
window = display.set_mode((700, 500))
display.set_caption('Пинг Понг')

# Шрифты
font = font.SysFont(None, 36)

# Фон
background = transform.scale(image.load("Ping.png"), (700, 500))

# Глобальные переменные
missed_ufos = 0
destroyed_ufos = 0
game_result = None  # None, "win", "lose"


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
        if keys[K_UP] and self.rect.y > 0:  # Изменено на K_UP для управления стрелками
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430:  # Изменено на K_DOWN для управления стрелками
            self.rect.y += self.speed


player1 = Player("Redrocket.png", 30, 250, 5)
player2 = Player("Bluerocket.png", 670, 250, 5)

clock = time.Clock()
running = True

while running:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            running = False

    player1.update1()  # Обновляем позицию первого игрока
    player2.update2()  # Обновляем позицию второго игрока

    player1.reset()  # Отрисовываем первого игрока
    player2.reset()  # Отрисовываем второго игрока

    display.update()
    clock.tick(60)

# Экран окончания игры
game_over = True
while game_over:
    for e in event.get():
        if e.type == QUIT:
            game_over = False

    window.blit(background, (0, 0))

    # Здесь можно добавить логику отображения результата игры

    display.update()
    clock.tick(60)
