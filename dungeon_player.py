import dungeon_lib as dl
import pygame
import ui
from pygame.locals import *

lookIndex={3:"a chest",0:"a wall",1:"nothing",4:"a lowly goblin",98:"a way up",99:"a way down"}

class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y

        self.hp=100
        self.gc=None

        #power, defense,
        #attack = d20 + power
        #defense = d8% reduction of dmg (roll defense/100 chance to block)

        self.stats={'p':1,'d':1,'a':1}


        self.facingIndex=0
        self.facingDirections=['n','e','s','w']
        self.facingDirection=self.facingDirections[self.facingIndex]
        self.moveW=[(0,-1),(1,0),(0,1),(-1,0)]
        self.moveS=[(0,1),(-1,0),(0,-1),(1,0)]
        self.moveA=[(-1,0),(0,-1),(1,0),(0,1)]
        self.moveD=[(1,0),(0,1),(-1,0),(0,-1)]

    def actionMove(self,direction):
        self.gc.drawn=0
        self.moving = 1
        xprev,yprev=self.x,self.y
        if direction == "w":
            self.x+=self.moveW[self.facingIndex][0]
            self.y+=self.moveW[self.facingIndex][1]
        if direction == "s":
            self.x+=self.moveS[self.facingIndex][0]
            self.y+=self.moveS[self.facingIndex][1]
        if direction == "a":
            self.x+=self.moveA[self.facingIndex][0]
            self.y+=self.moveA[self.facingIndex][1]
        if direction == "d":
            self.x+=self.moveD[self.facingIndex][0]
            self.y+=self.moveD[self.facingIndex][1]

        if self.gc.currentLevel[self.y][self.x]!=1:
            self.x,self.y=xprev,yprev

        #check turning
        if direction == "q":
            self.facingIndex-=1
        if direction == "e":
            self.facingIndex+=1

        if self.facingIndex>3:self.facingIndex=0
        if self.facingIndex<0:self.facingIndex=3
        self.facingDirection=self.facingDirections[self.facingIndex]

    def actionAttack(self):
        x1=self.x+self.moveW[self.facingIndex][0]
        y1=self.y+self.moveW[self.facingIndex][1]
        front=self.gc.currentLevel[y1][x1]
        #hit scan
        for e in self.gc.enemies:
            if e.x==x1:
                if e.y==y1:
                    e.takeHit(21)
                    break

        self.gc.logUpdate(str(front))

    def actionLook(self):
        x1=self.x+self.moveW[self.facingIndex][0]
        y1=self.y+self.moveW[self.facingIndex][1]
        front=self.gc.currentLevel[y1][x1]

        if front == 3:
            self.gc.dialog.append(ui.dialog(32,32,("Open the chest before you?",["Open it","Discard it"]),self.gc.screen,0))

        front=lookIndex[front]
        back=""
        if self.gc.currentLevel[y1][x1]!=0:
            x2=x1+self.moveW[self.facingIndex][0]
            y2=y1+self.moveW[self.facingIndex][1]
            back=self.gc.currentLevel[y2][x2]
            back=lookIndex[back]

        if len(back)<1:
            self.gc.logUpdate("You see "+front+".")
        else:
            self.gc.logUpdate("You see "+front+", and behind that you see "+back+".")

    def update(self):
        for event in self.gc.events:
            #key presses
            if event.type == KEYDOWN:
                #turning
                if event.key == K_e or event.key == K_q:
                    if event.key == K_e:
                        self.actionMove("e")
                    if event.key == K_q:
                        self.actionMove("q")
                #movement
                if event.key in [K_w,K_s,K_a,K_d]:
                    if event.key == K_w:
                        self.actionMove("w")
                    if event.key == K_s:
                        self.actionMove("s")
                    if event.key == K_a:
                        self.actionMove("a")
                    if event.key == K_d:
                        self.actionMove("d")
