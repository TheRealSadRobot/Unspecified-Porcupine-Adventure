import pygame
import Settings
import math

class hud:
    """This class defines the Heads-Up Display that the player sees information with."""
    def __init__(self, parent:"player", location:list, layer:pygame.Surface):
        """Initialize the HUD.
        :param parent: The player that this HUD is tied to
        :param location: The screen location of the HUD
        :param layer: The layer to draw on
        :return: a hud object"""
        self.player = parent
        self.pos = location
        self.layer = layer
        self.graphic = pygame.image.load("HUD.png").convert()
        self.graphic.set_colorkey("#111111")
        #self.endgraphic = pygame.image.load().convert()
        #self.endgraphic.set_colorkey("#111111")
        self.end = False
        self.font = pygame.font.Font('COMIC.ttf', 20)
        self.endfont = pygame.font.Font('ARIAL.ttf', 50)
    def update(self)->None:
        """Update the HUD with the most up-to-date information."""
        self.layer.blit(self.graphic, self.pos)
        text = self.font.render("ZIP", False, "#FFFFFF")
        self.layer.blit(text, (self.pos[0]+100, self.pos[1]+18))
        text = self.font.render(f"{int(self.player.level.timer/60)//60}:{(self.player.level.timer/60)%60:02.0f}", False, "#FFFFFF")
        self.layer.blit(text, (self.pos[0]+100, self.pos[1]+48))
        text = self.font.render(f"{self.player.rings}", False, "#FFFFFF")
        self.layer.blit(text, (self.pos[0]+100, self.pos[1]+78))
        if Settings.debug == True:
            text = self.font.render(f"location:{self.player.pos}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+135))
            text = self.font.render(f"ground angle:{math.degrees(self.player.anglerad)}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+155))
            text = self.font.render(f"raw movement speed:{self.player.movespeed}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+175))
            text = self.font.render(f"ground mode:{self.player.groundmode}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+195))
            text = self.font.render(f"Jump disabled:{self.player.jumped}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+215))
            text = self.font.render(f"grounded:{self.player.grounded}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+235))
            text = self.font.render(f"grounded last frame:{self.player.lastgrounded}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+255))
            text = self.font.render(f"player state:{self.player.state}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+275))
            text = self.font.render(f"invincible frames:{self.player.iframes}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+295))
            text = self.font.render(f"camera position:{self.player.level.maincam.pos}", False, "#FFFFFF")
            self.layer.blit(text, (self.pos[0], self.pos[1]+315))
        if self.end == True:
            text = self.endfont.render("YOU GOT THROUGH", False, "#FFFFFF")
            rect4text = text.get_rect(center = (self.layer.get_size()[0]/2,(self.layer.get_size()[1]/2)-50))
            self.layer.blit(text, rect4text)
            text = self.endfont.render("THE ZONE", False, "#FFFFFF")
            rect4text = text.get_rect(center = (self.layer.get_size()[0]/2,(self.layer.get_size()[1]/2)))
            self.layer.blit(text, rect4text)
