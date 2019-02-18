#!/usr/bin/env python

"""
escmenu.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []


import pygame
from random import choice
from pygame import *
import ui as ui
from os import path
import items

pygame.init()
font = ui.LoadFont(32,'uif')
fontItems = ui.LoadFont(19,'uif')


itemFrame=pygame.image.load(path.join("images","items.png")).convert()

class EscMenu(object):
    def __init__(self,surf,world):

        self.player_stats_drawn=0

        self.surf=surf
        self.world=world
        self.small = pygame.sprite.Group()
        self.tab="items"
        self.created=0

        #BUTTONS INIT
        self.tabs=[ui.Button(650,50,100,32,"Player",self.surf),
                    ui.Button(650,100,100,32,"Items",self.surf),
                    ui.Button(650,200,100,32,"Go Back",self.surf),
                    ui.Button(650,300,100,32,"Leave",self.surf)]

        self.invbuttons=[ui.Button(500,430,100,32,"Drop",self.surf),
                            ui.Button(500,385,100,32,"Use",self.surf)]

        self.levelbuttons=[ui.Button(245,267,32,32,"+1",self.surf),
                            ui.Button(245,312,32,32,"+1",self.surf),
                            ui.Button(245,357,32,32,"+1",self.surf),
                            ui.Button(245,403,32,32,"+1",self.surf),
                            ui.Button(245,448,32,32,"+1",self.surf),
                            ui.Button(245,494,32,32,"+1",self.surf),]


        self.invx=0
        self.invy=0

        self.drawn=0

    def Draw(self):
        #press ESC to exit menu
        if self.drawn==0:
            if self.tab=="items":
                self.surf.fill((0,0,0))
                oef=230+(self.invy*42)
                oef2=43+(self.invx*38)
                #draw selected item, look at "USE" code
                self.surf.blit(itemFrame,(0,0))
                pygame.draw.circle(self.surf,(255,0,0),(oef2,oef),5,0)

                try:
                    item=self.world.p.inventory[(self.invx+(self.invy)*12)]
                    self.surf.blit(pygame.transform.scale(item.image,(98,98)),(15,83))
                    y=88
                    for f in item.descr:
                        self.surf.blit(font.render(f,0,(255,255,255),(0,0,0)),(122,y))
                        y+=18
                except IndexError:
                    pass
                    ##print "no item selected";item=None

                x=30
                y=229
                for f in self.world.p.activeWeapon:
                    self.surf.blit(f.image,(30,16))
                for f in self.world.p.inventory:
                    #pygame.draw.rect(self.surf,(255,0,0),(x,y,26,26),0)
                    toDraw=f.image
                    if isinstance(f,items.Weapon):
                        toDraw=pygame.transform.scale(f.image,(26,26))
                    self.surf.blit(toDraw,(x,y))

                    self.surf.blit(fontItems.render(str(f.stack),0,(255,255,255),(0,0,0)),(x,y))
                    x+=38
                    if x>470:
                        x=30
                        y+=41
            if self.tab=="player":
                x=1
                self.surf.fill((0,0,0))
                b=[
                font.render(str(self.world.p.name)+": level "+str(self.world.p.level),0,(255,255,255),(0,0,0)),
                font.render("XP: "+str(self.world.p.xp)+"/"+str(self.world.p.nextxp),0,(255,255,255),(0,0,0)),
                font.render("",0,(0,0,0),(0,0,0)),
                font.render("Skill Points: "+str(self.world.p.skillpoints),0,(0,0,0),(0,0,0)),
                font.render("-----------------------",0,(255,255,255),(0,0,0)),
                font.render("Attack: "+str(self.world.p.stats["atk"]),0,(255,255,255),(0,0,0)),
                font.render("Agility: "+str(self.world.p.stats["agi"]),0,(255,255,255),(0,0,0)),
                font.render("Defense: "+str(self.world.p.stats["def"]),0,(255,255,255),(0,0,0)),
                font.render("Magic: "+str(self.world.p.stats["mag"]),0,(255,255,255),(0,0,0)),
                font.render("Vitality: "+str(self.world.p.stats["vit"]),0,(255,255,255),(0,0,0)),
                font.render("Critical: "+str(self.world.p.stats["crt"]),0,(255,255,255),(0,0,0)),
                font.render("-----------------------",0,(255,255,255),(0,0,0)),
                font.render("",0,(0,0,0),(0,0,0))
                ]
                if self.world.p.skillpoints>0:
                    b[3]=font.render("Skill Points: "+str(self.world.p.skillpoints),0,(25,255,50),(0,0,0))
                for f in b:
                    self.surf.blit(f,(32,x*45))
                    x+=1
                self.player_stats_drawn=1
            self.drawn=1

        for e in self.world.events:
            if e.type == MOUSEBUTTONUP and e.button == 1:
                self.drawn=0
                mse = e.pos

                if self.tab=="player":
                    if self.world.p.skillpoints>0:
                        for b in self.levelbuttons:
                            if b.rect.collidepoint(mse):
                                self.world.p.skillpoints-=1
                                if self.levelbuttons.index(b)==0:
                                    self.world.p.stats["atk"]+=1
                                if self.levelbuttons.index(b)==1:
                                    self.world.p.stats["agi"]+=1
                                if self.levelbuttons.index(b)==2:
                                    self.world.p.stats["def"]+=1
                                if self.levelbuttons.index(b)==3:
                                    self.world.p.stats["mag"]+=1
                                if self.levelbuttons.index(b)==4:
                                    self.world.p.stats["vit"]+=1
                                if self.levelbuttons.index(b)==5:
                                    self.world.p.stats["crt"]+=1

                #Handle inventory related buttons
                if self.tab=="items":
                    for b in self.invbuttons:
                        if b.rect.collidepoint(mse):
                            self.drawn=0
                            try:item=self.world.p.inventory[(self.invx+(self.invy)*12)]
                            except IndexError:
                                pass
                                ##print "no item selected";item=None
                            if item:
                                if b.text=="Use":
                                    if isinstance(item, items.Food):
                                        self.world.p.hp+=item.consumeVal
                                        if self.world.p.hp>self.world.p.maxhp:self.world.p.hp=self.world.p.maxhp
                                        if item.stack==1:
                                            self.world.p.inventory.pop((self.invx+(self.invy)*12))
                                        else:
                                            item.stack-=1
                                    if isinstance(item, items.Weapon):
                                        if item.name!=self.world.p.activeWeapon[0].name:
                                            if item.stack>1:
                                                item.stack-=1
                                                self.world.p.giveItem(self.world.player.activeWeapon[0])
                                                self.world.p.activeWeapon=[item]
                                            else:
                                                self.world.p.giveItem(self.world.player.activeWeapon[0])
                                                self.world.p.activeWeapon=[item]
                                                self.world.p.inventory.pop((self.invx+(self.invy)*12))

                                if b.text=="Drop":
                                        ###print "dropped item"
                                        if item.stack>1:
                                            item.stack-=1
                                        else:
                                            self.world.p.inventory.pop((self.invx+(self.invy)*12))
                            #self.world.Draw(False)


                    #INVENTORY DOT
                    if mse[0]<485:
                        if mse[1]>228:
                            if mse[1]>426:
                                self.invy=5
                            elif mse[1]>385:
                                self.invy=4
                            elif mse[1]>343:
                                self.invy=3
                            elif mse[1]>303:
                                self.invy=2
                            elif mse[1]>262:
                                self.invy=1
                            else:
                                self.invy=0

                        if mse[0]>21:
                            if mse[0]>442:
                                self.invx=11
                            elif mse[0]>405:
                                self.invx=10
                            elif mse[0]>366:
                                self.invx=9
                            elif mse[0]>328:
                                self.invx=8
                            elif mse[0]>290:
                                self.invx=7
                            elif mse[0]>252:
                                self.invx=6
                            elif mse[0]>213:
                                self.invx=5
                            elif mse[0]>175:
                                self.invx=4
                            elif mse[0]>136:
                                self.invx=3
                            elif mse[0]>100:
                                self.invx=2
                            elif mse[0]>61:
                                self.invx=1
                            else:
                                self.invx=0


                #Handle the general buttons
                for b in self.tabs:
                    if b.rect.collidepoint(e.pos):
                        if b.text=="Go Back":
                            self.world.changeState("game")
                            self.drawn=0
                        if b.text=="Player":
                            self.player_stats_drawn=0
                            self.tab="player"
                        if b.text=="Items":
                            self.tab="items"
        #DRAW BUTTONS
        for e in self.world.events:
            if e.type == QUIT:
                self.world.Close()

        for f in self.tabs:
            f.Update()

        if self.tab=="player":
            if self.world.p.skillpoints>0:
                for f in self.levelbuttons:
                    f.Update()
        if self.tab=="items":
            for f in self.invbuttons:
                f.Update()
