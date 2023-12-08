import pygame
import time
import math
import Settings
import HUD
import json

class player:
    """
    This is the class that contains the player character.
    """
    def __init__(self,pos:list,layer:pygame.Surface,level:'Level',camera:'Camera'):
        """
        Initializer for the player class.
        :param pos: The starting coordinates of the player
        :param layer: The pygame surface that the player will draw onto
        :param level: The level the player will explore
        :param camera: The camera that is watching the player
        :returns: A player object
        """
        self.debug = Settings.debug
        self.voice = pygame.mixer.Channel(1)
        self.ringlosesound = pygame.mixer.Sound("losering.wav")
        self.hitsound = pygame.mixer.Sound("hit.wav")
        
        self.rings = 0
        self.lastgrounded = False
        self.grounded = False
        self.rsidecollide = False
        self.lsidecollide = False
        self.jumped = False
        self.state = "control"
        self.groundmode = 0
        self.iframes = 0
        self.camera = camera
        self.anglerad = 0
        self.dir = 0
        self.pos = pos
        self.lastpos = self.pos
        self.collidesegment = None
        self.layer = layer
        self.level = level
        self.levelchunks = self.level.chunkarray
        self.hud = HUD.hud(self, (10,10), self.layer)
        self.size = (100,100)
        self.spritesize = (50,50)
        self.lboffset = (-50,50)
        self.rboffset = (50,50)
        self.lsoffset = (-50,0)
        self.rsoffset = (50,0)
        self.ltoffset = (-50,-50)
        self.rtoffset = (50,-50)
        self.lcollide = 0
        self.rcollide = 0
        self.movespeed = 0
        self.fallspeed = 0
        self.maxfall = 7
        self.maxspeed = 10
        self.intersectx = 0
        self.intersecty = 0

        self.file = json.load(open("Animations.json"))
        self.spritesheet = pygame.image.load("Hero.png").convert()
        self.animname = "Idle"
        self.frame = 0
        self.subframe = 0
        self.spriterect = []
        self.mirror = 0
        self.sprite = pygame.Surface(self.spritesize).convert()
        self.color = "#00FF00"

    def update(self)->None:
        """Updates the player. Called every frame."""
        #time.sleep(0.1)
        self.lastgrounded = self.grounded
        lcollidepast,rcollidepast = self.lcollide,self.rcollide
        self.grounded = False
        self.move()
        self.anglerad = 0
        if abs(self.movespeed) > 0:
            self.setanim("Move")
        else:
            self.setanim("Idle")
        if abs(self.fallspeed) > 0:
            self.setanim("Jump")
        if self.state == "hitstun":
            self.setanim("Hurt")
        #print(self.state)
        if self.state == "end" and self.movespeed == 0:
            self.setanim("Win")
        self.animate()
        self.render()
        self.lcheck, self.lcollide = self.collidecheck(self.lboffset, 1,"positive")
        self.rcheck, self.rcollide = self.collidecheck(self.rboffset, 1, "positive")
        burner, self.ltopcollide = self.collidecheck(self.ltoffset, 1,"negative")
        burner, self.rtopcollide = self.collidecheck(self.rtoffset, 1, "negative")
        burner, self.lsidecollide = self.collidecheck(self.lsoffset, 0,"negative")
        burner, self.rsidecollide = self.collidecheck(self.rsoffset, 0, "positive")
        if self.lcollide == True or self.rcollide == True:
            self.grounded = True

        self.groundangleget(self.pos)

        #pygame.draw.line(self.layer, self.color, (self.pos),(self.lastpos), 50)
        #pygame.draw.rect(self.layer,"#FFAA00",(self.pos[0]-(self.size[0]/2),self.pos[1]-(self.size[1]/2), self.size[0], self.size[1]))
        self.objcollidecheck()
        self.hud.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.debug == True:
                mouselocus = [pygame.mouse.get_pos()[0]+self.camera.pos[0], pygame.mouse.get_pos()[1]+self.camera.pos[1]]
                self.pos = [mouselocus[0],mouselocus[1]]

    def move(self)->None:
        """Moves the player's location based on factors such as input."""
        self.lastpos = [self.pos[0],self.pos[1]]
        newpos = [self.pos[0], self.pos[1]]
        keys = pygame.key.get_pressed()

        #newpos = (newpos[0]-0.1, newpos[1])
        """if keys[pygame.K_DOWN]:
            newpos = [newpos[0], newpos[1]+2]
        if keys[pygame.K_UP]:
            newpos = [newpos[0], newpos[1]-2]"""

        if self.state in ["control","iframes"]:
            if keys[pygame.K_SPACE] and self.jumped == False:
                self.fallspeed = -15
                self.jumped = True
            if (math.degrees(self.anglerad) < 45) or (math.degrees(self.anglerad) > 315):
                self.movespeed += 0.125*math.sin(self.anglerad)
            if keys[pygame.K_LEFT] and self.lsidecollide == False:
                if self.movespeed <= -self.maxspeed:
                    self.movespeed = -self.maxspeed
                else:
                    if self.lastgrounded == True:
                        self.movespeed -= 0.1
                    else:
                        self.movespeed -= 0.5
                self.dir = 1
            elif keys[pygame.K_RIGHT] and self.rsidecollide == False:
                if self.movespeed >= self.maxspeed:
                    self.movespeed = self.maxspeed
                else:
                    if self.lastgrounded == True:
                        self.movespeed += 0.1
                    else:
                        self.movespeed += 0.2
                self.dir = 0
            else:
                if self.movespeed > 0.1:
                    self.movespeed -= 0.1
                elif self.movespeed < -0.1:
                    self.movespeed += 0.1
                elif abs(self.movespeed) <= 0.1:
                    self.movespeed = 0
            #print(self.pos)
                #print(self.movespeed)
        if self.state == "iframes":
            self.iframes -= 1
            if self.iframes <= 0:
                self.state = "control"
        if self.state == "hitstun" and self.lastgrounded == True:
            self.state = "iframes"
            self.iframes = 120
        if self.state == "end":
            if self.movespeed > 0.1:
                self.movespeed -= 0.1
            elif self.movespeed < -0.1:
                self.movespeed += 0.1
            elif abs(self.movespeed) <= 0.1:
                self.movespeed = 0
        #GRAVITY
        if self.lastgrounded == False:
            if self.fallspeed >= self.maxfall:
                self.fallspeed = self.maxfall
            else:
                self.fallspeed += 0.4
        elif self.jumped == False: 
            self.fallspeed = 0
        if self.lastgrounded == True:
            self.jumped = False
        newpos[1] += self.fallspeed
        
        if self.lastgrounded==True:
            newpos[0] += round(self.movespeed*math.cos(self.anglerad),5)
            newpos[1] += round(self.movespeed*math.sin(self.anglerad),5)
        else:
            newpos[0] += self.movespeed
        self.pos[0] = newpos[0]
        self.pos[1] = newpos[1]

    def objcollidecheck(self)->None:
        """Check if the player is colliding with any objects. If so, provide appropriate resolution."""
        for item in self.level.objlist:
            itemt = item.pos[1]-(item.size[1]/2)
            itemb = item.pos[1]+(item.size[1]/2)
            iteml = item.pos[0]-(item.size[0]/2)
            itemr = item.pos[0]+(item.size[0]/2)
            if (iteml <= self.pos[0]+self.lsoffset[0] and itemr >= self.pos[0]+self.lsoffset[0]) or (iteml <= self.pos[0]+self.rsoffset[0] and itemr >= self.pos[0]+self.rsoffset[0]) or (item.pos[0] <= self.pos[0]+self.rsoffset[0] and item.pos[0] >= self.pos[0]+self.lsoffset[0]):
                if (itemt >= self.pos[1]+self.ltoffset[1] and itemt <= self.pos[1]+self.lboffset[1]) or (itemb >= self.pos[1]+self.ltoffset[1] and itemb <= self.pos[1]+self.lboffset[1]) or (item.pos[1] <= self.pos[1]+self.lboffset[1] and item.pos[1] >= self.pos[1]+self.ltoffset[1]):
                    if type(item).__name__ == "ring" and item.collected == False:
                        self.rings += 1
                    if type(item).__name__ == "goal":
                        self.state = "end"
                    if type(item).__name__ == "spike":
                        if self.state in ["control","hitstun","iframes"]:
                            if self.pos[1] <= itemt:
                                self.pos[1] = item.pos[1]-(item.size[1]/2)-(self.size[1]/2)
                                self.lastgrounded = True
                                self.grounded = True
                                if item.dir == 0 and self.state == "control":
                                    self.damage()
                            else:
                                if self.pos[0] <= item.pos[0]:
                                    self.pos[0] = item.pos[0]-(item.size[0]/2)-(self.size[0]/2)
                                    self.rsidecollide = True
                                elif self.pos[0] >= item.pos[0]:
                                    self.pos[0] = item.pos[0]+(item.size[0]/2)+(self.size[0]/2)
                                    self.lsidecollide = True

                    item.collide()
    
    def damage(self)->None:
        """Damage the player, knocking them back and stripping them of any rings they'd collected."""
        self.setanim("Hurt")
        self.state = "hitstun"
        self.grounded = False
        self.lastgrounded = False
        self.fallspeed = -5
        if self.movespeed > 0:
            self.movespeed = -5
        elif self.movespeed < 0:
            self.movespeed = 5
        else:
            if self.dir == 0:
                self.movespeed = -5
            else:
                self.movespeed = 5
        if self.rings > 0:
            self.rings = 0
            self.voice.play(self.ringlosesound)
        else:
            self.voice.play(self.hitsound)

    def collidecheck(self, offset: list, axis: int, polarity: str) -> list | bool:
        """Check if the player's current trajectory will cause them to go thru the level geometry. 
        If so, fix that promptly!
        :param offset: The offset(from player center) of the point being considered.
        :param axis: a boolean/int representing the axis to check on
        :param polarity: string that directs the aim of the checks
        :return: a list giving the collision point and a Yes/No answer to "did they collide?" """
        #find segment to check
        self.segmentget((self.pos[0]+offset[0],self.pos[1]+offset[1]),axis, polarity)
        if self.collidesegment != None:
            #create line between last known position of point and current position of point
            #check fo crossover
            #IF a ZeroDivisionError occurs, check if the x of the point is equal to the x of the segment
            #if axis is 1:
            p1x = self.collidesegment[1][1]
            p1y = self.collidesegment[1][2]
            xc1 = self.collidesegment[1][1]-self.collidesegment[0][1]
            yc1 = self.collidesegment[1][2]-self.collidesegment[0][2]

            if axis == 1 and polarity == "positive":
                try:
                    check = round((yc1/xc1)*(self.pos[0]+offset[0]-p1x)+p1y,5)
                    lastcheck = round((yc1/xc1)*(self.lastpos[0]+offset[0]-p1x)+p1y,5)
                except ZeroDivisionError:
                    if yc1 > 0:
                        check = self.collidesegment[1][2]
                    else:
                        check = self.collidesegment[0][2]
                    lastcheck = check
                collided = False
                if (round(self.lastpos[1]+offset[1],5) <= lastcheck and check <= round(self.pos[1]+offset[1],5)):
                    self.pos[1] = check-offset[1]
                    self.grounded = True
                    collided = True
                return [self.pos[0]+offset[0],check], collided
                
            if axis == 1 and polarity == "negative":
                try:
                    check = round((yc1/xc1)*(self.pos[0]+offset[0]-p1x)+p1y, 5)
                    lastcheck = round((yc1/xc1)*(self.lastpos[0]+offset[0]-p1x)+p1y, 5)
                except ZeroDivisionError:
                    if abs(yc1) > 0:
                        check = self.pos[0]+offset[0]
                    else:
                        check = self.collidesegment[0][2]
                    lastcheck = check
                collided = False
                if (round(self.lastpos[1]+offset[1], 5) >= lastcheck and check >= round(self.pos[1]+offset[1],5)):
                    self.pos[1] = check-offset[1]
                    collided = True
                return [self.pos[0]+offset[0],check], collided
                                
            elif axis == 0 and polarity == "positive":
                try:
                    check = round((xc1/yc1)*(self.pos[1]+offset[1]-p1y)+p1x,5)
                    lastcheck = round((xc1/yc1)*(self.lastpos[1]+offset[1]-p1y)+p1x,5)
                except ZeroDivisionError:
                    if xc1 < 0:
                        check = self.collidesegment[1][2]
                    else:
                        check = self.collidesegment[0][2]
                    lastcheck = check
                collided = False
                if (round(self.lastpos[0]+offset[0],5) <= lastcheck and check <= round(self.pos[0]+offset[0],5)):
                    self.pos[0] = check-offset[0]
                    collided = True
                return [check, self.pos[1]+offset[1]], collided
                
            elif axis == 0 and polarity == "negative":
                try:
                    check = round((xc1/yc1)*(self.pos[1]+offset[1]-p1y)+p1x,5)
                    lastcheck = round((xc1/yc1)*(self.lastpos[1]+offset[1]-p1y)+p1x,5)
                except ZeroDivisionError:
                    if xc1 > 0:
                        check = self.collidesegment[1][2]
                    else:
                        check = self.collidesegment[0][2]
                    lastcheck = check
                collided = False
                if (round(self.lastpos[0]+offset[0],5) >= lastcheck and check >= round(self.pos[0]+offset[0],5)):
                    self.pos[0] = check-offset[0]
                    collided = True
                return [check, self.pos[1]+offset[1]], collided
        else:
            return [self.pos[0]+offset[0],self.pos[1]+offset[1]], False

    def groundangleget(self, point:list)->None:
        """Get the angle of the ground the player is standing on.
        :param point: the point affected if angle isn't 180/0 and one point is under the line"""
        if self.grounded == True:
            if self.lcheck[1] < self.rcheck[1]:
               point[1] = self.lcheck[1]-self.lboffset[1]
            elif self.rcheck[1] > self.lcheck[1]:
                point[1] = self.rcheck[1]-self.rboffset[1]
            yc = (self.lcheck[1]-self.rcheck[1])
            xc = (self.lcheck[0]-self.rcheck[0])
            self.anglerad = math.atan(yc/xc)
            if self.anglerad < 0:
                self.anglerad = 2*math.pi+self.anglerad
            #select the groundmode for the player. This is needed for wall running.
            #the ordering is like this:
            #0: floor
            #1: rwall
            #2: roof
            #3: lwall
            """if math.degrees(self.anglerad) < -45:
                if self.groundmode != 3:
                    self.groundmode += 1
                else:
                    self.groundmode = 0"""
        else:
            #set the ground mode to the floor if not grounded
            self.groundmode = 0

    def getcollidepoint(self, segment, axis, offset=(0,0)) -> None|list:
        """get the point at which the considered geometry and the player vectors would intersect.
        :param segment: the segment that will be checked
        :param axis: the axis to check
        :param offset: the direction to check
        :return: None, or a point of collision.
        """
        self.movevector = (("line",self.lastpos[0]+offset[0],self.lastpos[1]+offset[1]),("line",self.pos[0]+offset[0],self.pos[1]+offset[1]))
        if segment != None:
            p1x = segment[1][1]
            p1y = segment[1][2]
            p2x = self.movevector[1][1]
            p2y = self.movevector[1][2]
            xc1 = segment[1][1]-segment[0][1]
            yc1 = segment[1][2]-segment[0][2]
            xc2 = self.movevector[1][1]-self.movevector[0][1]
            yc2 = self.movevector[1][2]-self.movevector[0][2]
            if axis == 0:
                try:
                    self.intersectx = ((p2x*yc2*xc1)-(p1x*yc1*xc2)-(p2y-p1y)*xc2*xc1)/(yc2*xc1-yc1*xc2)
                except:
                    if yc1 > 0:
                        self.intersectx=(xc1/yc1)*(self.pos[1]+offset[1]-p1y)+p1x
                    else:
                        if segment[1][1]> segment[0][1]:
                            self.intersectx = segment[0][1]
                        else:
                            self.intersectx = segment[1][1]
                try:
                    self.intersecty = (yc1/xc1)*(self.intersectx-p1x)+p1y
                except:
                    if (segment[0][2] <= self.lastpos[1]+offset[1] and self.lastpos[1]+offset[1] <= segment[1][2]) or (segment[1][2] <= self.lastpos[1]+offset[1] and self.lastpos[1]+offset[1] <= segment[0][2]):
                        if segment[0][2] <= segment[1][2]:
                            self.intersecty = segment[0][2]
                        else:
                            self.intersecty = segment[1][2]
            else:
                try:
                    self.intersecty = ((p2y*xc2*yc1)-(p1y*xc1*yc2)-(p2x-p1x)*yc2*yc1)/(xc2*yc1-xc1*yc2)
                except:
                    if xc1 > 0:
                        self.intersecty=(yc1/xc1)*(self.pos[0]+offset[0]-p1x)+p1y
                    else:
                        if segment[1][2] >= segment[0][2]:
                            self.intersecty = segment[0][2]
                        else:
                            self.intersecty = segment[1][2]
                try:
                    self.intersectx = (xc1/yc1)*(self.intersecty-p1y)+p1x
                except:
                    if yc2 > 0:
                        self.intersectx = (xc2/yc2)*(self.intersecty-p2y)+p2x
                    else:
                        self.intersectx = self.pos[0] + offset[0]
            if self.debug:
                pygame.draw.rect(self.layer, "#FFFF00", (self.intersectx-self.camera.pos[0],self.intersecty-self.camera.pos[1],5,5))
            return [self.intersectx, self.intersecty]
                    
    def segmentget(self, point, axis, polarity)->None:
        """Find the segment that will be checked for a given point.
        :param point: the point to be checked
        :param axis: the axis to check
        :param polarity: the direction that will be checked
        """
        self.color = "#00FF00"
        candidates = []
        if axis == 1:
            for number in range(len(self.levelchunks)):
                chunk = self.levelchunks[number]
                for segmentnum in range(len(chunk)):
                    try:
                        if chunk[segmentnum][1] > chunk[segmentnum+1][1]:
                            lpoint = chunk[segmentnum+1]
                            rpoint = chunk[segmentnum]
                        else:
                            lpoint = chunk[segmentnum]
                            rpoint = chunk[segmentnum+1]
                    except IndexError:
                        if chunk[0][1] < chunk[segmentnum][1]:
                            lpoint = chunk[0]
                            rpoint = chunk[segmentnum]
                        else:
                            lpoint = chunk[segmentnum]
                            rpoint = chunk[0]
                    
                    if (lpoint[1] <= point[0] and point[0] <= rpoint[1]) or (lpoint[1]==rpoint[1] and lpoint[1]==point[0]):
                        if not self.level.chunksemisolid[number]:
                            candidates.append((lpoint,rpoint))
                        else:
                            #Cotton
                            lcollidepoint = self.getcollidepoint((lpoint,rpoint),axis,self.lboffset)
                            rcollidepoint = self.getcollidepoint((lpoint,rpoint),axis,self.rboffset)
                            if lcollidepoint[1] > self.pos[1] or rcollidepoint[1] > self.pos[1]:
                                candidates.append((lpoint,rpoint))
                        #pygame.draw.line(self.layer,self.color,(lpoint[1],lpoint[2]),(rpoint[1],rpoint[2]),5)
                        """else:
                            pygame.draw.line(self.layer,"#FF00FF",(lpoint[1],lpoint[2]),(rpoint[1],rpoint[2]),5)"""
                
            if candidates != []:
                self.color = "#FF0000"
                dists = []
                for segment in candidates:
                    #print(segment)
                    try:
                        l = segment[0]
                        r = segment[1]
                        yval = ((l[2]-r[2])/(l[1]-r[1]))*(point[0]-l[1])+l[2]
                        ydist = abs(point[1]-yval)
                    #ZeroDivisionError will occur when vertical lines are encountered.
                    except ZeroDivisionError:
                        if segment[0][2] > segment[1][2]:
                            ydist = point[1]-segment[1][2]
                        else:
                            ydist = point[1]-segment[0][2]
                    dists.append(abs(ydist))
                greatestindex = 0
                for index in range(len(dists)):
                    #print(f"Index:{index} Value{dists[index]}\nVS\nIndex:{greatestindex} Value{dists[greatestindex]}")
                    if dists[index] < dists[greatestindex]:
                        greatestindex = index
                self.collidesegment = candidates[greatestindex]
                #print(self.collidesegment)
                if self.debug == True:
                    if polarity == "positive":
                        pygame.draw.line(self.layer,self.color,(self.collidesegment[0][1]-self.camera.pos[0],self.collidesegment[0][2]-self.camera.pos[1]),(self.collidesegment[1][1]-self.camera.pos[0],self.collidesegment[1][2]-self.camera.pos[1]),5)
                    else:
                        pygame.draw.line(self.layer,"#FF00FF",(self.collidesegment[0][1]-self.camera.pos[0],self.collidesegment[0][2]-self.camera.pos[1]),(self.collidesegment[1][1]-self.camera.pos[0],self.collidesegment[1][2]-self.camera.pos[1]),5)
            else:
                self.collidesegment = None
        elif axis == 0:
            for number in range(len(self.levelchunks)):
                chunk = self.levelchunks[number]
                for segmentnum in range(len(chunk)):
                    try:
                        if chunk[segmentnum][2] > chunk[segmentnum+1][2]:
                            tpoint = chunk[segmentnum+1]
                            bpoint = chunk[segmentnum]
                        else:
                            tpoint = chunk[segmentnum]
                            bpoint = chunk[segmentnum+1]
                    except IndexError:
                        if chunk[0][2] < chunk[segmentnum][2]:
                            tpoint = chunk[0]
                            bpoint = chunk[segmentnum]
                        else:
                            tpoint = chunk[segmentnum]
                            bpoint = chunk[0]
                    if (tpoint[2] <= point[1] and point[1] <= bpoint[2]) or (tpoint[2]==bpoint[2] and tpoint[2]==point[1]):
                        if not self.level.chunksemisolid[number]:
                            candidates.append((tpoint,bpoint))
                        #print(candidates)
                            if self.debug == True:
                                pygame.draw.line(self.layer,"#0000FF",(tpoint[1]-self.camera.pos[0],tpoint[2]-self.camera.pos[1]),(bpoint[1]-self.camera.pos[0],bpoint[2]-self.camera.pos[1]),5)
                    """else:
                        pygame.draw.line(self.layer,"#FF00FF",(lpoint[1],lpoint[2]),(rpoint[1],rpoint[2]),5)"""
            if candidates != []:
                self.color = "#FF0000"
                dists = []
                for segment in candidates:
                    #print(segment)
                    try:
                        t = segment[0]
                        b = segment[1]
                        #yval = ((l[2]-r[2])/(l[1]-r[1]))*(point[0]-l[1])+l[2]
                        xval = ((t[1]-b[1])/(t[2]-b[2]))*(point[1]-t[2])+t[1]
                        xdist = abs(point[0]-xval)
                    #ZeroDivisionError will occur when vertical lines are encountered.
                    except ZeroDivisionError:
                        if segment[0][1] > segment[1][1]:
                            xdist = point[0]-segment[1][1]
                        else:
                            xdist = point[0]-segment[0][1]
                    dists.append(abs(xdist))
                greatestindex = 0
                for index in range(len(dists)):
                    if dists[index] < dists[greatestindex]:
                        greatestindex = index
                self.collidesegment = candidates[greatestindex]
                #print(self.collidesegment)
                if self.debug == True:
                    if polarity == "positive":
                        pygame.draw.line(self.layer,"#00FFFF",(self.collidesegment[0][1],self.collidesegment[0][2]),(self.collidesegment[1][1],self.collidesegment[1][2]),5)
                    else:
                        pygame.draw.line(self.layer,"#0000FF",(self.collidesegment[0][1],self.collidesegment[0][2]),(self.collidesegment[1][1],self.collidesegment[1][2]),5)
            else:
                self.collidesegment = None

    def setanim(self, name:str)->None:
        """Sets the animation to the name passed in.
        :param name: the name of the animation being swapped to"""
        if self.animname != name:
            self.animname = name
            self.frame = 0
            self.subframe = 0
        
    def animate(self)->None:
        """Iterates to the next animation frame"""
        if self.subframe > self.file["Hero"][self.animname][self.frame][5]:
            self.subframe = 0
            self.frame += 1
        else:
            self.subframe += 1
        if self.file["Hero"][self.animname][self.frame] == "Loop":
            self.frame = 0
            self.subframe = 0
        else:
            self.spriterect = (self.file["Hero"][self.animname][self.frame][0],
            self.file["Hero"][self.animname][self.frame][1],
            self.file["Hero"][self.animname][self.frame][2],
            self.file["Hero"][self.animname][self.frame][3])
            self.mirror = self.file["Hero"][self.animname][self.frame][4]
            
    def render(self)->None:
        """Renders the current animation frame"""
        self.sprite.fill("#FFFFFF")
        if self.dir == 1:
            if self.mirror:
                self.mirror = False
            else:
                self.mirror = True
        if self.mirror:
            self.sprite.blit(self.spritesheet,
            (0,0),
            self.spriterect)
            newsprite = pygame.transform.scale(self.sprite, (100,100))
            self.layer.blit(pygame.transform.flip(newsprite,True, False),
            (self.pos[0]-(self.size[0]/2)-self.camera.pos[0],
            self.pos[1]-(self.size[1]/2)-self.camera.pos[1]))
        else:
            self.sprite.blit(self.spritesheet,
            (0,0),
            self.spriterect)
            newsprite = pygame.transform.scale(self.sprite, (100,100))
            self.layer.blit(newsprite,
            (self.pos[0]-(self.file["Hero"][self.animname][self.frame][2]/2)-self.camera.pos[0],
            self.pos[1]-(self.size[1]/2)-self.camera.pos[1]))
