import pygame, utilities


class Block(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def onhit(self,object,direction = 0):
        if True:
            if direction == 0:
                object.rect.right = self.rect.left
                object.syncposx()
            if direction == 1:
                object.rect.left = self.rect.right
                object.syncposx()

            if direction == 2:
                object.rect.bottom = self.rect.top
                object.syncposy()
                if isinstance(object,Player):
                    object.grounded = True

            if direction == 3:
                object.rect.top = self.rect.bottom
                object.syncposy()
                if isinstance(object,Player):
                    object.jumptimer = 0


    def render(self):
            self.game.screen.blit(self.image,self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, game = None):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(0,0,16,16).inflate(-8,0)

        self.accel = 0
        self.maxaccel = 5
        self.speed = .9
        self.pos = self.rect.topleft


        self.game = game
        self.images = utilities.loadSpriteSheet(utilities.loadImage(self.game.game.image_dir,"noiboy.png",1),(16,16))
        self.idle_images_right = [self.images[0][0],self.images[0][1]]
        self.idle_images_left = utilities.flipimages(self.idle_images_right)
        self.run_images_right = [self.images[1][0], self.images[1][1], self.images[1][2], self.images[1][3]]
        self.run_images_left = utilities.flipimages(self.run_images_right)
        self.climbing_images_right = [self.images[2][0], self.images[2][1]]
        self.climbing_images_left = utilities.flipimages(self.climbing_images_right)
        self.image =self.idle_images_right[1]
        self.state = "idle"
        self.facing = "right"
        self.frame = 0
        self.grounded = False
        self.jumptimer = 0
        self.attached = False
        self.climbing_step = 0
        self.hurttimer = 0
        self.player = True
        self.dead = False
    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    def set_pos(self,x,y):
        self.rect.x = x
        self.rect.y = y
        self.syncpos()
    def syncrect(self):
        self.rect.topleft = self.pos
    def syncpos(self):
        self.pos = (self.rect.left,self.rect.top)
    def syncposx(self):
        self.pos = (self.rect.left,self.pos[1])
    def syncposy(self):
        self.pos = (self.pos[0],self.rect.top)


    def move_single_axis(self, dx, dy):

        # Move the rect
        if dx != 0:
            self.pos = (self.pos[0] + self.accel  * self.game.game.delta_time ,self.pos[1])
        if dy != 0:
            self.pos = (self.pos[0],self.pos[1] + dy * self.game.game.delta_time)
        self.syncrect()

        # If you collide with a wall, move out based on velocity
        for block in pygame.sprite.spritecollide(self ,self.game.collision_group,False):
            if dx > 0:
                block.onhit(self,0)
            if dx < 0:
                block.onhit(self,1)
            if dy > 0:
                block.onhit(self,2)
            if dy < 0:
                block.onhit(self,3)
    def hurt(self):
        if self.hurttimer == 0:
            self.jumptimer = 6
            self.hurttimer = 30
            self.dead = True

    def update(self):
        self.frame += 1

        if self.accel < 0:
            if self.grounded:
                self.accel += .5
            else:
                self.accel += .2
        if self.accel > 0:
            if self.grounded:
                self.accel -= .5
            else:
                self.accel -= .2
        if self.accel < .4  and self.accel > -.4:
            self.accel = 0
        if self. accel > self.maxaccel:
            self.accel = self.maxaccel
        if self.accel < -self.maxaccel:
            self.accel = -self.maxaccel
        self.maxaccel = 5


        if self.facing == "right":
            if self.state == "idle":
                self.image = self.idle_images_right[int(self.frame / 15 % 2)]
            if self.state == "running":
                self.image = self.run_images_right[int(self.frame / 5 % 4)]
            if self.attached == True:
                if pygame.sprite.spritecollide(self, self.game.climbing_group, False):
                    self.attached = True
                    self.jumptimer = 0
                    if self.climbing_step < 10:
                        self.image = self.climbing_images_right[0]
                    else:
                        self.image = self.climbing_images_right[1]
                else:
                    self.attached = False
            if self.jumptimer > 3:
                self.image = self.run_images_right[1]
            if self.hurttimer > 0:
                self.image = self.images[3][0]


        if self.facing == "left":
            if self.state == "idle":
                self.image = self.idle_images_left[int(self.frame / 15 % 2)]
            if self.state == "running":
                self.image = self.run_images_left[int(self.frame / 5  % 4)]
            if self.attached == True:
                if pygame.sprite.spritecollide(self, self.game.climbing_group, False):
                    self.attached = True
                    self.jumptimer = 0
                    if self.climbing_step < 10:
                        self.image = self.climbing_images_left[0]
                    else:
                        self.image = self.climbing_images_left[1]
                else:
                    self.attached = False
            if self.jumptimer > 3:
                self.image = self.run_images_left[1]
            if self.hurttimer > 0:
                self.image = pygame.transform.flip(self.images[3][0],1,0).convert()

        if self.jumptimer > 0:
            self.move(0,-22)
            self.jumptimer -= 1
        if self.hurttimer > 0:
            self.hurttimer -= 1
        if self.climbing_step > 20:
            self.climbing_step = 0


    def render(self):
        pygame.draw.rect(self.game.screen,"red",self.rect)

class Ladder(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Topladder(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def onhit(self,object,direction = 0):
        if True:
            if direction == 0:
                pass
            if direction == 1:
                pass
            if direction == 2:
                if object.attached == False:
                    if object.rect.bottom < self.rect.top + 3:
                        object.rect.bottom = self.rect.top
                        object.syncposy()
                        if isinstance(object, Player):
                            object.grounded = True

            if direction == 3:
                pass

class Spike(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy().inflate(0, -1)

    def onhit(self,object,direction = 0):
        if True:
            if direction == 0:
                object.rect.right = self.rect.left
                object.syncposx()

            if direction == 1:
                object.rect.left = self.rect.right
                object.syncposx()

            if direction == 2:

                if isinstance(object,Player):
                    if self.hitbox.colliderect(object.rect):
                        object.hurt()
                object.rect.bottom = self.rect.top
                object.syncposy()
                if isinstance(object,Player):
                    object.grounded = True

            if direction == 3:
                object.rect.top = self.rect.bottom
                object.syncposy()


class Bouncer(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy().inflate(0, -2)
        self.hitbox.topleft = utilities.add_pos(self.hitbox.topleft, (0,1))

    def onhit(self,object,direction = 0):
        if self.hitbox.colliderect(object.rect):
            if True:
                if direction == 0:
                    object.rect.right = self.hitbox.left
                    object.syncposx()

                if direction == 1:
                    object.rect.left = self.hitbox.right
                    object.syncposx()

                if direction == 2:

                    if isinstance(object,Player):
                        if self.hitbox.colliderect(object.rect):
                            if object.game.game.actions["a"]:
                                self.game.bouncesound.play()
                                object.jumptimer = 35
                    object.rect.bottom = self.hitbox.top
                    object.syncposy()
                    if isinstance(object, Player):
                        object.grounded = True

                if direction == 3:
                    object.rect.top = self.hitbox.bottom

                    object.syncposy()



class BreakBlock(pygame.sprite.Sprite):
    def __init__(self, image=None,image2 =None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image2 = image2
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.life = 30
    def onhit(self,object,direction = 0):
        if True:
            if direction == 0:
                object.rect.right = self.rect.left
                object.syncposx()

            if direction == 1:
                object.rect.left = self.rect.right
                object.syncposx()

            if direction == 2:
                object.rect.bottom = self.rect.top
                object.syncposy()

                if isinstance(object,Player):
                    object.grounded = True
                    self.life -= 1
                    if self.life == 15:
                        self.game.game.schan2.play(self.game.breaking1sound)
                        self.image = self.image2
                    if self.life < 0:
                        self.game.game.schan3.play(self.game.breaking2sound)
                        self.kill()
            if direction == 3:
                object.rect.top = self.rect.bottom
                object.syncposy()
                if isinstance(object,Player):
                    object.jumptimer = 0


    def render(self):
            self.game.screen.blit(self.image,self.rect)
class Bridge(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def onhit(self,object,direction = 0):
        if True:
            if direction == 0:
                pass
            if direction == 1:
                pass
            if direction == 2:
                if not self.game.game.actions["down"]:
                    if object.rect.bottom < self.rect.top + 3:
                        object.rect.bottom = self.rect.top
                        object.syncposy()
                        if isinstance(object, Player):
                            object.grounded = True

            if direction == 3:
                pass
class Disappearingblock(pygame.sprite.Sprite):
    def __init__(self, image=None, image2 = None, pos=None, game=None, delay = 0, count = 200):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.img1 = self.image
        self.img2 = image2
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.delay = delay
        self.count = count
        self.counter = self.count - self.delay
        self.updates = True


    def onhit(self,object,direction = 0):
        if self.counter < self.count / 2:
            if True:
                if direction == 0:
                    object.rect.right = self.rect.left
                    object.syncposx()
                if direction == 1:
                    object.rect.left = self.rect.right
                    object.syncposx()

                if direction == 2:
                    object.rect.bottom = self.rect.top
                    object.syncposy()
                    if isinstance(object, Player):
                        object.grounded = True

                if direction == 3:
                    object.rect.top = self.rect.bottom
                    object.syncposy()
                    if isinstance(object, Player):
                        object.jumptimer = 0
    def update(self):
        self.counter -= 1
        if self.counter == 0:
            self.counter = self.count
        if self.counter < self.count / 2:
            self.image = self.img1
        else:
            self.image = self.img2
class Door(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            if self.game.game.actions["up"]:
                self.game.curlev += 1
                self.game.acorncount += self.game.acornlevcount
                self.game.reset()
class Acorn(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            self.game.acornlevcount += 1
            self.kill()
            self.game.collectsound.play()
class decor(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=None, game=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.topleft = pos



