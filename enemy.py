import dungeon_lib as dl
import pygame,random,math,items,json
from pygame.locals import *
from os import path
items.loadItems("items.json")
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def get_stats_enemy(enemy_id):
    return_data = {}

    with open(path.join("enemy.json")) as f:
        jsondata = json.load(f)

        #GRAB STATS FROM JSON SHEET
        x=0
        for f in ['atk','agi','def','mag','vit','crt']:
            return_data[f] = jsondata["Normal"][str(enemy_id)]["stats"][x]
            print(return_data[f])
            x+=1

    return return_data

def get_name_enemy(enemy_id):
    with open(path.join("enemy.json")) as f:
        jsondata = json.load(f)
        return_data = jsondata["Normal"][str(enemy_id)]["name"]
    return return_data

class Enemy:
    def __init__(self,x,y,et,gc):
        self.gc=gc
        self.x,self.y,self.et=x,y,et
        self.stats = get_stats_enemy(et);
        self.maxhp=int(3+(self.stats["vit"]*0.6))
        self.activeWeapon = [items.getItem("Axe")]
        self.hp=self.maxhp
        self.combat = False
        self.turns=1
        self.name = get_name_enemy(et)
        self.dead=False

    def movePos(self,xchange,ychange):
        if xchange==ychange or xchange == -ychange:
            return 0
        if self.gc.currentLevel[self.y+ychange][self.x+xchange]==1:
            self.gc.currentLevel[self.y][self.x]=1
            self.x+=xchange
            self.y+=ychange
            self.gc.currentLevel[self.y][self.x]=self.et

    def myTurn(self):
        if not self.gc.combat:
            self.movePos(random.choice([-1,1,0]),random.choice([-1,1,0]))
            if distance((self.x,self.y),(self.gc.p.x,self.gc.p.y))==1:
                self.gc.doCombat(self)
        else:
            self.gc.drawn=0
            self.gc.p.takeHit(dl.damageCalc(self,self.gc.p))
            self.turns-=1
    def takeHit(self,hit):
        if not self.dead:
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
