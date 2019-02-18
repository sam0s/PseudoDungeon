import dungeon_lib as dl
import pygame,items
import ui
from pygame.locals import *

lookIndex={3:"a chest",0:"a wall",1:"nothing",4:"a lowly goblin",98:"a way up",99:"a way down"}
weaponIndex={0:"dagger"}
key_directionIndex = {K_w:"w",K_s:"s",K_a:"a",K_d:"d",K_e:"e",K_q:"q",}
FACING_DIRECTIONS = ['n','e','s','w']
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y

        self.gc=None
        self.stats={'atk':25,'agi':25,'def':25,'mag':25,'vit':20,'crt':25}
        self.maxhp=int(10+(self.stats["vit"]*0.6))
        self.name="Craig"
        self.hp=int(self.maxhp)
        self.weapon=0

        self.xp=0
        self.nextxp=100
        self.skillpoints=32
        self.level=1
        items.loadItems("items.json")
        self.inventory = [items.getItem("Bread"),items.getItem("Dirk"),items.getItem("Bread"),items.getItem("Bread"),items.getItem("Axe"),]
        self.activeWeapon = [items.getItem("GoldSword")]
        self.facingIndex=0
        self.facingDirection=FACING_DIRECTIONS[self.facingIndex]
        self.moveW=[(0,-1),(1,0),(0,1),(-1,0)]
        self.moveS=[(0,1),(-1,0),(0,-1),(1,0)]
        self.moveA=[(-1,0),(0,-1),(1,0),(0,1)]
        self.moveD=[(1,0),(0,1),(-1,0),(0,-1)]
        self.turns=1

    def takeHit(self,hit):
        self.hp-=hit
        if hit>=1:
            self.gc.soundMixer.sndPlay("player_hit")

    def actionMove(self,direction):
        if not self.gc.combat:
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

            self.gc.currentLevel[yprev][xprev]=1
            self.gc.currentLevel[self.y][self.x]=12


            #check turning
            if direction == "q":
                self.facingIndex-=1
            if direction == "e":
                self.facingIndex+=1

            if self.facingIndex>3:self.facingIndex=0
            if self.facingIndex<0:self.facingIndex=3
            self.facingDirection=FACING_DIRECTIONS[self.facingIndex]

    def actionAttack(self):
        if self.gc.combat:
            if self.turns>0:
                self.turns-=1
                self.gc.soundMixer.sndPlay("swing")
                self.target.takeHit(dl.damageCalc(self,self.target))
                self.gc.drawn=0
                if self.turns!=0:pygame.time.delay(200)

    def actionLook(self):
        x1=self.x+self.moveW[self.facingIndex][0]
        y1=self.y+self.moveW[self.facingIndex][1]
        front=self.gc.currentLevel[y1][x1]

        if front == 3:
            a=self.gc.doDialog(ui.dialog(32,32,("Open the chest before you?",["Open it","Discard it"]),self.gc.screen,0))
            if a == "Open it":
                front=lookIndex[front]
                self.gc.logUpdate("You open "+front+".")
                self.gc.currentLevel[y1][x1]=1
        else:
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

    def lookAt(self,pos):
        posit=0
        if pos[0]>self.x and pos[1]==self.y:
            posit=1
        if pos[0]<self.x and pos[1]==self.y:
            posit=3
        if pos[1]<self.y and self.x==pos[0]:
            posit=0
        if pos[1]>self.y and self.x==pos[0]:
            posit=2
        self.facingIndex=posit
        self.facingDirection=FACING_DIRECTIONS[self.facingIndex]

    def update(self):
        for event in self.gc.events:
            if event.type == KEYDOWN:
                if event.key in [K_w,K_s,K_a,K_d,K_e,K_q]:
                    self.actionMove(key_directionIndex[event.key])
