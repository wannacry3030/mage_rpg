import pygame
import utilities
import scene
import game

class Deadscreen(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self, game)
        self.dead_text = self.game.small_text.render("Voce Morreu",False,self.game.colors[0])
        self.dead_text_rect = self.dead_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
    def update(self):
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] <= 0:
            self.game.pausecooldown = 20
            self.game.prev_scene.enter()
            self.game.game_play.reset()
            self.exit()
    def render(self):
        self.game.prev_scene.render()
        self.game.screen.blit(self.dead_text,self.dead_text_rect)