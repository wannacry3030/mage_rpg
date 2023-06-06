
import scene

class Gameover(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self,game)
        self.game = game
        self.gameover_text = self.game.large_text.render("Game over",False,self.game.colors[3])
        self.gameover_text_rect = self.gameover_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 3))
    def update(self):
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] <= 0:
            self.game.actions_cooldowns["start"]= 20
            self.game.start_screen.enter()
            self.game.game_play.curlev = 0
            self.game.game_play.reset()
            self.game.game_play.acorncount = 0
            self.game.game_play.lives = 3

    def render(self):
        self.game.screen.fill(self.game.colors[0])
        self.game.screen.blit(self.gameover_text, self.gameover_text_rect)
