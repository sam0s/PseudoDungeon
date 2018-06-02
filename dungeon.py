import pygame

from pygame.locals import *
import random,math,mazeGen

screen=pygame.display.set_mode((960,720))

#load images and function library
import dungeon_lib as dl
import dungeon_player as dp

disp=pygame.Surface((960,720))
clock=pygame.time.Clock()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

lev_1,xy,end=mazeGen.generate(25)

p=dp.Player(*xy)
c=dl.gameControl(disp)
c.currentLevel=lev_1
c.p=p
p.gc=c
c.screen=screen

def main():
    while c.go:
        clock.tick(999)
        pygame.display.set_caption(str(clock.get_fps()))
        c.events=pygame.event.get()
        p.update()
        c.update()

if __name__ == "__main__":
    main()
