class Scene():
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.musicstart = False

    def update(self):
        pass

    def render(self):
        pass

    def onenter(self):
        pass

    def onexit(self):
        self.musicstart = False
        pass

    def enter(self):
        self.game.curr_scene.exit()
        self.game.curr_scene = self
        self.onenter()

    def exit(self):
        self.game.prev_scene = self
        self.onexit()
