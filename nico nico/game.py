import time as t
from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, x_cor, y_cor, width, height, speed, player_image):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < fon_height - 150:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < fon_height - 150:
            self.rect.y += self.speed


fon_height = 500
fon_width = 700
background = transform.scale(image.load("fon.jpg"), (fon_width, fon_height))
window = display.set_mode((fon_width, fon_height))
window.blit(background, (0, 0))

timer = time.Clock()

mixer.init()
mixer.music.load("music.mp3")

mixer.music.play(loops=-1)
lose_sound = mixer.Sound("lose.ogg")
racket_sound = mixer.Sound("racketkick.ogg")
wall_sound = mixer.Sound("wallkick.ogg")

font.init()
game_font = font.SysFont('Times New Roman', 48)
lose_left = game_font.render('2 игрок выиграл', True, (180, 0, 0))
lose_right = game_font.render('1 игрок выиграл', True, (180, 0, 0))

font.init()
font = font.Font(None, 35)
lose1 = font.render('2 игрок победил', True, (180, 0, 0))
lose2 = font.render('1 игрок победил', True, (180, 0, 0))

font_image = "fon.jpg"
racket_image = "racket.png"
ball_image = "ball.png"

ball_speed_x = 10
ball_speed_y = 10

ball = GameSprite(350, 250, 50, 50, 10, ball_image)
racket_left = Player(30, 200, 50, 150, 10, racket_image)
racket_right = Player(620, 200, 50, 150, 10, racket_image)

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))

        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y
        racket_left.update_left()
        racket_right.update_right()

        if ball.rect.y < 5 or ball.rect.y > fon_height - 50:
            ball_speed_y *= -1
            wall_sound.play()

        if sprite.collide_rect(ball, racket_left) or sprite.collide_rect(ball, racket_right):
            ball_speed_x *= -1
            racket_sound.play()
            

        if ball.rect.x < racket_left.rect.x - 30:
            window.blit(lose_left, (200, 200))
            lose_sound.play()
            finish=True            

        if ball.rect.x > racket_right.rect.x + 30:
            window.blit(lose_right, (200, 200))
            lose_sound.play()
            finish=True


        ball.reset()
        racket_left.reset()
        racket_right.reset()
    
    else:
        t.sleep(2)
        finish = False
        ball.kill()
        ball = GameSprite(350, 250, 50, 50, 10, ball_image)



    display.update()
    time.delay(50)