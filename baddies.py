import pygame, utilities, gameobjects, os



class Deebot(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.bimages[0][0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.updates = True

        self.hitbox = self.rect.copy().inflate(-2, -2)

        self.dir = True
        self.frame = 0
        self.accel = 2

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def syncrect(self):
        self.rect.topleft = self.pos

    def syncpos(self):
        self.pos = (self.rect.left, self.rect.top)

    def syncposx(self):
        self.pos = (self.rect.left, self.pos[1])

    def syncposy(self):
        self.pos = (self.pos[0], self.rect.top)


    def move_single_axis(self, dx, dy):
        if dx > 0:
            self.pos = (self.pos[0] + self.accel * self.game.game.delta_time, self.pos[1])
        if dx < 0:
            self.pos = (self.pos[0] + -(self.accel * self.game.game.delta_time), self.pos[1])
        if dy != 0:
            self.pos = (self.pos[0], self.pos[1] + dy * self.game.game.delta_time)
        self.syncrect()
        hit = pygame.sprite.spritecollide(self, self.game.collision_group, False)
        for block in hit:
            if not block == self:
                if dx > 0:
                    block.onhit(self, 0)
                    self.dir = False
                if dx < 0:
                    block.onhit(self, 1)
                    self.dir = True
                if dy > 0:
                    block.onhit(self, 2)
                if dy < 0:
                    block.onhit(self, 3)


    def onhit(self, object, direction=0):

        if isinstance(object, gameobjects.Player):
            if direction == 2:
                if self.rect.top > object.rect.bottom - 4 and self.rect.top < object.rect.bottom + 6:
                    object.jumptimer = 20
                    self.kill()
                    self.game.hitsound.play()
            else:
                if self.hitbox.colliderect(object.rect):
                    object.hurt()
                    self.dir = not self.dir


    def update(self):
        self.move(0, 1)
        self.frame += 1
        self.image = self.game.bimages[0][int(self.frame / 8 % 4)]
        if self.dir:
            self.move(1, 0)
            self.image = pygame.transform.flip(self.image, 1, 0).convert()
        if not self.dir:
            self.move(-1, 0)

        self.hitbox.center = self.rect.center

class Meebo(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.bimages[1][0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.updates = True

        self.hitbox = self.rect.copy().inflate(-2, -2)

        self.dir = True
        self.frame = 0
        self.accel = 5

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def syncrect(self):
        self.rect.topleft = self.pos

    def syncpos(self):
        self.pos = (self.rect.left, self.rect.top)

    def syncposx(self):
        self.pos = (self.rect.left, self.pos[1])

    def syncposy(self):
        self.pos = (self.pos[0], self.rect.top)


    def move_single_axis(self, dx, dy):
        if dx > 0:
            self.pos = (self.pos[0] + self.accel * self.game.game.delta_time, self.pos[1])
        if dx < 0:
            self.pos = (self.pos[0] + -(self.accel * self.game.game.delta_time), self.pos[1])
        if dy > 0:
            self.pos = (self.pos[0], self.pos[1] + self.accel * self.game.game.delta_time)
        if dy < 0:
            self.pos = (self.pos[0], self.pos[1] + -(self.accel * self.game.game.delta_time))
        self.syncrect()
        hit = pygame.sprite.spritecollide(self, self.game.collision_group, False)
        for block in hit:
            if not block == self:
                if dx > 0:
                    block.onhit(self, 0)
                if dx < 0:
                    block.onhit(self, 1)
                if dy > 0:
                    block.onhit(self, 2)
                    self.dir = True
                if dy < 0:
                    block.onhit(self, 3)
                    self.dir = False


    def onhit(self, object, direction=0):
        if isinstance(object, gameobjects.Player):
            if self.hitbox.colliderect(object.rect):
                object.hurt()
                self.dir = not self.dir


    def update(self):
        #self.counter -= 1
        self.frame += 1
        self.image = self.game.bimages[1][int(self.frame / 8 % 4)]
        if self.dir:
            self.move(0,-1)
        if not self.dir:
            self.move(0,1)

        self.hitbox.center = self.rect.center
class Sawber(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.bimages[2][0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.updates = True

        self.hitbox = self.rect.copy().inflate(-2, -2)

        self.dir = True
        self.frame = 0
        self.accel = 9

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def syncrect(self):
        self.rect.topleft = self.pos

    def syncpos(self):
        self.pos = (self.rect.left, self.rect.top)

    def syncposx(self):
        self.pos = (self.rect.left, self.pos[1])

    def syncposy(self):
        self.pos = (self.pos[0], self.rect.top)


    def move_single_axis(self, dx, dy):
        if dx > 0:
            self.pos = (self.pos[0] + self.accel * self.game.game.delta_time, self.pos[1])
        if dx < 0:
            self.pos = (self.pos[0] + -(self.accel * self.game.game.delta_time), self.pos[1])
        if dy != 0:
            self.pos = (self.pos[0], self.pos[1] + dy * self.game.game.delta_time)
        self.syncrect()
        hit = pygame.sprite.spritecollide(self, self.game.collision_group, False)
        for block in hit:
            if not block == self:
                if dx > 0:
                    block.onhit(self, 0)
                    self.dir = False
                if dx < 0:
                    block.onhit(self, 1)
                    self.dir = True
                if dy > 0:
                    block.onhit(self, 2)
                if dy < 0:
                    block.onhit(self, 3)


    def onhit(self, object, direction=0):
        if isinstance(object, gameobjects.Player):
            if self.hitbox.colliderect(object.rect):
                object.hurt()
                self.dir = not self.dir


    def update(self):
        self.move(0, 1)
        self.frame += 1
        self.image = self.game.bimages[2][int(self.frame / 8 % 4)]
        if self.dir:
            self.move(1, 0)
            self.image = pygame.transform.flip(self.image, 1, 0).convert()
        if not self.dir:
            self.move(-1, 0)

        self.hitbox.center = self.rect.center