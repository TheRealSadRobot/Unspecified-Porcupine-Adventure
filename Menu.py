import pygame
import Settings
import Level

class menu:
    """This class defines all of the menus that you see throught the game."""
    def __init__(self, layer: pygame.surface, typename: str, array: list):
        """This initializes the menus.
        :param layer: layer to draw on
        :param typename: type of menu to use
        :param array: array of objects to place this in
        :return: menu object"""
        self.mode = 0
        self.mousedown = False
        self.fadetimer = 0
        self.fade = pygame.Surface((1280, 720))
        self.fade.fill("#FFFFFF")
        if typename == "Main":
            self.BG = pygame.image.load("TitleBG.png")
            self.bgcoords = [0,0]
            self.btnquit = pygame.image.load("Button.png")
            self.quitcoords = [10,500]
            self.quitmove = 20
            self.btnoption = pygame.image.load("Button.png")
            self.optioncoords = [10,390]
            self.optionmove = 20
            self.btnplay = pygame.image.load("Button.png")
            self.playcoords = [10,280]
            self.playmove = 20
            self.fontcolor1 = "#2222AA"
            self.fontcolor2 = "#2222AA"
            self.fontcolor3 = "#2222AA"
            self.font = pygame.font.Font('COMIC.ttf', 50)
        elif typename == "Title":
            self.image = pygame.image.load("Title.png")
            self.BG = pygame.image.load("TitleBG.png")
            self.bgcoords = [0,0]
            self.font = pygame.font.Font('COMIC.ttf', 50)
            self.starttexttimer = 0
        elif typename == "Options":
            self.BG = pygame.image.load("TitleBG.png")
            self.bgcoords = [0,0]
            self.btndebug = pygame.image.load("Button.png")
            self.debugcoords = [10,280]
            self.debugmove = 20
            self.btnquit = pygame.image.load("Button.png")
            self.quitcoords = [10,500]
            self.quitmove = 20
            self.fontcolor1 = "#2222AA"
            self.color = "#FF0000"
            self.state = "OFF"
            self.font = pygame.font.Font('COMIC.ttf', 50)
        elif typename == "Endcard":
            self.image = pygame.image.load("Credits.png")
            self.BG = pygame.image.load("LevelBG1.png")
            self.bgcoords = [0,0]
            self.font = pygame.font.Font('COMIC.ttf', 50)
            self.starttexttimer = 0
        self.typename = typename
        self.layer = layer
        self.array = array
        array.append(self)
        
    def update(self)->None:
        """Update the menu. Called every frame."""
        if self.typename == "Main":
            self.bgcoords[0]+=1
            if self.bgcoords[0] >= 0:
                self.bgcoords[0] = -1280
            keys = pygame.key.get_pressed()
            locus = pygame.mouse.get_pos()
            if self.mode == 0:
                self.fontcolor1 = "#2222AA"
                self.fontcolor2 = "#2222AA"
                self.fontcolor3 = "#2222AA"
                if locus[1] > self.quitcoords[1] and locus[1] < self.quitcoords[1] + 100 and locus[0] > self.quitcoords[0] and locus[0] < self.quitcoords[0] + 500 :
                    self.fontcolor1 = "#0000FF"
                    if pygame.mouse.get_pressed()[0]:
                        self.mode = 1
                if locus[1] > self.optioncoords[1] and locus[1] < self.optioncoords[1] + 100 and locus[0] > self.optioncoords[0] and locus[0] < self.optioncoords[0] + 500 :
                    self.fontcolor2 = "#0000FF"
                    if pygame.mouse.get_pressed()[0]:
                        self.mode = 2
                if locus[1] > self.playcoords[1] and locus[1] < self.playcoords[1] + 100 and locus[0] > self.playcoords[0] and locus[0] < self.playcoords[0] + 500 :
                    self.fontcolor3 = "#0000FF"
                    if pygame.mouse.get_pressed()[0]:
                        self.mode = 3
            
            self.layer.blit(self.BG,self.bgcoords)
            text = self.font.render("Quit", False,self.fontcolor1)
            rect4text = text.get_rect(center = (250,50))
            self.btnquit.blit(text,rect4text)
            self.layer.blit(self.btnquit,self.quitcoords)
            text = self.font.render("Options", False,self.fontcolor2)
            rect4text = text.get_rect(center = (250,50))
            self.btnoption.blit(text,rect4text)
            self.layer.blit(self.btnoption,self.optioncoords)
            text = self.font.render("Start", False,self.fontcolor3)
            rect4text = text.get_rect(center = (250,50))
            self.btnplay.blit(text,rect4text)
            self.layer.blit(self.btnplay,self.playcoords)
            
            if self.mode == 1:
                self.fadetimer += 1
                self.quitcoords[1] += self.quitmove
                self.playcoords[0]-=15
                self.optioncoords[0]-=10
                self.quitmove -= 1
                if self.fadetimer >= 60:
                    self.fade.set_alpha((255/60)*(self.fadetimer-60))
                    self.layer.blit(self.fade, (0,0))
                if self.fadetimer >= 120:
                    newmenu = menu(self.layer,"Title",self.array)
                    self.array.remove(self)
            
            if self.mode == 2:
                self.fadetimer += 1
                self.optioncoords[1] += self.optionmove
                self.playcoords[0]-=15
                self.quitcoords[0]-=10
                self.optionmove -= 1
                if self.fadetimer >= 60:
                    self.fade.set_alpha((255/60)*(self.fadetimer-60))
                    self.layer.blit(self.fade, (0,0))
                if self.fadetimer >= 120:
                    newmenu = menu(self.layer,"Options",self.array)
                    self.array.remove(self)
            
            if self.mode == 3:
                self.fadetimer += 1
                self.optioncoords[0]-=15
                self.quitcoords[0]-=10
                if self.fadetimer >= 60:
                    self.fade.set_alpha((255/60)*(self.fadetimer-60))
                    self.layer.blit(self.fade, (0,0))
                if self.fadetimer >= 120:
                    level = Level.Level(self.layer, self.array)
                    self.array.remove(self)
            
        elif self.typename == "Title":
            self.bgcoords[0]-=1
            if self.mode == 0:
                self.starttexttimer += 1
            else:
                self.starttexttimer += 10
            if self.bgcoords[0] <= -1280:
                self.bgcoords[0] = 0
            if self.starttexttimer >= 60:
                self.starttexttimer = 0
            keys = pygame.key.get_pressed()
            if True in keys:
                self.mode = 1
                
            self.layer.blit(self.BG,self.bgcoords)
            self.layer.blit(self.image, (0,0))
            if self.starttexttimer < 30:
                self.layer.blit(self.font.render("Press Any Key", False, "#FFFFFF"), (500,500))
            
            if self.mode == 1:
                self.fadetimer += 1
            if self.fadetimer >= 60:
                self.fade.set_alpha((255/60)*(self.fadetimer-60))
                self.layer.blit(self.fade, (0,0))
            if self.fadetimer >= 120:
                newmenu = menu(self.layer,"Main",self.array)
                self.array.remove(self)
            
        elif self.typename == "Options":
            self.bgcoords[0]+=1
            if self.bgcoords[0] >= 0:
                self.bgcoords[0] = -1280
            keys = pygame.key.get_pressed()
            locus = pygame.mouse.get_pos()
            if self.mode == 0:
                color = self.fontcolor1
                state = "OFF"
                self.fontcolor1 = "#2222AA"
                if locus[1] > self.quitcoords[1] and locus[1] < self.quitcoords[1] + 100 and locus[0] > self.quitcoords[0] and locus[0] < self.quitcoords[0] + 500 :
                    self.fontcolor1 = "#0000FF"
                    if pygame.mouse.get_pressed()[0]:
                        self.mode = 1
                self.fontcolor1 = "#2222AA"
                if locus[1] > self.debugcoords[1] and locus[1] < self.debugcoords[1] + 100 and locus[0] > self.debugcoords[0] and locus[0] < self.debugcoords[0] + 500 :
                    self.fontcolor1 = "#0000FF"
                    if pygame.mouse.get_pressed()[0] and self.mousedown == False:
                        if Settings.debug == False:
                            Settings.debug = True
                            self.btndebug = pygame.image.load("Button.png")
                        else:
                            Settings.debug = False
                            self.btndebug = pygame.image.load("Button.png")
                        self.mousedown = True
                if Settings.debug == True:
                    self.color = "#00FF00"
                    self.state = "ON"
                else:
                    self.color = "#FF0000"
                    self.state = "OFF"
            self.layer.blit(self.BG,self.bgcoords)
            text = self.font.render("Done", False,self.fontcolor1)
            rect4text = text.get_rect(center = (250,50))
            self.btnquit.blit(text,rect4text)
            self.layer.blit(self.btnquit,self.quitcoords)
            text = self.font.render(f"Debug Mode: {self.state}", False,self.color)
            rect4text = text.get_rect(center = (250,50))
            self.btndebug.blit(text,rect4text)
            self.layer.blit(self.btndebug,self.debugcoords)
            if self.mode == 1:
                self.fadetimer += 1
                self.quitcoords[1] += self.quitmove
            if self.fadetimer >= 60:
                self.fade.set_alpha((255/60)*(self.fadetimer-60))
                self.layer.blit(self.fade, (0,0))
            if self.fadetimer >= 120:
                newmenu = menu(self.layer,"Main",self.array)
                self.array.remove(self)
                
        elif self.typename == "Endcard":
            self.bgcoords[0]-=1
            if self.mode == 0:
                self.starttexttimer += 1
            else:
                self.starttexttimer += 10
            if self.bgcoords[0] <= -1280:
                self.bgcoords[0] = 0
            if self.starttexttimer >= 60:
                self.starttexttimer = 0
            keys = pygame.key.get_pressed()
            if True in keys:
                self.mode = 1
            self.layer.blit(self.BG,self.bgcoords)
            self.layer.blit(self.image, (0,0))
            if self.mode == 1:
                self.fadetimer += 1
            if self.fadetimer >= 60:
                self.fade.set_alpha((255/60)*(self.fadetimer-60))
                self.layer.blit(self.fade, (0,0))
            if self.fadetimer >= 120:
                newmenu = menu(self.layer,"Title",self.array)
                self.array.remove(self)
        if pygame.mouse.get_pressed()[0] != True:
            self.mousedown = False
