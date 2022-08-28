from pygame import *
from random import *

hight_win = 800
widght_win = 1200
widght_Gera = 40

wight_enemy = 70

total_score = 0

mod_fire = 1

Enemy_amount = 5

font.init()
font1 = font.Font(None, 36)
font2 = font.SysFont('corbel', 30)
print(font.get_fonts())
Met = 1

#классы
class gamesprite(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y, pl_speed, pl_height, pl_widght):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (pl_height, pl_widght))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.name_image = pl_image

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def change_im(self, picture):
        self.image = transform.scale(image.load(picture), (self.rect.width, self.rect.height))
        self.name_image = picture




class player(gamesprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_d] and self.rect.x:
            self.rect.x += self.speed

        if keys[K_a] and self.rect.x:
            self.rect.x -= self.speed
    def fire(self, update_level):
        if update_level == 1:

            bullets.add(Fire('image/shot.png', self.rect.centerx, self.rect.top, 5, 20, 30))
        if update_level == 2:
            bullets.add(Fire('image/shot.png', self.rect.centerx + 10, self.rect.top, 5, 20, 30))
            bullets.add(Fire('image/shot.png', self.rect.centerx - 10, self.rect.top, 5, 20, 30))
        if update_level == 3:
            bullets.add(Fire('image/shot.png', self.rect.centerx + 10, self.rect.top, 5, 20, 30))
            bullets.add(Fire('image/shot.png', self.rect.centerx - 10, self.rect.top, 5, 20, 30))
            bullets.add(Fire('image/shot.png', self.rect.centerx + 30, self.rect.top, 5, 20, 30))



class Enemy(gamesprite):
    def update(self):

        self.rect.y += self.speed
        if self.rect.y > hight_win:
            self.rect.y = randint(-300, 0)
            self.rect.x = randint(0, widght_win - self.rect.width)

class Fire(gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Bonus(gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.kill()

class Meteor(gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.kill()


def m_restart():
    global total_score
    total_score = 0
    global mod_fire
    gr_bonus.empty()
    ye_bonus.empty()
    meteorit.empty()
    Enemies.empty()
    mod_fire = 1
    hero.change_im('image/spaceshatel.png')

#создание окна
window = display.set_mode((widght_win, hight_win))

display.set_caption("звёздные войны")
background = transform.scale(image.load("image/background.png"), (widght_win, hight_win))



clock = time.Clock()
FPS = 60
#подлючение музыки
mixer.init()
mixer.music.load('image/voice_space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

fire_sound = mixer.Sound('image/shotgun.ogg')
fire_sound.set_volume(0.1)






#создание групп спрайтов
Enemies = sprite.Group()
bullets = sprite.Group()
gr_bonus = sprite.Group()
ye_bonus = sprite.Group()
meteorit = sprite.Group()
#создание персонажа и врагов
hero = player('image/spaceshatel.png', 370, 600, 5, 100, 150)
for i in range(5):

    Enemies.add(Enemy('image/enemyship.png', randint(0, widght_win - wight_enemy) - 100, randint(0, 1000) * -1, randint(3, 5), wight_enemy, wight_enemy))



#логика программы
game = True
stop_game = False

while game:
    if stop_game:
        end_score2 = font2.render('Score: ' + str(total_score), 1, (250, 255, 0))
        end_score = font2.render('if you want to restart the game press << Space >>',  1, (250, 255, 0))
        window.blit(end_score, (200, 395))
        window.blit(end_score2, (250, 350))

        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    stop_game = False



        m_restart()

        display.update()
        clock.tick(FPS)
    else:



        window.blit(background, (0, 0))
        hero.update()
        hero.reset()

        Enemies.draw(window)
        Enemies.update()

        bullets.draw(window)
        bullets.update()

        gr_bonus.draw(window)
        gr_bonus.update()

        ye_bonus.draw(window)
        ye_bonus.update()

        meteorit.draw(window)
        meteorit.update()

        #проверка на столкновение 1
        collides = sprite.groupcollide(Enemies, bullets, True, True)

        for i in collides:
            if randint(1, 2):
                enemy_size = randint(1, 50)
            else:
                enemy_size = 0
            Enemies.add(Enemy('image/enemyship.png', randint(0, widght_win - wight_enemy) - 100, randint(0, 1000) * -1,
                              randint(3, 5), wight_enemy + enemy_size, wight_enemy + enemy_size))
            total_score += 1



            #создание бонусов
            if 0 < randint(1, 10) < 3:

                    gr_bonus.add(Bonus('image/green_star.png', i.rect.x, i.rect.y, 3, 50, 50))

            if 0 < randint(1, 10) < 5:

                    ye_bonus.add(Bonus('image/etllow_star.png', i.rect.x, i.rect.y, 3, 50, 50))


        #проверка столкновение 2
        if sprite.spritecollide(hero, Enemies, True):
            print(len(Enemies))
            print(hero.image)
            if hero.name_image == 'image/safetyshatel.png':
                hero.change_im('image/spaceshatel.png')
                pass
            else:
                stop_game = True



                print('ok')





        while len(Enemies) != Enemy_amount:
            Enemies.add(Enemy('image/enemyship.png', randint(0, widght_win - wight_enemy) - 100, randint(0, 1000) * -1, randint(3, 5), wight_enemy, wight_enemy))

        if total_score >= 2:
            while len(meteorit) != Met:
                meteor_size = randint(1, 50)
                if randint(1, 2) == 1:
                    meteorit.add(Meteor('image/stone.png', randint(0, widght_win - widght_Gera) - 100, randint(0, 1000) * -1,
                                  randint(3, 5), widght_Gera + meteor_size, widght_Gera + meteor_size))
                else:

                    meteorit.add(
                        Meteor('image/spacestone.png', randint(0, widght_win - widght_Gera) - 100, randint(0, 1000) * -1,
                               randint(3, 5), widght_Gera + meteor_size, widght_Gera + meteor_size))





        if sprite.spritecollide(hero, meteorit, True):
            game = False


        if sprite.spritecollide(hero, gr_bonus, True):
            if mod_fire != 3:

                mod_fire += 1

        if sprite.spritecollide(hero, ye_bonus, True):
            hero.change_im('image/safetyshatel.png')


        #if total_score >= 20:
            #mixer.music.stop()
            #mixer.music.load('image/scarysound.ogg')
            #mixer.music.set_volume(0.3)
            #mixer.music.play(-1)




        #создание счетчика убийств
        text_score = font1.render('Убито: ' + str(total_score), 1, (255, 255, 255))
        window.blit(text_score, (10, 10))






        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    fire_sound.play()
                    hero.fire(mod_fire)


        display.update()
        clock.tick(FPS)