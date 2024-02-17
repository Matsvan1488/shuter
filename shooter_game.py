#Створи власний Шутер!

from typing import Any

from pygame import *

from random import randint
font.init()
window = display.set_mode((700,500))
display.set_caption("Зоряні війни")
background = transform.scale(image.load("galaxy.jpg"),(700,500))

clock = time.Clock()
FPS = 60

bgcolor = "galaxy.jpg"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,width , heigth ,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, heigth))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed =  key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self):
        bulet = Bulet("bullet.png",self.rect.centerx,self.rect.y,25,50,-15)
        bulets.add(bulet)




class Enemy(GameSprite):
    def update(self):
        global lost, scor
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost += 1
        if sprite.spritecollide(self,bulets,True):
            scor += 1
            self.rect.y = 0
            self.rect.x = randint(80,620)
class Label():
    def set_text(self, text, size,color):
        letter = font.Font(None,size)
        self.image = letter.render(text,True, color)
    def drawing_image(self, shift_x = 0, shift_y = 0):
        window.blit(self.image,(shift_x, shift_y))




class Bulet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

score = Label()      
fight = Label()






air = Player("rocket.png",250,400,85,85,4)      
enemies = sprite.Group()
bulets =  sprite.Group()

for i in range(1,5):
    enemy= Enemy('ufo.png',randint(80,620), 0, 80,50, randint(3,5))
    enemies.add(enemy)

mixer.init()
mixer.music.load('space.ogg')

mixer.music.play()
south_fire = mixer.Sound("fire.ogg")
lost = 0
scor=0
finish = False
game =  True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                air.fire() 
                south_fire.play() 
    if finish != True:
        window.blit(background,(0,0))
        air.update()
        enemies.update()
        bulets.update()
        bulets.draw(window)

        air.reset()
        enemies.draw(window)

        score.set_text("Пропущено: "+str(lost), 30,(247, 250, 254))
        score.drawing_image(10,10) 

        fight.set_text("Збито: "+str(scor), 30,(247, 250, 254))
        fight.drawing_image(10,35) 
    # sprite.collidegroup(enemies, bulets,False,True)

    
        if   lost >= 30:
            lose =  Label()
            lose.set_text("You Lose", 100,(255,0,0))
            window.blit(background,(0,0))
            lose.drawing_image(200,200)
            finish = True
    if   scor >= 10:
        win =  Label()
        win.set_text("You WIN", 100,(255,255,0))
        window.blit(background,(0,0))
           
        win.drawing_image(200,200)
        finish = True




    
    display.flip()
    clock.tick(FPS)