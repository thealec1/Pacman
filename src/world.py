import pygame as pg
from pacman import Pacman
from ghost import Ghost, Blinky, Pinky, Inky, Clyde
from barrier import Barrier, GhostDoor
from tile import Tile
from constants import *
from consumables.pellet import *
from consumables.pellet import Pellet
from consumables.cherry import Cherry
from math import pi
from queue import PriorityQueue

class World:

    STICKY_TEXT_LIFETIME = FPS*3

    def __init__(self, main):

        self.main = main
        window_width = pg.display.get_window_size()[0]
        window_height = pg.display.get_window_size()[1]
        self.update_dimensions(window_width, window_height)
        self.render_ghosts = True
        
        self.sticky_text_timer = 0
        self.sticky_text = None
        self.sticky_text_pos = [0, 0]

        self.cherry = None

        self.grid = []
        self.tiles = []
        self.valid_tiles = []

        # scatter
        # chase
        # run
        self.mode = "scatter"

        self.time = 0

        self.pacman = Pacman(self)

        self.create_level()

        # Ghost.create_ghosts(self.pacman)
    
    def update_dimensions(self, window_width, window_height):
        self.tile_size = 15
        self.BARRIER_THICKNESS = max(1, ((self.tile_size*3)//15)//3)

        self.height = self.tile_size*51
        self.width = self.tile_size*42

        self.x = (window_width - self.width) / 2
        self.y = (window_height - self.height)-1

        self.left_panel = pg.Rect((0, 0, (window_width-self.width)/2, window_height))
        self.right_panel = pg.Rect((self.x+self.width+self.BARRIER_THICKNESS, 0, (window_width-self.width)/2, window_height))
        
    """
    if (self.x-1, self.y) == barrier:
        black on left
    if (self.x+1, self.y) == barrier:
        black on right
    if (self.x, self.y-1) == barrier:
        black on top
    if (self.x, self.y+1) == barrier:
        block on bottom
    """
    def create_level(self):
        f = open(LEVEL_FILE_PATH)
        for row in enumerate(f):
            self.grid.append([])
            self.tiles.append([])
            for tile in enumerate(row[1]):
                
                tile_type = tile[1]
                if tile_type == "\n":
                    continue
                
                fx = tile[0]
                fy = row[0]
                tx = self.x + fx * self.tile_size
                ty = self.y + fy * self.tile_size
                m_tx = tx + self.tile_size/2
                m_ty = ty + self.tile_size/2

                tile_row = self.tiles[fy]

                if tile_type == "*":
                    Barrier(tx, ty, m_tx, m_ty, fx, fy, tile_row, self.tile_size, self.tile_size, fx, fy, self)
                elif tile_type == ".":
                    Pellet(m_tx, m_ty, fx, fy, tile_row, self.pacman, self.tile_size, self)
                elif tile_type == "@":
                    LargePellet(m_tx, m_ty, fx, fy, tile_row, self.pacman, self.tile_size, self)
                elif tile_type == "C":
                    self.cherry = Cherry(m_tx, m_ty, fx, fy, tile_row, self.pacman, self)    
                elif tile_type == "D":
                    GhostDoor(tx, ty, m_tx, m_ty, fx, fy, tile_row, fx, fy, self)
                else:
                    if tile_type == "1":
                        self.pinky = Pinky(self.pacman, m_tx, m_ty)
                    elif tile_type == "2":
                        self.inky = Inky(self.pacman, m_tx, m_ty)
                    elif tile_type == "3":
                        self.clyde = Clyde(self.pacman, m_tx, m_ty)
                    elif tile_type == "4":
                        self.blinky = Blinky(self.pacman, m_tx, m_ty)
                    elif tile_type == "P":
                        self.pacman.set_location([m_tx, m_ty])

                    Tile(tx, ty, m_tx, m_ty, fx, fy, self, self.tiles[fy], False)
                    
                self.grid[fy].append(tile_type)

        self.create_valid_tiles_list()
        column_size = len(self.tiles)
        row_size = len(self.tiles[0])
        for row in self.tiles:
            for tile in row:
                tile.update_neighbours(self.tiles, column_size, row_size)

    def create_valid_tiles_list(self):
        column_size = len(self.tiles)
        row_size = len(self.tiles[0])

        for row in enumerate(self.tiles):
            for tile in enumerate(row[1]):
                gx = tile[0]
                gy = row[0]
                is_valid = True
                if gx < row_size - 1 and self.is_barrier(self.tiles[gy][gx+1]): # RIGHT
                    is_valid = False
                if gx > 0 and self.is_barrier(self.tiles[gy][gx-1]): # LEFT
                    is_valid = False
                if gy > 0 and self.is_barrier(self.tiles[gy-1][gx]): # TOP
                    is_valid = False
                if gy < column_size - 1 and self.is_barrier(self.tiles[gy+1][gx]): # BOTTOM
                    is_valid = False
                if gx < row_size - 1 and gy > 0 and self.is_barrier(self.tiles[gy-1][gx+1]): #TOP RIGHT
                    is_valid = False
                if gy > 0 and gx > 0 and self.is_barrier(self.tiles[gy-1][gx-1]): # TOP LEFT
                    is_valid = False
                if gx > 0 and gy < column_size - 1 and self.is_barrier(self.tiles[gy+1][gx-1]): # BOTTOM LEFT
                    is_valid = False
                if gx < row_size - 1 and gy < column_size - 1 and self.is_barrier(self.tiles[gy+1][gx+1]): # BOTTOM RIGHT
                    is_valid = False
                
                if is_valid:
                    self.valid_tiles.append(tile[1])
                    tile[1].set_colour((255, 255, 255))

        return self.valid_tiles

    def is_barrier(self, tile):
        return isinstance(tile, Barrier)

    def get_tile_coords(self, pixel_x, pixel_y) -> tuple:

        x = round((pixel_x-self.x)/self.tile_size)
        y = round((pixel_y-self.y)/self.tile_size)
        
        for row in enumerate(self.grid):
            for tile in enumerate(row[1]):
                gx = tile[0]
                gy = row[0]
                if gx == x and gy == y:
                    return (gx, gy)
        
        return f"Couldn't find a tile at pixel position x:{pixel_x}, y:{pixel_y}. \n Tile position came out as x:{x}, y:{y}."
    
    def grid_coords_from_pos(self, pos):
        x, y = pos
        x -= self.x
        y -= self.y
        size = self.tile_size
        row = x // size
        col = y // size

        return int(row), int(col)

    def get_node_from_pos(self, pos):
        grid_coords = self.grid_coords_from_pos(pos)
        try:
            retrieved_node = self.tiles[grid_coords[1]][grid_coords[0]]
        except:
            retrieved_node = None
        return retrieved_node

    def get_pixels_from_tile(self, x, y):
        px = x*self.tile_size+self.x+(self.tile_size/2)
        py = y*self.tile_size+self.y+(self.tile_size/2)
        return (px, py)

    def visualize_grid(self, screen : pg.Surface):
        rows = self.height // self.tile_size
        columns = self.width // self.tile_size
        line_colour = (25, 25, 25)
        for row in range(rows+1):
            end_y_coord = self.y+self.tile_size*row
            pg.draw.line(screen, line_colour, (self.x, end_y_coord), (self.x+self.width, end_y_coord))
        for column in range(columns+1):
            end_x_coord = self.x+self.tile_size*column
            pg.draw.line(screen, line_colour, (end_x_coord, self.y), (end_x_coord, self.y+self.height))

    def draw_circular_progress_bar(self, screen : pg.Surface, value : int, max : int):
        rect = pg.Rect(500, 500, 200, 200)
        start_angle = 0
        end_angle = (value/max) * 2*pi
        pg.draw.arc(screen, (255, 0, 0), rect, start_angle, end_angle, width=5)

    def make_ghosts_eatable(self):
        for ghost in Ghost.ghosts:
            ghost.eatable = True

    def reset_ghosts(self):
        for ghost in Ghost.ghosts:
            ghost.reset()

    def update(self):
        
        self.time += 1

        if self.time == 60*20:
            self.mode = "chase"

        for row in self.tiles:
            for tile in row:
                if tile.active:
                    tile.update()

        for ghost in Ghost.ghosts:
            ghost.update(self.mode)

        self.pacman.update()
    
    def regenerate_pellets(self):
        for row in self.tiles:
            for tile in row:
                if isinstance(tile, Pellet):
                    tile.active = True
    
    def init_sticky_text_render(self, text : str, x : int, y : int):
        self.sticky_text_timer = World.STICKY_TEXT_LIFETIME
        self.sticky_text = text
        self.sticky_text_pos[0] = x
        self.sticky_text_pos[1] = y

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1-x2) + abs(y1-y2)

    def search_for_shortest_path(self, grid, start_node, end_node):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start_node))
        shortest_path = {}

        g_score = {node: float("inf") for row in grid for node in row}
        g_score[start_node] = 0

        f_score = {node: float("inf") for row in grid for node in row}
        f_score[start_node] = self.h(start_node.get_pos(), end_node.get_pos())

        open_set_hash = {start_node}

        while not open_set.empty():
                
            current_node = open_set.get()[2]
            open_set_hash.remove(current_node)
            
            if current_node == end_node:
                finished_path = []
                while current_node in shortest_path:
                    current_node = shortest_path[current_node]
                    finished_path.append(current_node)
                return finished_path
            
            for neighbour in current_node.neighbours:
                temp_g_score = g_score[current_node] + 1
                if temp_g_score < g_score[neighbour]:
                    shortest_path[neighbour] = current_node
                    g_score[neighbour] = temp_g_score
                    h_score = self.h(neighbour.get_pos(), end_node.get_pos())
                    f_score[neighbour] = temp_g_score + h_score
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)

        return None

    def render(self, current_FPS):

        screen = self.main.screen

        if self.sticky_text_timer > 0:
            self.sticky_text_timer -= 1
            sticky_text = NORMAL_FONT.render(self.sticky_text, True, STICKY_TEXT_COLOUR)
            x_offset = sticky_text.get_width()//2
            y_offset = sticky_text.get_height()//2
            screen.blit(sticky_text, (self.sticky_text_pos[0]-x_offset, self.sticky_text_pos[1]-y_offset))

        if self.main.debugging:
            pg.display.set_caption(f"Debug Mode... | FPS: {round(current_FPS,1)} | Consumed Pellets: {self.pacman.consumed_pellets} | Direction: {self.pacman.get_circle_direction((3*pi)/2, self.pacman.rot)} | Rotation: {self.pacman.rot}")
            self.visualize_grid(screen)
            pg.draw.rect(screen, (255, 255, 255), self.pacman.vicinity_rect)
        else:
            pg.display.set_caption(WINDOW_TITLE)

        for row in self.tiles:
            for tile in row:
                if tile.active:
                    tile.render(screen)
                if self.main.debugging:
                    tile.debug_render(screen)

        # Render mobs
        for ghost in Ghost.ghosts:
            if self.render_ghosts:
                ghost.render(screen)

        self.pacman.render(screen)

        pg.draw.rect(screen, (BACKGROUND_COLOUR), self.left_panel)
        pg.draw.rect(screen, (BACKGROUND_COLOUR), self.right_panel)
