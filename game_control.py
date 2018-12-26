import pygame
from os import path
from pygame.locals import *
import random,math,mazeGen
import dungeon_player as dp
import ui,sound
import enemy as el
import dungeon_lib as dl
FONT=ui.LoadFont(24)

class gameControl:
    def __init__(self,surf,screen):
        self.surf=surf
        self.screen=screen
        self.state="ingame"
        self.events=[]
        self.go=True
        self.drawn=0
        self.log=["You awaken from a deep sleep."]
        self.controlToggle=False


        self.dialog=[]
        self.lastResult = "None"

        self.hudMoveButtons=[
        ui.Button(691,315,86,76,"TL",self.screen),
        ui.Button(778,315,83,76,"UP",self.screen),
        ui.Button(861,315,87,77,"TR",self.screen),
        ui.Button(690,392,87,77,"LEFT",self.screen),
        ui.Button(777,392,84,77,"DOWN",self.screen),
        ui.Button(860,392,88,77,"RIGHT",self.screen)]

        self.hudButtons=[
        ui.Button(715,295,82,82,"LK",self.screen),
        ui.Button(835,295,82,82,"INV",self.screen),
        ui.Button(715,415,82,82,"ATK",self.screen),
        ui.Button(835,415,82,82,"CHAR",self.screen),
        ui.Button(685,270,32,32,"TGM",self.screen)]

        self.combat=False
        self.turn=0

        self.soundMixer = sound.Mix()
        #self.soundMixer.mscPlay("track1")

    def newMap(self):
        self.currentLevel=mazeGen.generate(25)
        self.currentView=[]
        for a in self.currentLevel:
            self.currentView.append([1,]*len(self.currentLevel[0])) #fog off
            #self.currentView.append([0,]*len(self.currentLevel[0])) #fog on

        self.enemies=[]
        eX=0
        eY=0
        for block in self.currentLevel:
            for cell in block:
                if cell == 99:
                    end=(eX,eY)
                if cell == 12:
                    self.p=dp.Player(eX,eY)
                    self.p.gc=self
                if cell == 4:
                    self.enemies.append(
                    el.Enemy(eX,eY,4,self))
                eX+=1
            eX=0
            eY+=1

    def enemyUpdate(self):
        for enemy in self.enemies:
            enemy.update()

    def logUpdate(self,message):
        self.log.append(message)
        #self.log=self.log[1:]
        self.drawn=False

    def buttonUpdate(self,mpos):
        for b in self.hudButtons:
            if b.rect.collidepoint(mpos):
                if b.text == "TGM":
                    self.controlToggle=(not self.controlToggle)
                    self.soundMixer.sndPlay("flip")
                    self.drawn=False
        if not self.controlToggle:
            for b in self.hudButtons:
                if b.rect.collidepoint(mpos):
                    if b.text == "LK":
                        self.p.actionLook()
                    if b.text == "ATK":
                        if self.p.turns>0:
                            self.soundMixer.sndPlay("swing")
                            self.p.actionAttack()

        else:
            for b in self.hudMoveButtons:
                if b.rect.collidepoint(mpos):
                    if b.text == "UP":
                        self.p.actionMove("w")
                    if b.text == "DOWN":
                        self.p.actionMove("s")
                    if b.text == "LEFT":
                        self.p.actionMove("a")
                    if b.text == "RIGHT":
                        self.p.actionMove("d")
                    if b.text == "TL":
                        self.p.actionMove("q")
                    if b.text == "TR":
                        self.p.actionMove("e")

    def event(self,dlg=0):
        self.events=pygame.event.get()
        for e in self.events:
            if e.type == QUIT:
                self.go=False
                pygame.display.quit()
            if e.type == MOUSEBUTTONUP:
                if dlg==0:
                    self.buttonUpdate(e.pos)
                else:
                    dlg.buttonCheck(e.pos)

    def doDialog(self,dlg):
        self.soundMixer.sndPlay("popup")
        self.surf.fill((0,0,0))
        dl.drawHud(self)
        dl.drawView((self.p.x,self.p.y),self.currentLevel,self.p.facingDirection,self.surf)
        small=pygame.transform.scale(self.surf, (672,512))
        while dlg.result=="None":
            self.screen.blit(small,(0,0))
            dlg.Update()
            self.event(dlg)
            pygame.display.flip()
        self.drawn=0
        return dlg.result

    def doCombat(self,enemy):
        self.drawn=0
        self.combat=True
        self.p.lookAt((enemy.x,enemy.y))
        self.p.target=enemy
        self.soundMixer.sndPlay("popup")
        self.surf.fill((0,0,0))
        small=pygame.transform.scale(self.surf, (672,512))
        self.p.turns=int(1+self.p.stats['agi']/10)
        enemy.turns=int(1+enemy.stats['agi']/10)

        while enemy.hp>1:
            self.event()

            if self.drawn==0:
                self.surf.fill((0,0,0))
                dl.drawHud(self)
                dl.drawView((self.p.x,self.p.y),self.currentLevel,self.p.facingDirection,self.surf)
                small=pygame.transform.scale(self.surf, (672,512))
                self.screen.blit(small,(0,0))
                if not enemy.dead:dl.bar(self.screen,(0,200,20),-1,32,32,245,32,enemy.hp,enemy.maxhp)
                pygame.display.flip()
                self.drawn=1

            if not enemy.dead:
                if enemy.turns<1:
                    self.p.turns=int(1+self.p.stats['agi']/10)
                    enemy.turns=int(1+enemy.stats['agi']/10)

                if self.p.turns<1 and enemy.turns>0:
                    print (enemy.hp)
                    pygame.time.delay(200)
                    enemy.myTurn()
                    self.drawn=0


        self.drawn=0
        self.combat=False
        return "A"

    def update(self):
        #Player Update
        self.p.update()
        self.event()
        if self.drawn==0:
            #draw player view
            self.surf.fill((0,0,0))
            dl.drawHud(self)
            dl.drawView((self.p.x,self.p.y),self.currentLevel,self.p.facingDirection,self.surf)

            #scale player view
            small=pygame.transform.scale(self.surf, (672,512))

            self.screen.blit(small,(0,0))
            self.drawn=1
            self.enemyUpdate()

            pygame.display.flip()
