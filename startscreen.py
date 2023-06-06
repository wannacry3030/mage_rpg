import scene, utilities, pygame,os

class Startscreen(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self,game)

        self.top = utilities.loadImage(self.game.image_dir,"startscreentop.png",1)

        self.title = self.game.large_text.render("noiboy",False,self.game.colors[3])
        self.titlerect = self.title.get_rect(center = (self.screen.get_width()/ 2,self.screen.get_height() / 2))

        self.subtitle = self.game.small_text.render("spirit of the woods",False,self.game.colors[1])
        self.subtitlerect = self.subtitle.get_rect(center = self.titlerect.center)
        self.subtitlerect.top = self.titlerect.bottom

        self.start1 = self.game.small_text.render("press start",False,self.game.colors[2])
        self.start2 = self.game.small_text.render("press start", False, self.game.colors[1])
        self.start3 = self.game.small_text.render("press start", False, self.game.colors[3])
        self.startcounter = 0

        self.startrect = self.start1.get_rect(center = self.titlerect.center)
        self.startrect.top = self.titlerect.bottom + 25
    def update(self):
        if self.musicstart == False:
            pygame.mixer.music.load(os.path.join(self.game.sound_dir, "title.wav"))
            pygame.mixer.music.play(-1,0,10)
            self.musicstart = True
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] < 1:
            self.game.game_play.enter()
            self.game.actions_cooldowns["start"] = 20


    def render(self):
        self.screen.fill(self.game.colors[0])
        self.screen.blit(self.title,self.titlerect)
        self.screen.blit(self.subtitle,self.subtitlerect)
        self.startcounter += 1
        if self.startcounter < 20:
            self.screen.blit(self.top,(0,-1))
            self.screen.blit(self.start1,self.startrect)
        elif self.startcounter < 40:
            self.screen.blit(self.top, (0, -4))
            self.screen.blit(self.start2,self.startrect)
        elif self.startcounter < 60:
            self.screen.blit(self.top, (0, -2))
            self.screen.blit(self.start3,self.startrect)
        elif self.startcounter < 80:
            self.screen.blit(self.top, (0, -1))
            self.startcounter = 0