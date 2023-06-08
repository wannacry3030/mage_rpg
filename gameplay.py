import pygame, pytmx
import scene
import os
import gameobjects, camera, baddies
import utilities


class Gameplay(scene.Scene):
    def __init__(self, game):
        scene.Scene.__init__(self,game)

        self.actionpressed = False
        self.acorncount = 0
        self.acornlevcount = 0

        self.screen = self.game.screen
        self.collision_group = pygame.sprite.Group()
        self.climbing_group = pygame.sprite.Group()
        self.decor_group = pygame.sprite.Group()
        self.player = gameobjects.Player(self)
        self.camspeed = 1
        self.camera = camera.Camera(self.player,self.screen.get_size(),(1000,10000000),self.camspeed)
        self.lives = 3


        self.levels = [ pytmx.load_pygame(os.path.join(self.game.level_dir,"l1.tmx")),
                        pytmx.load_pygame(os.path.join(self.game.level_dir,"l2.tmx")),
                        pytmx.load_pygame(os.path.join(self.game.level_dir,"l3.tmx")),
                        pytmx.load_pygame(os.path.join(self.game.level_dir,"l4.tmx")),
                        pytmx.load_pygame(os.path.join(self.game.level_dir,"l5.tmx")),
                        pytmx.load_pygame(os.path.join(self.game.level_dir, "l6.tmx"))
                        ]
        self.curlev = 0
        self.tilesheet = utilities.loadSpriteSheet(utilities.loadImage(self.game.image_dir, "tiles.png",1), (16, 16))
        self.bimages = utilities.loadSpriteSheet(utilities.loadImage(self.game.image_dir, "baddies.png",1),
                                            (16, 16))
        self.hud = utilities.loadImage(self.game.image_dir,"hud.png",1)
        self.levelparse(self.curlev)
        self.grav_group = pygame.sprite.Group()
        self.grav_group.add(self.player)
        self.background1 = utilities.loadImage(self.game.image_dir,"background1.png",0)
        self.jumpsound = utilities.loadSound(self.game.sound_dir, "jump.ogg")
        self.collectsound = utilities.loadSound(self.game.sound_dir,"collect.ogg")
        self.bouncesound = utilities.loadSound(self.game.sound_dir, "bounce.ogg")
        self.hitsound = utilities.loadSound(self.game.sound_dir,"hit.ogg")
        self.breaking1sound = utilities.loadSound(self.game.sound_dir, "breaking1.ogg")
        self.breaking2sound = utilities.loadSound(self.game.sound_dir, "breaking2.ogg")
        self.stepsound = utilities.loadSound(self.game.sound_dir, "steps.ogg")



    def levelparse(self,lev):
        self.camera.levelsize = (self.levels[lev].width * 16, self.levels[lev].height * 16)
        for layer in [self.levels[lev].get_layer_by_name("tiles")]:
            for t in layer:
                try:
                    img = self.levels[lev].get_tile_image_by_gid(t[2])
                    self.collision_group.add(gameobjects.Block(img, (t[0] * 16, t[1] * 16), self))
                except:
                    pass

        for layer in [self.levels[lev].get_layer_by_name("objects")]:
            for o in layer:
                if o.name == "start":
                    self.player.set_pos(o.x , o.y)
                if o.name == "ladder":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.climbing_group.add(gameobjects.Ladder(img, (o.x , o.y ), self))
                if o.name == "topladder":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    l = gameobjects.Topladder(img, (o.x , o.y ), self)
                    self.climbing_group.add(l)
                    self.collision_group.add(l)
                if o.name == "spike":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.collision_group.add(gameobjects.Spike(img, (o.x, o.y), self))
                if o.name == "bouncer":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.collision_group.add(gameobjects.Bouncer(img, (o.x, o.y), self))
                if o.name =="breaking":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    img2 = self.tilesheet[0][6]
                    self.collision_group.add(gameobjects.BreakBlock(img,img2,(o.x,o.y),self))
                if o.name == "bridge":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.collision_group.add(gameobjects.Bridge(img, (o.x, o.y), self))
                if o.name =="disappearing":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    img2 = self.tilesheet[3][4]
                    self.collision_group.add(gameobjects.Disappearingblock(img,img2,(o.x,o.y),self,int(o.delay)))
                if o.name == "deebot":
                    self.collision_group.add(baddies.Deebot((o.x,o.y),self))
                if o.name == "meebo":
                    self.collision_group.add(baddies.Meebo((o.x,o.y),self))
                if o.name == "sawber":
                    self.collision_group.add(baddies.Sawber((o.x,o.y),self))
                if o.name == "door":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.collision_group.add(gameobjects.Door(img, (o.x, o.y), self))
                if o.name == "acorn":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.collision_group.add(gameobjects.Acorn(img, (o.x, o.y), self))
                if o.name == "decor":
                    img = self.levels[lev].get_tile_image_by_gid(o.gid)
                    self.decor_group.add(gameobjects.decor(img, (o.x, o.y), self))

    def reset(self):
        self.collision_group.empty()
        self.climbing_group.empty()
        self.decor_group.empty()
        self.acornlevcount = 0
        if self.curlev < 6:
            self.levelparse(self.curlev)
        else:
            self.game.winscreen.enter()
        if self.curlev == 5:
            pygame.mixer.music.load(os.path.join(self.game.sound_dir, "finished.wav"))
            pygame.mixer.music.play(-1, 0, 10)
        else:
            pygame.mixer.music.rewind()


    def update(self):


        self.camera.update()
        self.player.grounded = False
        print(self.acorncount)

        for s in self.grav_group:
            if s.attached == False:
                s.move(0,10)
        if self.game.actions["b"]:
            if self.player.grounded:
                self.player.maxaccel = 10
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] < 1 :
            self.game.actions_cooldowns["start"] = 20
            self.game.pausescreen.enter()
        if self.game.actions["select"] and self.game.actions_cooldowns["select"] < 1:
            self.game.actions_cooldowns["select"] = 20
            self.curlev += 1
            self.reset()

        if self.game.actions["left"]:
            self.player.accel -= self.player.speed
            self.player.state = "running"
            self.player.facing = "left"
        elif self.game.actions["right"]:
            self.player.accel += self.player.speed
            self.player.state = "running"
            self.player.facing = "right"
        else:
            self.player.state = "idle"
        if self.game.actions["a"] :
            if self.actionpressed == False:
                self.actionpressed = True
                if self.player.grounded:
                    self.jumpsound.play()
                    self.player.jumptimer = 20
                if self.player.attached == True:
                    self.player.attached = False
                    self.player.jumptimer = 8
                    self.jumpsound.play()
        else:
            self.actionpressed = False
            if self.player.jumptimer > 6:
                self.player.jumptimer = 6
        if self.game.actions["up"]:
            if self.player.attached == True:
                self.player.move(0,-5)
                self.player.climbing_step += 1
            else:
                self.player.attached = True

        if self.game.actions["down"]:
            if self.player.attached == True:
                self.player.move(0,5)
                self.player.climbing_step += 1
            else:
                self.player.attached = True
                if self.player.grounded:
                    self.player.move(0, 8)
        self.player.move(self.player.accel,0)

        self.player.update()
        for i in self.collision_group:
            if hasattr(i,"updates"):
                i.update()
        if self.player.dead and self.player.hurttimer == 0:
            self.player.dead = False
            self.game.deathscreen.enter()
            self.lives -= 1
            if self.lives == - 1:
                self.game.gameover.enter()
    def onenter(self):
        pygame.mixer.music.load(os.path.join(self.game.sound_dir, "gamesong.wav"))
        pygame.mixer.music.play(-1, 0, 10)

    def render(self):
        self.screen.fill(self.game.colors[0])
        self.screen.blit(self.background1, (0,0))
        for d in self.decor_group:
            self.camera.draw_sprite(self.screen,d)
        for t in self.collision_group:
            self.camera.draw_sprite(self.screen,t)
        for l in self.climbing_group:
            self.camera.draw_sprite(self.screen,l)
        self.camera.draw_sprite(self.screen,self.player)
        self.screen.blit(self.hud,(0,0))
        acorntext = self.game.small_text.render("Diamantes: " + str(self.acorncount + self.acornlevcount),False,self.game.colors[2])
        self.screen.blit(acorntext, (20,15))
        livestext = self.game.small_text.render("Vidas: " + str(self.lives), False, self.game.colors[2])
        self.screen.blit(livestext, (20, 25))










