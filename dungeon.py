import pygame
import random,math,mazeGen
from pygame import surface

screen=pygame.display.set_mode((960,720))

#load images and function library
import dungeon_lib as dl
import dungeon_player as dp

disp=surface.Surface((960,720))
clock=pygame.time.Clock()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

gc=dl.gameControl(disp,screen)
gc.newMap()

def main():
    while gc.go:
        clock.tick(60)
        pygame.display.set_caption(str(clock.get_fps()))
        gc.events=pygame.event.get()
        gc.update()

if __name__ == "__main__":
    main()
