
import scene

class Pause(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self, game)
        self.pause_text = self.game.small_text.render("*pause*",False,self.game.colors[0])
        self.pause_text_rect = self.pause_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
    def update(self):
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] <= 0:
            self.game.actions_cooldowns["start"] = 20
            self.game.prev_scene.enter()
            self.exit()
    def render(self):
        self.game.prev_scene.render()
        self.game.screen.blit(self.pause_text,self.pause_text_rect)