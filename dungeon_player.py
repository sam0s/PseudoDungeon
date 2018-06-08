import dungeon_lib as dl
import pygame
from pygame.locals import *

class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y

        self.hp=100
        self.gc=None

        self.facingIndex=0
        self.facingDirections=['n','e','s','w']
        self.facingDirection=self.facingDirections[self.facingIndex]
        self.moveW=[(0,-1),(1,0),(0,1),(-1,0)]
        self.moveS=[(0,1),(-1,0),(0,-1),(1,0)]
        self.moveA=[(-1,0),(0,-1),(1,0),(0,1)]
        self.moveD=[(1,0),(0,1),(-1,0),(0,-1)]
    def checkFront(self):
        xx=self.x+self.moveW[self.facingIndex][0]
        yy=self.y+self.moveW[self.facingIndex][1]
        print(self.gc.currentLevel[yy][xx])
        self.gc.currentLevel[yy][xx]=1

    def update(self):
        for event in self.gc.events:
            if event.type == KEYDOWN:
                self.gc.drawn=False
                #turning
                if event.key == K_SPACE:
                    self.checkFront()
                if event.key == K_e or event.key == K_q:
                    if event.key == K_e:
                        self.facingIndex+=1
                    if event.key == K_q:
                        self.facingIndex-=1
                    if self.facingIndex>3:self.facingIndex=0
                    if self.facingIndex<0:self.facingIndex=3
                    self.facingDirection=self.facingDirections[self.facingIndex]


                #movement
                if event.key in [K_w,K_s,K_a,K_d]:
                    self.moving = 1
                    xprev,yprev=self.x,self.y
                    if event.key == K_w:
                        self.x+=self.moveW[self.facingIndex][0]
                        self.y+=self.moveW[self.facingIndex][1]
                    if event.key == K_s:
                        self.x+=self.moveS[self.facingIndex][0]
                        self.y+=self.moveS[self.facingIndex][1]
                    if event.key == K_a:
                        self.x+=self.moveA[self.facingIndex][0]
                        self.y+=self.moveA[self.facingIndex][1]
                    if event.key == K_d:
                        self.x+=self.moveD[self.facingIndex][0]
                        self.y+=self.moveD[self.facingIndex][1]

                    #collision
                    if self.gc.currentLevel[self.y][self.x]!=1:
                        self.x,self.y=xprev,yprev
