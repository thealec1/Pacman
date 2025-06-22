import pygame as pg
from utils import Utils
from tile import Tile
from constants import COLOUR_WORLD

class Barrier(Tile):

    barriers = []
    SAVED_COLOUR = (33, 33, 255)
    colour = SAVED_COLOUR

    barrier_count = 0

    def __init__(self, x, y, mx, my, gx, gy, row, width, height, grid_x, grid_y, world, send_to_back=False):
        super().__init__(x, y, mx, my, gx, gy, world, row, send_to_back=send_to_back)

        Barrier.MARGIN = world.BARRIER_THICKNESS
        
        self.x = x
        self.y = y
        self.gx = grid_x
        self.gy = grid_y
        self.width = width
        self.height = height
        self.world = world
        
        self.id = Barrier.barrier_count
        
        Barrier.barrier_count += 1
        Barrier.barriers.append(self) 

        self.i_width = self.width - Barrier.MARGIN
        self.i_height = self.height - Barrier.MARGIN

    def render(self, screen):
        super().render(screen)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        # pg.draw.rect(screen, (0, 0, 150), self.rect)

        # return

        grid = self.world.grid

        above = None
        below = None
        right = None
        left = None
        if self.gy > 0:
            above = grid[self.gy-1][self.gx]
        if self.gy < (len(grid)-1):
            below = grid[self.gy+1][self.gx]
        if self.gx < len(grid[self.gy])-1:
            right = grid[self.gy][self.gx+1]
        if self.gx > 0:
            left = grid[self.gy][self.gx-1]

        freq = Utils.COLOUR_WAVE_FREQ
        t = pg.time.get_ticks()
        r = Utils.colour_wave(freq, t, freq*self.id+10)
        g = Utils.colour_wave(freq, t, freq*self.id)
        b = Utils.colour_wave(freq, t, freq*self.id+20)

        if COLOUR_WORLD:
            Barrier.colour = (r, g, b)

        # Top right corner
        if above != "*" and below == "*" and right != "*" and left == "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x+self.width, self.y), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
        # Top left corner
        elif above != "*" and below == "*" and right == "*" and left != "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x+self.width, self.y), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x, self.y+self.height), Barrier.MARGIN)
        # Bottom right corner
        elif above == "*" and below != "*" and right != "*" and left == "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
        #Bottom left corner
        elif above == "*" and below != "*" and right == "*" and left != "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x, self.y+self.height), Barrier.MARGIN)
        # Top barrier
        elif above != "*" and below == "*" and right == "*" and left == "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x+self.width, self.y), Barrier.MARGIN)
        # Bottom barrier
        elif above == "*" and below != "*" and right == "*" and left == "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
        # Top and bottom barrier
        elif above != "*" and below != "*" and ((right == "*" and left == "*") or
                                                (right == "*" and left == None) or (right == None and left == "*")):
            pg.draw.line(screen, Barrier.colour, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x+self.width, self.y), Barrier.MARGIN)
        # All but right barrier
        elif above != "*" and below != "*" and left != "*" and right == "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x+self.width, self.y), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x, self.y+self.height), Barrier.MARGIN)
        # All but left barrier
        elif above != "*" and below != "*" and left == "*" and right != "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y+self.height), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x+self.width, self.y), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
        # Right and left barrier
        elif above == "*" and below == "*" and right != "*" and left != "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x, self.y+self.height), Barrier.MARGIN)
            pg.draw.line(screen, Barrier.colour, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
        # Right barrier
        elif above == "*" and below == "*" and right != "*" and left == "*":
            pg.draw.line(screen, Barrier.colour, (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), Barrier.MARGIN)
        # Left barrier
        elif above == "*" and below == "*" and right == "*" and left != "*":
            pg.draw.line(screen, Barrier.colour, (self.x, self.y), (self.x, self.y+self.height), Barrier.MARGIN)
        
        # Attempt at shifting rectangles relative to the position of the barrier in the level file

        # intr_w = self.i_width
        # intr_h = self.i_height

        # x_offset = 0
        # y_offset = 0
        # extend_w = 0
        # extend_h = 0

        # # Above
        # if self.gy > 0 and grid[self.gy-1][self.gx] == "*":
        #     extend_h += Barrier.MARGIN
        #     y_offset = -Barrier.MARGIN
        
        # # Below
        # if self.gy < (len(grid)-1) and grid[self.gy+1][self.gx] == "*":
        #     extend_h += Barrier.MARGIN

        # # Right
        # if self.gx < len(grid[self.gy])-1 and grid[self.gy][self.gx+1] == "*":
        #     extend_w += Barrier.MARGIN
        
        # # Left
        # if self.gx > 0 and grid[self.gy][self.gx-1] == "*":
        #     extend_w += Barrier.MARGIN
        #     x_offset = -Barrier.MARGIN

        # Has diagonal(s)?
        # diagonals = False
        # if self.gy > 0:
        #     if self.gx < len(grid[self.gy])-1 and grid[self.gy-1][self.gx+1] == "*":
        #         diagonals = True
        #     if self.gx > 0 and grid[self.gy-1][self.gx-1] == "*":
        #         diagonals = True
        # if self.gy < (len(grid)-1):
        #     if self.gx < len(grid[self.gy])-1 and grid[self.gy+1][self.gx+1] == "*":
        #         diagonals = True
        #     if self.gx > 0 and grid[self.gy+1][self.gx-1] == "*":
        #         diagonals = True
            
        # if diagonals:
        #     self.interior = pg.Rect(self.x+((self.width-intr_w)/2)+x_offset,
        #                         self.y+((self.height-intr_h)/2)+y_offset, intr_w+extend_w, intr_h+extend_h)
        #     pg.draw.rect(screen, (0, 0, 0), self.interior)
        # else:
        #     self.horizontal_interior = pg.Rect(self.x+((self.width-intr_w)/2)+x_offset,
            #                         self.y+((self.height-intr_h)/2), intr_w+extend_w, intr_h)
            # self.vertical_interior = pg.Rect(self.x+((self.width-intr_w)/2),
            #                         self.y+((self.height-intr_h)/2)+y_offset, intr_w, intr_h+extend_h)
            
            # pg.draw.rect(screen, (0, 0, 0), self.horizontal_interior)
            # pg.draw.rect(screen, (0, 0, 0), self.vertical_interior)

class GhostDoor(Barrier):

    COLOUR = (251, 154, 252)

    def __init__(self, x, y, mx, my, gx, gy, row, grid_x, grid_y, world):
        self.ts = world.tile_size
        super().__init__(x, y, mx, my, gx, gy, row, self.ts, self.ts/3, grid_x, grid_y, world, send_to_back=True)

    def render(self, screen):
        super().render(screen)
        self.rect = pg.Rect(self.x, self.y, self.ts, self.ts)

        self.door = pg.Rect(self.x, self.y+(self.ts-self.height)/2, self.width, self.height)
        pg.draw.rect(screen, GhostDoor.COLOUR, self.door)
