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
background = transform.scale(image.load("Sprites/Ping.png"), (700, 500))

play_button_image = transform.scale(image.load("Sprites/Play_button.jpg"), (230, 80))
play_button_rect = play_button_image.get_rect(center=(350, 250))  # Центрируем кнопку

BackHome_image = transform.scale(image.load("Sprites/BackHome_button.jpg"), (230, 70))
BackHome_rect = BackHome_image.get_rect(center=(350, 350))

oneVSone_button_image = transform.scale(image.load("Sprites/oneVSone_button.jpg"), (230, 70))
oneVSone_button_rect = oneVSone_button_image.get_rect(center=(550, 250))

trening_button_image = transform.scale(image.load("Sprites/trening_button.jpg"), (230, 70))
trening_button_rect = trening_button_image.get_rect(center=(150, 250))

# Глобальные переменные
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

    def update_trening(self):
        if self.rect.y < random.randint(0, 400):
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed


class Ball(GameSprite):
    def __init__(self, image_path, x, y, speed_x, speed_y):
        super().__init__(image_path, x, y, speed=0, size=(100, 80))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        # Двигаем мяч
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Проверка на столкновение со стенами
        if self.rect.top <= 0 or self.rect.bottom >= 500:
            self.speed_y *= -1

        # Проверка выхода за границы экрана по X (для подсчета очков)
        if self.rect.left <= 0:
            global score2
            score2 += 1
            self.reset_position()

        if self.rect.right >= 700:
            global score1
            score1 += 1
            self.reset_position()

    def update_trening(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхней и нижней стен
        if self.rect.top <= 0 or self.rect.bottom >= 500:
            self.speed_y *= -1

        # Отскок от правой стены
        if self.rect.right >= 700:
            self.speed_x *= -1

        # Если мяч вышел за левую границу — игрок проиграл очко
        if self.rect.left <= 0:
            global score2
            score2 += 1
            self.reset_position()

    def reset_position(self):
        self.rect.center = (350, 250)

        # Обеспечим ненулевую скорость по X
        self.speed_x = 0
        while self.speed_x == 0:
            self.speed_x = random.choice([-5, 5])

        # Обеспечим ненулевую скорость по Y
        self.speed_y = 0
        while self.speed_y == 0:
            self.speed_y = random.choice([-5, 5])
        print(self.speed_x, self.speed_y)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


def main_menu():
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

            # Обработка нажатия мыши для кнопки "Играть"
            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    return show_game_mode_selection()

        background_menu = transform.scale(image.load("Sprites/main_menu.png"), (700, 500))
        window.blit(background_menu, (0, 0))

        # Отображение кнопки "Играть"
        window.blit(play_button_image, play_button_rect)

        display.update()


def show_game_mode_selection():
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

            # Обработка нажатия мыши для выбора режима игры
            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                if oneVSone_button_rect.collidepoint(mouse_pos):
                    return start_game(mode='1vs1')
                elif trening_button_rect.collidepoint(mouse_pos):
                    return start_game(mode='trening')

        window.blit(background,(0 ,0))


        window.blit(oneVSone_button_image , oneVSone_button_rect)
        window.blit(trening_button_image , trening_button_rect)

        display.update()


def start_game(mode):
    global score1, score2
    print(mode)

    player1 = Player("Sprites/Redrocket.png", 30, 250, 5)

    if mode == '1vs1':
        player2 = Player("Sprites/Bluerocket.png", 670, 250, 5)

    ball = Ball("Sprites/Ball.png", 350, 250, random.choice([-5, 5]), random.choice([-5, 5]))
    clock = time.Clock()
    running = True

    while running:
        window.blit(background, (0, 0))

        for e in event.get():
            if e.type == QUIT:
                running = False

        player1.update1()

        if mode == '1vs1':
            player2.update2()
            ball.update()
            if sprite.collide_rect(ball, player1) or sprite.collide_rect(ball, player2):
                ball.speed_x *= -1

        elif mode == 'trening':

            ball.update_trening()
            if sprite.collide_rect(ball, player1):
                ball.speed_x *= -1

        player1.reset()

        if mode == '1vs1':
            player2.reset()

        ball.reset()

        # Отображение счёта
        score_text = font.render(f"{score1}:{score2}", True, (255, 255, 255))
        text_x = (700 - score_text.get_width()) // 2
        text_y = (500 - score_text.get_height()) // 2
        window.blit(score_text, (text_x, text_y))

        if score1 >= 5 or score2 >= 5:
            running = False

        display.update()
        clock.tick(60)

    game_over_screen()



def game_over_screen():
    while True:
       for e in event.get():
           if e.type == QUIT:
               quit()
               break

           if e.type == MOUSEBUTTONDOWN:
               mouse_pos=mouse.get_pos()
               if BackHome_rect.collidepoint(mouse_pos):
                   return True


       background=transform.scale(image.load("Sprites/main_menu.png"),(700 ,500))


       window.blit(background,(0 ,0))


       # Отображение текста "Игра окончена" в центре экрана
       text=font.render("Игра окончена",True,(255 ,255 ,255))


       text_x=(700 - text.get_width()) //2
       text_y=(400 - text.get_height()) //2


       window.blit(text,(text_x,text_y))


       # Отображение кнопки "Назад"
       window.blit(BackHome_image , BackHome_rect)


       display.update()


while True:
   main_menu()

   score1=0
   score2=0

# Завершение Pygame
quit()
