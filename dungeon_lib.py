import pygame
from os import path
from pygame.locals import *

#load in images

#enviro
floor=pygame.image.load(path.join("images","enviro","floor.png")).convert()
wall=pygame.image.load(path.join("images","enviro","wall.png")).convert()
enemy1=pygame.image.load(path.join("images","enemy","enemy1.png")).convert()

#hud iamges
movecontrol=pygame.image.load(path.join("images","hud","control.png")).convert()

#set colorkeys
wall.set_colorkey((0,255,0))
enemy1.set_colorkey((0,255,0))

#handle hud and other control
class gameControl:
    def __init__(self,surf):
        self.surf=surf
        self.state="ingame"
        self.controlsImage=pygame.image.load(path.join("images","hud","control.png")).convert()
        self.events=[]
        self.go=True
        self.drawn=False

    def update(self):
        for e in self.events:
            if e.type == QUIT:
                self.go=False
                pygame.display.quit()

        if self.drawn==False:

            #draw player view
            self.surf.fill((0,0,0))
            drawView((self.p.x,self.p.y),self.currentLevel,self.p.facingDirection,self.surf)

            #scale player view
            small=pygame.transform.scale(self.surf, (672,512))
            self.screen.blit(small,(0,0))
            drawMiniMap(self)
            self.drawn=True

            drawHud(self)

            pygame.display.flip()

def drawMiniMap(gcObj):
    x=1
    y=0

    px=gcObj.p.x
    py=gcObj.p.y

    px+=2

    for block in gcObj.currentLevel:
        for cell in block:
            x+=1

            if cell == 0:c=(150,150,150)
            if cell == 1:c=(25,25,25)
            if cell == 4:c=(250,0,0)
            if cell == 3:c=(0,0,255)

            pygame.draw.rect(gcObj.screen,(c),(670+x*6,y*6,6,6),0)


        x=1
        y+=1

    pygame.draw.rect(gcObj.screen,((0,255,0)),(670+px*6,py*6,6,6),0)

def drawTile(tile,pos,side,surf,mini):
    print (tile)
    if mini:
        if tile == 1: c=(25,25,25)
        if tile == 0: c=(150,150,150)
        if tile == 4: c=(250,25,25)


    if tile == 1: tile = floor
    if tile == 0: tile = wall
    if tile == 4: tile = enemy1
    if tile == 3: tile = floor

    x=tile.subsurface(960*pos[0],720*pos[1],960,720)
    xblit=0
    if side == 0:
        x=x.subsurface(0,0,960/2,720)
    if side == 2:
        x=x.subsurface(960/2,0,960/2,720)
        xblit=960/2

    surf.blit(x,(xblit,0))

