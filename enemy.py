import dungeon_lib as dl
import pygame,random,math
from pygame.locals import *

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
#handle hud and other control
class Enemy(object):
    def __init__(self,x,y,et,gc):
        self.gc=gc
        self.x,self.y,self.et=x,y,et
        self.stats={'atk':25,'agi':10,'def':10,'mag':0,'vit':25,'crt':25}
        self.maxhp=int(3+(self.stats["vit"]*0.6))
        self.hp=self.maxhp
        self.combat = False
        self.turns=1
        self.name = "Goblin"
        self.dead=False

    def movePos(self,xchange,ychange):
        if xchange==ychange or xchange == -ychange:
            return 0
        if self.gc.currentLevel[self.y+ychange][self.x+xchange]==1:
            self.gc.currentLevel[self.y][self.x]=1
            self.x+=xchange
            self.y+=ychange
            self.gc.currentLevel[self.y][self.x]=4
    def myTurn(self):
        if not self.gc.combat:
            self.movePos(random.choice([-1,1,0]),random.choice([-1,1,0]))
            if distance((self.x,self.y),(self.gc.p.x,self.gc.p.y))==1:
                self.gc.doCombat(self)
        else:
            print("enemy turn")
            self.gc.p.takeHit(dl.damageCalc(self,self.gc.p))
            self.turns-=1
    def takeHit(self,hit):
        self.hp-=hit
        if hit>=1:
            self.gc.soundMixer.sndPlay("hit1")
            animator = dl.animation("slash")
            while not animator.done:
                animator.play(self.gc.screen)
        if self.hp<=1:
            self.gc.enemies.pop(self.gc.enemies.index(self))
            self.gc.currentLevel[self.y][self.x]=1
            self.dead=True

    def update(self):
        self.myTurn()
