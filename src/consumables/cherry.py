import pygame as pg
import os
from consumables.consumable import Consumable
from utils import Utils
from constants import FPS

class Cherry(Consumable):

    SCORE = 100
    
    LIFE_LENGTH = FPS * 8

    def __init__(self, x, y, gx, gy, row, pacman, world):
        super().__init__(x, y, gx, gy, row, pacman, world)
        Cherry.SPRITE = Utils.load_res("cherry.png")
        self.active = False
        self.lifetime = 0
        self.pacman = pacman
        self.SIZE = world.tile_size*2
        self.SCALED_SPRITE = pg.transform.scale(Cherry.SPRITE, (self.SIZE, self.SIZE))
    
    def spawn(self):
        self.lifetime = 0
        self.active = True

    def update(self):
        if self.active:
            self.lifetime += 1

        if self.lifetime == Cherry.LIFE_LENGTH:
            self.active = False
        
        return super().update()

    def render(self, screen : pg.Surface):
        super().render(screen)
        screen.blit(self.SCALED_SPRITE, (self.x-(self.SIZE/2), self.y-(self.SIZE/2)) )

    def on_consumed(self):
        self.pacman.add_score(Cherry.SCORE)
        self.world.init_sticky_text_render(str(Cherry.SCORE), self.x, self.y)
        return super().on_consumed()
