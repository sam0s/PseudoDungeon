import pygame
from os import path
from pygame.locals import *
import random,math,mazeGen
import dungeon_player as dp
import ui

FONT=ui.LoadFont(24)

#load in images

#enviro
floor=pygame.image.load(path.join("images","enviro","floor.png")).convert()
wall=pygame.image.load(path.join("images","enviro","wall.png")).convert()
chest=pygame.image.load(path.join("images","enviro","chest.png")).convert()
enemy1=pygame.image.load(path.join("images","enemy","enemy1.png")).convert()
floor_down=pygame.image.load(path.join("images","enviro","floor_down.png")).convert()
floor_up=pygame.image.load(path.join("images","enviro","floor_up.png")).convert()

#hud iamges
bordersImage=pygame.image.load(path.join("images","hud","borders.png")).convert()
cursor=pygame.image.load(path.join("images","hud","cursor.png")).convert()

button_images=[
pygame.image.load(path.join("images","hud","look_button.png")).convert(),
pygame.image.load(path.join("images","hud","inventory_button.png")).convert(),
pygame.image.load(path.join("images","hud","attack_button.png")).convert(),
pygame.image.load(path.join("images","hud","char_button.png")).convert(),
pygame.image.load(path.join("images","hud","control.png")).convert(),
pygame.image.load(path.join("images","hud","mtoggle_button.png")).convert(),
]

#set colorkeys
for button in button_images:
    button.set_colorkey((255,0,255))

bordersImage.set_colorkey((255,0,255))
cursor.set_colorkey((255,0,255))
wall.set_colorkey((255,0,255))
floor_down.set_colorkey((255,0,255))
floor_up.set_colorkey((255,0,255))
enemy1.set_colorkey((255,0,255))
chest.set_colorkey((255,0,255))

northCone=[[-1,0],[1,0],[0,-1],[-1,-1],[-2,-1],[1,-1],[2,-1],[0,-2],[-1,-2],[-2,-2],[1,-2],[2,-2]
]
eastCone=[[0,-1],[0,1],[1,0],[1,-1],[1,-2],[1,1],[1,2],[2,0],[2,-1],[2,-2],[2,1],[2,2],
]
southCone=[[-1,0],[1,0],[0,1],[-1,1],[-2,1],[1,1],[2,1],[-2,2],[-1,2],[0,2],[1,2],[2,2]
]
westCone=[[0,-1],[0,1],[-1,0],[-1,1],[-1,2],[-1,-1],[-1,-2],[-2,0],[-2,1],[-2,2],[-2,-1],[-2,-2]
]

#handle hud and other control
class Enemy(object):
    def __init__(self,x,y,et,gc):
        self.gc=gc
        self.x,self.y,self.et=x,y,et
        self.hp=10
    def takeHit(self,hit):
        self.hp-=3
        print(self.hp)
        if self.hp<=0:
            self.gc.enemies.pop(self.gc.enemies.index(self))
            self.gc.currentLevel[self.y][self.x]=1

    def update(self):
        pass

class gameControl:
    def __init__(self,surf,screen):
        self.surf=surf
        self.screen=screen
        self.state="ingame"
        self.events=[]
        self.go=True
        self.drawn=0
        self.log=["You awaken."]
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

    def newMap(self):
        self.currentLevel,xy,end=mazeGen.generate(25)
        self.currentView=[]
        for a in self.currentLevel:
            self.currentView.append([1,]*len(self.currentLevel[0]))
        self.p=dp.Player(*xy)
        self.p.gc=self
        self.enemies=[]
        eX=0
        eY=0
        for block in self.currentLevel:
            #print(block)
            for cell in block:

                if cell == 4:
                    self.enemies.append(
                    Enemy(eX,eY,4,self))
                    print(cell,eX,eY)
                    #eX+=1
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
                    self.drawn=False
        if not self.controlToggle:
            for b in self.hudButtons:
                if b.rect.collidepoint(mpos):
                    if b.text == "LK":
                        self.p.actionLook()
                    if b.text == "ATK":
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

    def event(self):
        for e in self.events:
            if e.type == QUIT:
                self.go=False
                pygame.display.quit()
            if e.type == MOUSEBUTTONUP:
                if len(self.dialog)==0:
                    self.buttonUpdate(e.pos)
                else:
                    self.dialog[0].buttonCheck(e.pos)
                    if self.dialog[0].result != "None":
                        self.lastResult=self.dialog[0].result
                        self.dialog.pop(0)
                        self.drawn=False

    def doDialog(self):
        pass
        #make it work 


    def update(self):
        if len(self.dialog)>0:
            self.surf.fill((0,0,0))
            drawHud(self)
            drawView((self.p.x,self.p.y),self.currentLevel,self.p.facingDirection,self.surf)
            #scale player view
            small=pygame.transform.scale(self.surf, (672,512))
            self.screen.blit(small,(0,0))
            self.dialog[0].Update()
            self.event()
            pygame.display.flip()
        else:
            #Player Update
            self.p.update()
            self.event()
            if self.drawn==0:
                #draw player view
                self.surf.fill((0,0,0))
                drawHud(self)
                drawView((self.p.x,self.p.y),self.currentLevel,self.p.facingDirection,self.surf)

                #scale player view
                small=pygame.transform.scale(self.surf, (672,512))

                self.screen.blit(small,(0,0))
                self.enemyUpdate()

                self.drawn=1
                pygame.display.flip()

