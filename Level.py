import pygame
import json
import Player
import Camera
import Objects
import Settings

class Level:
    """This class defines the levels that the player will traverse"""
    def __init__(self, layer,array):
        """initializes the level
        :param layer: the layer on which the level is drawn
        :param array: the array that the level goes into
        :return: a Level object"""
        self.file = json.load(open("AFZ0.json"))
        self.winsurface = layer
        self.timer = 0
        self.timeiterate = True
        self.charlayer = pygame.Surface((1280,720))
        self.levellayer = pygame.Surface((1280, 720))
        self.levelgraphicslayer = pygame.Surface((1280, 720))
        self.loopbglocation = [0,0]
        self.bglocation = [0,0]
        self.itemsounds = pygame.mixer.Channel(0)
        #format for bgarray entry is [pygame image, scrollscalefactor]
        self.charlayer.set_colorkey("#111111")
        self.levellayer.set_colorkey("#111111")

        self.bgarray = [[pygame.image.load("LevelBG1.png").convert(),5],[pygame.image.load("LevelBG2.png").convert(),4],[pygame.image.load("LevelBG3.png").convert(),2]]
        self.chunkarray = []        
        self.chunksemisolid = []
        self.levelimage = None
        self.objlist = []
        self.cambounds = []
        self.playerlocus = [0,0]
        self.levelload()
        self.maincam = Camera.Camera("Follow",(0,0), self.cambounds)
        self.ring = Objects.ring(self.charlayer, self, self.maincam, (1275,-450))
        self.ring = Objects.ring(self.charlayer, self, self.maincam, (1350,-450))
        self.ring = Objects.ring(self.charlayer, self, self.maincam, (1200,-450))
        self.ring = Objects.ring(self.charlayer, self, self.maincam, (2675,-550))
        self.ring = Objects.ring(self.charlayer, self, self.maincam, (2750,-550))
        self.ring = Objects.ring(self.charlayer, self, self.maincam, (2825,-550))

        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2375,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2425,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2475,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2525,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2575,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2625,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2675,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2725,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2775,-5))
        self.spike = Objects.spike(self.charlayer, self, self.maincam, 0, (2825,-5))

        self.goal = Objects.goal(self.charlayer, self, self.maincam, (4830,-160))
        self.p1 = Player.player(self.playerlocus, self.charlayer, self, self.maincam)
        self.array = array
        array.append(self)

    def levelload(self)->None:
        """Load level data from a json file"""
        self.cambounds = self.file["CameraBounds"]
        self.chunkarray = self.file["Chunks"]
        self.chunksemisolid = self.file["Semisolid"]
        self.playerlocus = self.file["PlayerLocus"]
        filename =  self.file["Graphic"]
        self.levelimage = pygame.image.load(filename)
                
    def update(self)->None:
        """Update the level"""
        if self.timeiterate == True:
            self.timer+=1
        self.levellayer.fill("#111111")
        self.charlayer.fill("#111111")
        self.renderlines()
        self.renderbg()
        self.objsupdate()
        self.winsurface.blit(self.levelgraphicslayer, (0,0))
        self.winsurface.blit(self.levellayer, (0,0))
        self.winsurface.blit(self.charlayer, (0,0))

    def renderbg(self)->None:
        """Render the Background of the level"""
        for layer in self.bgarray:
            #self.bglocation = self.basebglocation
            self.bglocation[0] = -(self.maincam.pos[0]%(1280*layer[1]))/layer[1]
            self.bglocation[1] = -(self.maincam.pos[1]%(720*layer[1]))/layer[1]
            layer[0].set_colorkey("#111111")
            self.levelgraphicslayer.blit(layer[0], self.bglocation)
        
    def renderlines(self)->None:
        """Render the lines that make up the level geometry"""
        try:
            #print(self.levelimage)
            self.levellayer.blit(self.levelimage,(-self.maincam.pos[0],-(2125)-self.maincam.pos[1]))#,area=(500,2125))
        except:
            pass
        if Settings.debug:
            for chunknum in range(len(self.chunkarray)):
                self.segarray = []
                for point in self.chunkarray[chunknum]:
                    self.segarray.append((point[1]-self.maincam.pos[0], point[2]-self.maincam.pos[1]))
                if not self.chunksemisolid[chunknum]:
                    pygame.draw.polygon(self.levellayer,(0,0,0),self.segarray,5)
                else:
                    pygame.draw.polygon(self.levellayer,"#FFFFFF",self.segarray,5)

    def objsupdate(self)->None:
        """Update the objects within the level"""
        self.maincam.focuspoint = self.p1.pos
        self.maincam.update()
        for item in self.objlist:
            item.update()
        self.p1.update()
        
    def end(self)->None:
        """run at the end of the level to ease the transition to whatever's next."""
        self.p1.hud.end = True
