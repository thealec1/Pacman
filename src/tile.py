import pygame as pg

class Tile:

    def __init__(self, x, y, mx, my, gx, gy, world, row, centered=False, send_to_back=False):
        self.x = x
        self.y = y
        self.mx = mx
        self.my = my
        self.gx = gx
        self.gy = gy
        self.world = world
        self.centered = centered
        self.active = True
        self.lifetime = 0
        self.row = row
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = self.g_cost + self.h_cost
        self.colour = (50, 50, 50)
        self.size = 1

        if send_to_back:
            row.insert(0, self)
        else:
            row.append(self)

    def get_pos(self):
        return self.gx, self.gy

    def update_neighbours(self, grid, column_size, row_size):
        self.neighbours = []
        if self.gy < column_size - 1 and grid[self.gy+1][self.gx] in self.world.valid_tiles: # DOWN
            self.neighbours.append(grid[self.gy+1][self.gx])
        if self.gy > 0 and grid[self.gy-1][self.gx] in self.world.valid_tiles: # UP
            self.neighbours.append(grid[self.gy-1][self.gx])
        if self.gx < row_size - 1 and grid[self.gy][self.gx+1] in self.world.valid_tiles: # RIGHT
            self.neighbours.append(grid[self.gy][self.gx+1])
        if self.gx > 0 and grid[self.gy][self.gx-1] in self.world.valid_tiles: # LEFT
            self.neighbours.append(grid[self.gy][self.gx-1])

    def update(self):
        pass

    def render(self, screen : pg.Surface):
        pass

    def set_colour(self, colour):
        self.colour = colour

    def debug_render(self, screen : pg.Surface):
        pg.draw.rect(screen, self.colour, pg.Rect(self.mx, self.my, self.world.tile_size*.9, self.world.tile_size*.9))

"""

[[tile(0,0), tile(0,1), ... tile(0,n)], [tile(1,0), tile(1,1), ... tile(1,n)] ... [tile(j,0), tile(j,1), ... tile(j,n)]]

"""
