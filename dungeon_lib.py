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
floor_up=pygame.image.load(path.join("images","enviro","door.png")).convert()

#hud iamges
bordersImage=pygame.image.load(path.join("images","hud","borders.png")).convert()
bordersCombat=pygame.image.load(path.join("images","hud","combat_borders.png")).convert()
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
bordersCombat.set_colorkey((255,0,255))
cursor.set_colorkey((255,0,255))
wall.set_colorkey((255,0,255))
floor_down.set_colorkey((255,0,255))
floor_up.set_colorkey((255,0,255))
enemy1.set_colorkey((255,0,255))
chest.set_colorkey((255,0,255))

northCone=[[-1,0],[1,0],[0,-1],[-1,-1],[-2,-1],[1,-1],[2,-1],[0,-2],[-1,-2],[-2,-2],[1,-2],[2,-2]
]
eastCone=[[0,-1],[0,1],[1,0],[1,-1],[1,-2],[1,1],[1,2],[2,0],[2,-1],[2,-2],[2,1],[2,2]
]
southCone=[[-1,0],[1,0],[0,1],[-1,1],[-2,1],[1,1],[2,1],[-2,2],[-1,2],[0,2],[1,2],[2,2]
]
westCone=[[0,-1],[0,1],[-1,0],[-1,1],[-1,2],[-1,-1],[-1,-2],[-2,0],[-2,1],[-2,2],[-2,-1],[-2,-2]
]

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

def drawLog(gcObj):
    pygame.draw.rect(gcObj.screen,(255,255,255),(0,516,672,204),0)
    bottom=708
    #2 line messages currently supported
    for msg in reversed(gcObj.log):
        msg1=msg
        msg2=[]
        if len(msg)>69:
            msg1=msg[:69]
            msg2=[msg[69:]]
        a=1
        for mesg in reversed([msg1]+msg2):
            if a==len([msg1]+msg2):
                msgImg=FONT.render("> "+str(mesg),1,(255,0,0),(255,255,255))
            else:
                msgImg=FONT.render("  "+str(mesg),1,(255,0,0),(255,255,255))
            a+=1
            space=msgImg.get_height()+2
            y=bottom-space
            gcObj.screen.blit(msgImg,(9,y))
            bottom-=space

def drawButtons(gcObj):
    #draw either controls for movement or actions

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
    if tile == 12:tile=1
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
    pygame.draw.rect(gcObj.screen,(0,0,0),(678,0,282,720),0)
    #minimap
    drawMiniMap(gcObj)
    #draw log
    drawLog(gcObj)
    #draw buttons
    drawButtons(gcObj)
    #draw borders
    bar(gcObj.screen,((0,200,20),-1),(688,532),(245,32),(gcObj.p.hp,gcObj.p.maxhp))
    gcObj.screen.blit(bordersImage,(0,0))

    #turns
    x=688
    for turn in range(gcObj.p.turns):
        x+=18
        pygame.draw.circle(gcObj.screen, (0,255,0), (x,590),8, 0)

def drawCombat(gcObj):
    #draw all of this during combat
    gcObj.surf.fill((0,0,0))
    drawHud(gcObj)
    drawView((gcObj.p.x,gcObj.p.y),gcObj.currentLevel,gcObj.p.facingDirection,gcObj.surf)
    small=pygame.transform.scale(gcObj.surf, (672,512))
    gcObj.screen.blit(small,(0,0))

    #enemy hp/turns
    pygame.draw.rect(gcObj.screen,(0,0,0),(9,11,330-9,130-11),0)
    bar(gcObj.screen,((0,200,20),-1),(32,32),(245,32),(gcObj.p.target.hp,gcObj.p.target.maxhp))
    x=40
    for turn in range(gcObj.p.target.turns):
        x+=21
        pygame.draw.circle(gcObj.screen, (255,0,0), (x,90),8, 0)

    gcObj.screen.blit(bordersCombat,(0,0))

    pygame.display.flip()

def bar(surface,colors,pos,dimensions,values,altText=""):
    xx=0
    value=values[0];maxvalue=values[1];width=dimensions[0];height=dimensions[1]
    x=pos[0];y=pos[1]
    color1=colors[0];color2=colors[1]
    if color2!=-1:
        pygame.draw.rect(surface, color2, (x,y,width,height), 0)
    for hp in range(int(max(min(value / float(maxvalue) * width, width), 0))):
        pygame.draw.rect(surface, color1, (x+xx,y,1,height), 0)
        xx+= 1

    surface.blit(FONT.render(str(value)+"/"+str(maxvalue),1,(255,255,255),(0,0,0)),(x+8,y+height/2-10))

def damageCalc(t1,t2):
    totalDmg=0
    crit=1
    missed=True
    #crit chance
    if random.randint(0,250) <= t1.stats["crt"]:
        crit=2
    #chance to hit based on ATK skill - Enemy AC
    if random.randint(0,90) <= t1.stats["atk"]:
        #chance to dodge
        if random.randint(0,200) <= t2.stats["agi"]:
            t1.gc.logUpdate(t2.name+" dodged!")
            return 0
        else:
            #dmg = weapon dmg range - enemy def

            totalDmg+=random.randint(t1.activeWeapon[0].min,t1.activeWeapon[0].max)

            totalDmg=totalDmg*crit

            totalDmg-=int(totalDmg*(t2.stats["def"]/100))

            if totalDmg<=1:
                totalDmg=random.choice([0,1,0,1,1,1])

    else:
        t1.gc.logUpdate(t1.name+" misses.")
        return 0
    if crit>1:
        t1.gc.logUpdate(t1.name+" critically strikes for "+str(totalDmg)+".")
        return totalDmg
    else:
        t1.gc.logUpdate(t1.name+" strikes for "+str(totalDmg)+".")
        return totalDmg


class animation(object):
    def __init__(self,anim):
        self.anim=pygame.image.load(path.join("images","enviro","slash.png"))
        self.frames=6
        self.done=False
    def play(self,surf):
        surfCopy=surf.copy()
        frame=0
        while frame<=self.frames:
            surf.blit(surfCopy,(0,0))
            if frame!=self.frames:surf.blit(self.anim.subsurface(247*frame,0,247,205),(200,175))
            frame+=1
            pygame.display.flip()
            pygame.time.delay(25)
        self.done=True
