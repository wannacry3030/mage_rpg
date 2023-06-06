import scene
41
class Win(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self,game)
        self.game = game
        self.won_text = self.game.large_text.render("  The End",False,self.game.colors[3])
        self.acorn_text = self.game.small_text.render("number of acorns" ,False,self.game.colors[3])
        self.acorn_text2 = self.game.small_text.render("     saved : " + str(self.game.game_play.acorncount),
                                                      False, self.game.colors[3])
        self.good_ending = self.game.small_text.render("you've collected",False,self.game.colors[3])
        self.good_ending2 = self.game.small_text.render("enough to replant ", False,
                                                       self.game.colors[3])
        self.good_ending3 = self.game.small_text.render("  the forest", False,
                                                       self.game.colors[3])
        self.bad_ending = self.game.small_text.render("you've failed ", False,
                                                       self.game.colors[3])
        self.bad_ending2 = self.game.small_text.render("  to save", False,
                                                      self.game.colors[3])
        self.bad_ending3 = self.game.small_text.render("  enough acorns", False,
                                                      self.game.colors[3])
    def update(self):
        self.acorn_text2 = self.game.small_text.render("     saved : " + str(self.game.game_play.acorncount),
                                                       False, self.game.colors[3])
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] <= 0:
            self.game.actions_cooldowns["start"]= 20
            self.game.start_screen.enter()
            self.game.game_play.curlev = 0
            self.game.game_play.reset()
            self.game.game_play.acorncount = 0
            self.game.game_play.lives = 3

    def render(self):
        self.game.screen.fill(self.game.colors[0])
        self.game.screen.blit(self.won_text, (10,10))
        self.game.screen.blit(self.acorn_text, (10, 30))
        self.game.screen.blit(self.acorn_text2, (10, 40))
        if self.game.game_play.acorncount > 30:
            self.game.screen.blit(self.good_ending, (10, 50))
            self.game.screen.blit(self.good_ending2, (10, 60))
            self.game.screen.blit(self.good_ending3, (10, 70))
        if self.game.game_play.acorncount <= 30:
            self.game.screen.blit(self.bad_ending, (10, 50))
            self.game.screen.blit(self.bad_ending2, (10, 60))
            self.game.screen.blit(self.bad_ending3, (10, 70))
