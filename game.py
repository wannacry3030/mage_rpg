import pygame, os,sys
import asyncio
import pygame._sdl2.controller as pgc

import deathscreen
import gameover
import gameplay
import pause
import scene, utilities,startscreen
import winscreen

SCREENWIDTH = 144
SCREENHEIGHT = 160
SCALEDW = 288
SCALEDH = 320


class Game():
    def __init__(self):

        # pygame setup
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.mixer.pre_init(44100, -16, 2, 256)
        pygame.init()
        pgc.init()
        self.screen = pygame.surface.Surface((SCREENWIDTH,SCREENHEIGHT))
        self.rscreen = pygame.display.set_mode((SCALEDW,SCALEDH),pygame.RESIZABLE|pygame.SCALED)
        pygame.display.set_caption("forest Mage","Forest Mage")



        #set up controls
        self.actions = {"a":False,"b":False,"up": False,"down":False,"left":False,"right":False,
                                        "start":False, "select":False}
        self.action_mapping = { "a":pygame.K_a,"b":pygame.K_s,"up":pygame.K_UP, "down":pygame.K_DOWN, "left":pygame.K_LEFT,"right":pygame.K_RIGHT,"start":pygame.K_RETURN,"select":pygame.K_RIGHTBRACKET}

        self.actions_cooldowns = {"a": 0, "b": 0, "up": 0, "down": 0, "left": 0, "right": 0,
                        "start": 0, "select": 0}
        try:
            self.p1c = pgc.Controller(0)
        except:
            self.p1c = None



        #setup up game directories and paths
        self.image_dir = os.path.join("data","images")
        self.sound_dir = os.path.join("data","sounds")
        self.level_dir = os.path.join("data", "levels")
        self.style_font_path = os.path.join("data","fonts","GameBoy.ttf")

        self.icon = utilities.loadImage(self.image_dir,"icon.png")
        pygame.display.set_icon(self.icon)

        self.schan1 = pygame.mixer.Channel(1)
        self.schan2 = pygame.mixer.Channel(2)
        self.schan3 = pygame.mixer.Channel(3)
        self.schan4 = pygame.mixer.Channel(4)
        self.schan5 = pygame.mixer.Channel(5)


        #setup font
        self.large_text = pygame.font.Font(self.style_font_path,16)
        self.med_text = pygame.font.Font(self.style_font_path, 12)
        self.small_text = pygame.font.Font(self.style_font_path, 8)

        #colors
        # self.colors = [(208,208,88),(160,164,64),(112,128,40),(64,80,16),]

        self.colors = [(151, 117, 166),(104, 58, 104),(65, 39, 82),(45, 22, 44),]


        #setup gameloop and clock
        self.running = False
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # game scenes  setup
        self.start_screen = startscreen.Startscreen(self)
        self.game_play = gameplay.Gameplay(self)
        self.deathscreen = deathscreen.Deadscreen(self)
        self.gameover = gameover.Gameover(self)
        self.pausescreen = pause.Pause(self)
        self.winscreen = winscreen.Win(self)
        self.curr_scene = self.start_screen
        self.prev_scene = "game"

    def update_actions(self):

        # gets keys pressed from pygame
        keys = pygame.key.get_pressed()
        # resets all keys to false
        for k in self.actions:
            self.actions[k] = False
        if self.p1c != None:
            if self.p1c.get_button(0):
                self.actions["a"] = True
            if self.p1c.get_button(1):
                self.actions["b"] = True
            if self.p1c.get_button(14):
                self.actions["right"] = True
            if self.p1c.get_button(13):
                self.actions["left"] = True
            if self.p1c.get_button(11):
                self.actions["up"] = True
            if self.p1c.get_button(12):
                self.actions["down"] = True
            if self.p1c.get_button(6):
                self.actions["start"] = True
            if self.p1c.get_button(4):
                self.actions["select"] = True

        # sets any key to true if its pressed
        for k in self.action_mapping.values():
            if keys[k]:
                self.actions[utilities.get_key(self.action_mapping, k)] = True
        for k in self.actions_cooldowns:
            self.actions_cooldowns[k] -= 1
        if keys[pygame.K_ESCAPE]:
            self.running = False
            pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
        #self.clock.tick(60)
        self.delta_time = self.clock.tick(65)/100
        self.update_actions()
        self.curr_scene.update()

    def render(self):
        self.curr_scene.render()
        pygame.transform.scale(self.screen,(SCALEDW,SCALEDH),self.rscreen)
        pygame.display.flip()


