import pygame.sprite

import utilities

class Camera():
    def __init__(self, target, screensize,levelsize,speed = 1):
        self.offset = (0, 0)
        self.realoffest = target.rect.center
        self.target = target
        self. speed = speed
        self.screensize = screensize
        self.levelsize = levelsize
    def update(self):
        self.offset = utilities.sub_pos((self.screensize[0] / 2, self.screensize[1] / 1.5), self.target.rect.center)
        if self.offset[0] > 0:
            self.offset = utilities.setx(self.offset, 0)
        if self.offset[0] < -self.levelsize[0] + self.screensize[0] + 8:
            self.offset = utilities.setx(self.offset, -self.levelsize[0] + self.screensize[0] + 8)
        if self.offset[1]  > 28 :
            self.offset = utilities.sety(self.offset, 28)
        if self.offset[1] < self.screensize[1] - self.levelsize[1]:
            self.offset = utilities.sety(self.offset, self.screensize[1] - self.levelsize[1])


    def get_offset(self):
        return self.offset
    def draw_sprite(self,screen,sprite):
        if sprite.rect.colliderect(pygame.rect.Rect(utilities.sub_pos(screen.get_rect().topleft, self.offset),(screen.get_width(),screen.get_height()))):
            if hasattr(sprite,"player"):
                screen.blit(sprite.image, utilities.add_pos(utilities.add_pos(sprite.rect.topleft, (-4 , 0)), self.offset))
            else:
                screen.blit(sprite.image,utilities.add_pos(sprite.rect.topleft,self.offset))