import pygame
from pygame.locals import *
import mainmenu
import game_control as dgc

class Game:
    def __init__(self,surf,screen):
        self.surf=surf;self.screen=screen

        self.mm=mainmenu.Menu(self.screen)
        self.mm.game=self

        self.st=mainmenu.ScrollingText(self.screen,"menu")
        self.st.game=self

        self.gc=dgc.gameControl(self.surf,self.screen)
        self.gc.newMap()

        self.logos=mainmenu.Logos(self.screen)
        self.logos.game=self

        self.state = "game"

    def update(self,dt):
        if self.state == "game":
            self.gc.update()
        else:
            self.events=pygame.event.get()
        if self.state == "scrolling":
            self.st.Draw(dt)

        if self.state == "logos":
            self.logos.Draw(dt)
        if self.state == "menu":
            self.mm.Draw()

        pygame.display.flip()
