#!/usr/bin/env python

"""
items.py

"""
__author__ = "djkool"
__copyright__ = "None"
__credits__ = []

import pygame
from os import path
from random import choice
import json
from copy import copy

itemsheet = pygame.image.load(path.join("images","itemF.png")).convert()
itemsheetWeapon = pygame.image.load(path.join("images","itemW.png")).convert()
itemsheetQuest = pygame.image.load(path.join("images","itemQ.png")).convert()

_ItemsById = {}
_ItemsByName = {}

def loadItems(filename):
    global _ItemsById, _ItemsByName
    with open(path.join(filename)) as f:
        jsondata = json.load(f)

        for itemclass in jsondata:
            itemdata = jsondata[itemclass]

            ##print "Itemclass Lookup: %s" % (itemclass)
            # Attempt to find item class in globals
            try:
                iclass = globals()[itemclass]
                ##print iclass
            except KeyError as e:
                ##print e
                continue

            # Contruct item templates from data
            ##print "Loading %d items of type %s" % (len(itemdata), str(iclass))
            for itemid in itemdata:
                item = iclass(itemid, **itemdata[itemid])
                _ItemsById[item.id] = item
                _ItemsByName[item.name] = item

        ##print _ItemsById

def getItem(name):
    global _ItemsByName
    ##print "Creating %s" % (name)
    return copy(_ItemsByName[name])

def fromId(idn,parent=None,justname=False):
    global _ItemsById
    if isinstance(idn, int):
        idn = str(idn)
    ##print "items.fromId(%s)" % (idn)

    # New ItemDB lookup
    item = _ItemsById[idn]
    return item.name if justname else copy(item)

class Item:
    def __init__(self, id_, name, descr, idx, value = 0):
        self.id = id_
        self.name = name
        self.descr = descr
        self.idx = idx
        self.val = value
        self.stack=1

############ WEAPONS #######################
##########################

class Weapon(Item):
    def __init__(self, id_, max, min, **item_info):
        Item.__init__(self, id_, **item_info)
        self.max = max
        self.min = min
        self.image = itemsheetWeapon.subsurface(pygame.Rect(self.idx*32, 0, 32, 32))


## EAT ##
#########

class Food(Item):
    def __init__(self, id_, consumeVal, **item_info):
        Item.__init__(self, id_, **item_info)
        self.consumeVal = consumeVal
        self.image = itemsheet.subsurface(pygame.Rect(self.idx*26, 0, 26, 26))
