import pygame
import Menu
import json

class obj:
    """This class is a parent for a bunch of non-player objects. The player could also be a subclass of this in the future."""
    file = json.load(open("Animations.json"))
    def __init__(self,layer:pygame.Surface,level:"Level",camera:"Camera",pos:list):
        """Initializer for the class.
        :param layer: the surface to draw on
        :param level: The parent level of the object
        :param pos: The position of the object
        :return: an obj object (or subclass thereof...)"""
        self.layer = layer
        self.level = level
        self.camera = camera
        self.pos = pos
        level.objlist.append(self)
        
        self.frame = 0
        self.subframe = 0
        self.spriterect = []
        self.mirror = 0
        self.sprite = pygame.Surface(self.size).convert()

    def setanim(self, name:str)->None:
        """Sets the animation to the name passed in.
        :param name: the name of the animation being swapped to"""
        self.animname = name
        self.frame = 0
        self.subframe = 0    
    def animate(self)->None:
        """Iterates to the next animation frame"""
        if self.subframe > self.file[self.name][self.animname][self.frame][5]:
            self.subframe = 0
            self.frame += 1
        else:
            self.subframe += 1
        if self.file[self.name][self.animname][self.frame] == "Loop":
            self.frame = 0
            self.subframe = 0
        else:
            self.spriterect = (self.file[self.name][self.animname][self.frame][0],
            self.file[self.name][self.animname][self.frame][1],
            self.file[self.name][self.animname][self.frame][2],
            self.file[self.name][self.animname][self.frame][3])
            self.mirror = self.file[self.name][self.animname][self.frame][4]
    def render(self)->None:
        """Renders the current animation frame"""
        self.sprite.fill("#111111")
        if self.mirror:
            self.sprite.blit(self.spritesheet,
            (0,0),
            self.spriterect)
            self.layer.blit(pygame.transform.flip(self.sprite,True, False),
            (self.pos[0]-(self.size[0]/2)-self.camera.pos[0],
            self.pos[1]-(self.size[1]/2)-self.camera.pos[1]))
        else:
            self.sprite.blit(self.spritesheet,
            (0,0),
            self.spriterect)
            self.layer.blit(self.sprite,
            (self.pos[0]-(self.file[self.name][self.animname][self.frame][2]/2)-self.camera.pos[0],
            self.pos[1]-(self.size[1]/2)-self.camera.pos[1]))
            #pygame.draw.rect(self.layer,"#FFFF00",(self.pos[0]-(self.size[0]/2)-self.camera.pos[0],self.pos[1]-(self.size[1]/2)-self.camera.pos[1], self.size[0], self.size[1]))
class ring(obj):
    """This class defines the Rings the player collects throughout the game."""
    fx = pygame.mixer.Sound("ringget.wav")
    def __init__(self, layer:pygame.Surface,level:"Level",camera:"Camera",pos:list):
        """Initializer for the class.
        :param layer: the surface to draw on
        :param level: The parent level of the object
        :param camera: The camera object to offset distance by
        :param pos: The position of the object
        :return: an ring object"""
        self.size = (50,50)
        super().__init__(layer,level,camera,pos)
        self.collected = False
        self.name = "Ring"
        self.collecttimer = 0
        self.vanishtime = 5
        self.spritesheet = pygame.image.load("Ring.png").convert()
        self.animname = "Idle"
        
    def update(self)->None:
        """Update the ring. That is all"""
        self.animate()
        if self.collected == True:
            if self.collecttimer <= self.vanishtime:
                self.collecttimer += 1
                self.render()
            else:
                self.level.objlist.remove(self)
        else:
            self.render()
    def collide(self)->None:
        """Update status if player has collected the ring"""
        if self.collected == False:
            self.level.itemsounds.play(ring.fx)
            self.setanim("Flash")
            self.collected = True

class spike(obj):
    """This class defines the spike objects found in that one pit and nowhere else ¯\_(ツ)_/¯"""
    def __init__(self, layer:pygame.Surface,level:"Level",camera:"Camera",dir:int,pos:list):
        """Initializer for the class.
        :param layer: the surface to draw on
        :param level: The parent level of the object
        :param camera: The camera object to offset distance by
        :param dir: The direction the spikes should face. Only one of them is programmed to do anything
        :param pos: The position of the object
        :return: an spike object"""
        self.size = (50,50)
        super().__init__(layer,level,camera,pos)
        self.dir = dir
        self.sprite = pygame.image.load("Spikes.png").convert()
        
    def update(self)->None:
        """Update the spikes. I mean, not much is going to happen, but you can try."""
        self.layer.blit(self.sprite, (self.pos[0]-(self.size[0]/2)-self.camera.pos[0],self.pos[1]-(self.size[1]/2)-self.camera.pos[1], self.size[0], self.size[1]))        
    def collide(self)->None:
        """As of now? does nothing. Just here to make the player programming easier."""
        pass

class goal(obj):
    """This class defines the goalpost at the end of the level."""
    def __init__(self, layer:pygame.Surface,level:"Level",camera:"Camera",pos:list):
        """Initializer for the class.
        :param layer: the surface to draw on
        :param level: The parent level of the object
        :param camera: The camera object to offset distance by
        :param pos: The position of the object
        :return: a goal object"""
        self.size = (102,86)
        super().__init__(layer,level,camera,pos)
        self.spritesheet = pygame.image.load("Signpost.png").convert()
        self.collected = False
        self.delay = 240
        self.speentime = 180
        self.name = "Signpost"
        self.animname = "Hostile"
        self.timer = 0
        
    def update(self)->None:
        """Update the goalpost"""
        if self.collected == True:
            if self.timer == self.speentime:
                self.level.end()
                self.setanim("Friendly")
                self.timer += 1
            elif self.timer > self.speentime:
                self.level.timeiterate = False
                if self.delay > 0:
                    self.delay -= 1
                else:
                    menu = Menu.menu(self.level.winsurface, "Endcard" ,self.level.array)
                    self.level.array.remove(self.level)
            else:
                self.timer += 1
        self.animate()
        self.render()
        #pygame.draw.rect(self.layer,"#00FF00",(self.pos[0]-(self.size[0]/2)-self.camera.pos[0],self.pos[1]-(self.size[1]/2)-self.camera.pos[1], self.size[0], self.size[1]))
        
    def collide(self)->None:
        """Set the sign to spin when the player touches it."""
        if self.collected == False:
            self.setanim("Spin")
            self.collected = True
        
