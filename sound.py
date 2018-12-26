#!/usr/bin/env python

"""
sound.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []



import pygame
from random import choice
from pygame import *
from os import path

pygame.mixer.init()

class Mix(object):
    def __init__(self):
        self.music={"track1":pygame.mixer.Sound(path.join("sound","msc","dw- - cloudkicker.wav"))}

        self.sounds=sounds = {"flip":pygame.mixer.Sound(path.join("sound","fx","switch_toggle.wav")),
                                "popup":pygame.mixer.Sound(path.join("sound","fx","popup.wav")),
                                "swing":pygame.mixer.Sound(path.join("sound","fx","wpn","sword_swing.wav")),
                                "hit1":pygame.mixer.Sound(path.join("sound","fx","wpn","sword_hit1.wav")),
                                "player_hit":pygame.mixer.Sound(path.join("sound","fx","wpn","player_hit.wav")),
                            }
        self.musicChannel=pygame.mixer.Channel(5)
        self.sfxChannel=pygame.mixer.Channel(0)
    def sndPlay(self,sndname):
        pygame.mixer.find_channel(True).play(self.sounds[sndname])
    def mscPlay(self,sndname):
        self.musicChannel.play(sndname)
