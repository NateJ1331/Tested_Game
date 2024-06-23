import os
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile,join

from pygame.sprite import _Group

pg.init()
pg.display.set_caption("Tested")

BG_COLOR = (0,0,0)
WIDTH,HEIGHT = 1000, 800
FPS = 60

PLAYER_VEL = 5

window = pg.display.set_mode((WIDTH,HEIGHT))

class Player(pg.sprite.Sprite):
    def __init__(self, x,y,width,height):
        self.rect = pg.Rect(x,y,width,height)  
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None  

def main (window):
    clock = pg.time.Clock()

    run = True

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break


if __name__ == "__main__":
    main(window)