def drawView(pos,level,facing,surf,mini=False):
    if facing=="n":
        drawTile(level[pos[1]-2][pos[0]-2],(0,0),0,surf,mini) #outer sides back left
        drawTile(level[pos[1]-2][pos[0]+2],(0,0),2,surf,mini) #outer sides back right
        drawTile(level[pos[1]-2][pos[0]-1],(1,0),0,surf,mini) #inner sides back left
        drawTile(level[pos[1]-2][pos[0]+1],(1,0),2,surf,mini) #inner sides back right
        drawTile(level[pos[1]-2][pos[0]],(2,0),1,surf,mini) #back mid

        drawTile(level[pos[1]-1][pos[0]-2],(3,0),0,surf,mini) #mid far sides left
        drawTile(level[pos[1]-1][pos[0]+2],(3,0),2,surf,mini) #mid far sides right

        drawTile(level[pos[1]-1][pos[0]-1],(0,1),0,surf,mini) #mid sides left
        drawTile(level[pos[1]-1][pos[0]+1],(0,1),2,surf,mini) #mid sides right
        drawTile(level[pos[1]-1][pos[0]],(1,1),1,surf,mini) #mid

        drawTile(level[pos[1]][pos[0]-1],(2,1),0,surf,mini) #close sides left
        drawTile(level[pos[1]][pos[0]+1],(2,1),2,surf,mini) #close sides right
        drawTile(level[pos[1]+0][pos[0]+0],(3,1),1,surf,mini) #mid close

    if facing=="s":
        drawTile(level[pos[1]+2][pos[0]+2],(0,0),0,surf,mini) #outer sides back left
        drawTile(level[pos[1]+2][pos[0]-2],(0,0),2,surf,mini) #outer sides back right
        drawTile(level[pos[1]+2][pos[0]+1],(1,0),0,surf,mini) #inner sides back left
        drawTile(level[pos[1]+2][pos[0]-1],(1,0),2,surf,mini) #inner sides back right
        drawTile(level[pos[1]+2][pos[0]],(2,0),1,surf,mini) #back mid

        drawTile(level[pos[1]+1][pos[0]+2],(3,0),0,surf,mini) #mid far sides left
        drawTile(level[pos[1]+1][pos[0]-2],(3,0),2,surf,mini) #mid far sides right

        drawTile(level[pos[1]+1][pos[0]+1],(0,1),0,surf,mini) #mid sides left
        drawTile(level[pos[1]+1][pos[0]-1],(0,1),2,surf,mini) #mid sides right
        drawTile(level[pos[1]+1][pos[0]],(1,1),1,surf,mini) #mid

        drawTile(level[pos[1]][pos[0]+1],(2,1),0,surf,mini) #close sides left
        drawTile(level[pos[1]][pos[0]-1],(2,1),2,surf,mini) #close sides right
        drawTile(level[pos[1]+0][pos[0]+0],(3,1),1,surf,mini) #mid close

    if facing=="w":
        drawTile(level[pos[1]+2][pos[0]-2],(0,0),0,surf,mini) #outer sides back left
        drawTile(level[pos[1]-2][pos[0]-2],(0,0),2,surf,mini) #outer sides back right
        drawTile(level[pos[1]+1][pos[0]-2],(1,0),0,surf,mini) #inner sides back left
        drawTile(level[pos[1]-1][pos[0]-2],(1,0),2,surf,mini) #inner sides back right
        drawTile(level[pos[1]][pos[0]-2],(2,0),1,surf,mini) #back mid

        drawTile(level[pos[1]+2][pos[0]-1],(3,0),0,surf,mini) #mid far sides left
        drawTile(level[pos[1]-2][pos[0]-1],(3,0),2,surf,mini) #mid far sides right

        drawTile(level[pos[1]+1][pos[0]-1],(0,1),0,surf,mini) #mid sides left
        drawTile(level[pos[1]-1][pos[0]-1],(0,1),2,surf,mini) #mid sides right
        drawTile(level[pos[1]][pos[0]-1],(1,1),1,surf,mini) #mid

        drawTile(level[pos[1]+1][pos[0]],(2,1),0,surf,mini) #close sides left
        drawTile(level[pos[1]-1][pos[0]],(2,1),2,surf,mini) #close sides right
        drawTile(level[pos[1]][pos[0]],(3,1),1,surf,mini) #mid close

    if facing=="e":
        drawTile(level[pos[1]-2][pos[0]+2],(0,0),0,surf,mini) #outer sides back left
        drawTile(level[pos[1]+2][pos[0]+2],(0,0),2,surf,mini) #outer sides back right
        drawTile(level[pos[1]-1][pos[0]+2],(1,0),0,surf,mini) #inner sides back left
        drawTile(level[pos[1]+1][pos[0]+2],(1,0),2,surf,mini) #inner sides back right
        drawTile(level[pos[1]][pos[0]+2],(2,0),1,surf,mini) #back mid

        drawTile(level[pos[1]-2][pos[0]+1],(3,0),0,surf,mini) #mid far sides left
        drawTile(level[pos[1]+2][pos[0]+1],(3,0),2,surf,mini) #mid far sides right

        drawTile(level[pos[1]-1][pos[0]+1],(0,1),0,surf,mini) #mid sides left
        drawTile(level[pos[1]+1][pos[0]+1],(0,1),2,surf,mini) #mid sides right
        drawTile(level[pos[1]][pos[0]+1],(1,1),1,surf,mini) #mid

        drawTile(level[pos[1]-1][pos[0]],(2,1),0,surf,mini) #close sides left
        drawTile(level[pos[1]+1][pos[0]],(2,1),2,surf,mini) #close sides right
        drawTile(level[pos[1]][pos[0]],(3,1),1,surf,mini) #mid close

def drawHud(gcEnt):
    gcEnt.screen.blit(movecontrol,(670,541))

    mmb=pygame.Surface((4,4))
    mmb.fill((255,0,0))