##### HUDV FUNCTIONS START
def drawMiniMap(gcObj):
    x=1
    y=0

    px=gcObj.p.x
    py=gcObj.p.y
    px+=2

    offset=668
    mmsize = 9

    if gcObj.p.facingDirection=="n":pTri=[( (offset+px*mmsize), (py*mmsize)+mmsize ),( (offset+px*mmsize)+mmsize/2, (py*mmsize) ),( (offset+px*mmsize)+mmsize, (py*mmsize)+mmsize )]
    if gcObj.p.facingDirection=="e":pTri=[(offset+px*mmsize,py*mmsize),( (offset+px*mmsize)+mmsize, (py*mmsize)+mmsize/2 ),( (offset+px*mmsize), (py*mmsize)+mmsize )]
    if gcObj.p.facingDirection=="s":pTri=[( (offset+px*mmsize), (py*mmsize)),( (offset+px*mmsize)+mmsize/2, (py*mmsize)+mmsize ),( (offset+px*mmsize)+mmsize, (py*mmsize) )]
    if gcObj.p.facingDirection=="w":pTri=[( (offset+px*mmsize)+mmsize, (py*mmsize)),( (offset+px*mmsize), (py*mmsize)+mmsize/2 ),( (offset+px*mmsize)+mmsize, (py*mmsize)+mmsize )]



    #pygame.draw.polygon(gcObj.screen, (c), tri,width=0)
    px-=2

    for a in {"n":northCone,"e":eastCone,"s":southCone,"w":westCone}[gcObj.p.facingDirection]:
        gcObj.currentView[py+a[1]][px+a[0]]=1

    for block in gcObj.currentLevel:
        for cell in block:
            x+=1
            c=(3,3,3)

            if gcObj.currentView[y][x-2]==1:
                if cell == 0:c=(150,150,150)
                if cell == 1:c=(25,25,25)
                if cell == 4:c=(250,0,0)
                if cell == 3:c=(0,0,255)
                if cell == 98:c=(0,255,255)
                if cell == 99:c=(0,230,100)

            pygame.draw.rect(gcObj.screen,(c),(offset+x*9,y*9,9,9),0)


        x=1
        y+=1
    pygame.draw.polygon(gcObj.screen, ((0,255,0)),pTri,0)
    #pygame.draw.rect(gcObj.screen,((0,255,0)),(mmsize70+px*mmsize,py*mmsize,mmsize,mmsize),0)

def drawLog(gcObj):
    pygame.draw.rect(gcObj.screen,(255,255,255),(0,516,672,204),0)
    bottom=708
    for msg in reversed(gcObj.log):
        msgImg=FONT.render("> "+str(msg),1,(255,0,0),(255,255,255))
        space=msgImg.get_height()+2
        y=bottom-space
        gcObj.screen.blit(msgImg,(9,y))
        bottom-=space
    #gcObj.screen.blit(FONT.render("> Does this font and style look okay?",1,(255,0,0),(255,255,255)),(9,570))

def drawButtons(gcObj):
    #draw either controls for movement or actions

    #black-drop
    pygame.draw.rect(gcObj.screen,(0,0,0),(685,270,300,400),0)

    if not gcObj.controlToggle:
        gcObj.screen.blit(button_images[5].subsurface(0,0,32,32),(685,270))
        gcObj.screen.blit(button_images[0],(715,295))#look
        gcObj.screen.blit(button_images[2],(715,415))#atk
        gcObj.screen.blit(button_images[1],(835,295))#inv
        gcObj.screen.blit(button_images[3],(835,415))#char
    else:
        gcObj.screen.blit(button_images[5].subsurface(32,0,32,32),(685,270))
        gcObj.screen.blit(button_images[4],(690,315))#movement panel
##### HUDV FUNCTIONS END

def drawTile(tile,pos,side,surf,mini):
    if mini:
        if tile == 1: c=(25,25,25)
        if tile == 0: c=(150,150,150)
        if tile == 4: c=(250,25,25)


    if tile == 1: tile = floor
    if tile == 0: tile = wall
    if tile == 4: tile = enemy1
    if tile == 3: tile = chest
    if tile == 98: tile = floor_up
    if tile == 99: tile = floor_down

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

def drawHud(gcObj):
    #controls

    mmb=pygame.Surface((4,4))
    mmb.fill((255,0,0))

    #minimap
    drawMiniMap(gcObj)
    #draw log
    drawLog(gcObj)
    #draw buttons
    drawButtons(gcObj)
    #draw borders
    gcObj.screen.blit(bordersImage,(0,0))
