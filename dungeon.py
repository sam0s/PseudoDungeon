import pygame
from pygame import surface
from pygame.locals import *


screen=pygame.display.set_mode((960, 720),HWSURFACE | DOUBLEBUF)
import game

disp=surface.Surface((960,720))

GAME = game.Game(disp,screen)
GAME.clock=pygame.time.Clock()
GAME.go=True
def main():
    while GAME.go:
        GAME.update(dt=float(GAME.clock.tick(30)*1e-3))

if __name__ == "__main__":
    main()
