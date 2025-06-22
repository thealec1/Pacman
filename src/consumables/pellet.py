import pygame as pg
from consumables.consumable import Consumable
from math import sin, pi
from utils import Utils
from constants import FPS

class Pellet(Consumable):

    COLOUR = (255, 255, 255)

    pellet_count = 0
    FLASH_FREQUENCY = 1000 * 1/5 # ms

    def __init__(self, x, y, gx, gy, row, pacman, tile_size, world):
        super().__init__(x, y, gx, gy, row, pacman, world)
        self.SIZE = (tile_size*3)/15
        
        self.id = Pellet.pellet_count
        Pellet.pellet_count += 1
        self.freq = Utils.COLOUR_WAVE_FREQ

    def on_consumed(self):
        
        self.pacman.consumed_pellets += 1

        self.pacman.add_score(10)

        if self.pacman.consumed_pellets == 70:
            self.world.cherry.spawn()
        
        if self.pacman.consumed_pellets == 170:
            self.world.cherry.spawn()

        if self.pacman.consumed_pellets == Pellet.pellet_count:
            self.pacman.game_won()

        super().on_consumed()

    def render(self, screen):
        super().render(screen)

        colour = Pellet.COLOUR

        t = pg.time.get_ticks()
        r = Utils.colour_wave(self.freq, t, self.freq*self.id+10)
        g = Utils.colour_wave(self.freq, t, self.freq*self.id)
        b = Utils.colour_wave(self.freq, t, self.freq*self.id+20)

        colour = (r, g, b)

        if isinstance(self, LargePellet):
            ticks = pg.time.get_ticks()
            if (ticks//(Pellet.FLASH_FREQUENCY)) % 2 == 0:
                self.do_circle(screen, colour)
        else:
            self.do_circle(screen, colour)

        # gfxdraw.aacircle(screen, self.x, self.y, self.SIZE, Pellet.COLOUR)
        # gfxdraw.filled_circle(screen, self.x, self.y, self.SIZE, Pellet.COLOUR)

    def do_circle(self, screen, colour):
        pg.draw.circle(screen, colour, (self.x, self.y), self.SIZE)

class LargePellet(Pellet):

    COLOUR = (255, 255, 255)

    def __init__(self, x, y, gx, gy, row, pacman, tile_size, world):
        super().__init__(x, y, gx, gy, row, pacman, tile_size, world)
        self.SIZE = (tile_size*3)//6

    def on_consumed(self):
        self.pacman.init_eat_mode()

        super().on_consumed()

    # def render(self, screen):
        # gfxdraw.aacircle(screen, self.x, self.y, LargePellet.SIZE, Pellet.COLOUR)
        # gfxdraw.filled_circle (screen, self.x, self.y, LargePellet.SIZE, Pellet.COLOUR)
        # pg.draw.circle(screen, Pellet.COLOUR, (self.x, self.y), LargePellet.SIZE)
