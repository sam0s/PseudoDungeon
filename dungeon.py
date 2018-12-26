import pygame
from pygame import surface

screen=pygame.display.set_mode((960,720))
import game_control as dc
import dungeon_player as dp

disp=surface.Surface((960,720))

gc=dc.gameControl(disp,screen)
gc.newMap()
gc.clock=pygame.time.Clock()

def main():
    while gc.go:
        gc.clock.tick()
        gc.update()

if __name__ == "__main__":
    main()
