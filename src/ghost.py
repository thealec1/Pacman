import pygame as pg
import os
from pacman import Pacman
from utils import Utils
from constants import *
import random

class Ghost:
    
    ghosts = []

    DIRECTIONS = [0, 1, -1]
    SIZE = 30
    
    def __init__(self, pacman : Pacman, x, y):
        self.spawn_x, self.spawn_y = x, y
        self.x, self.y = x, y
        self.name = "Ghost"
        self.pacman = pacman
        self.world = pacman.world
        self.colour = (0, 0, 150)
        self.world_mode = "scatter"
        self.lifetime = 0
        self.sprite_index = 0
        self.x_vel = -1
        self.y_vel = 0
        self.speed = 2
        self.eye_direction = 0
        self.eatable = False
        self.selected_node = None
        self.target_node = None
        self.current_path = []
        self.path_index = 1
        self.respawning = False
        self.active = True
        Ghost.ghosts.append(self)
        
        ts = self.pacman.world.tile_size
        self.h = 3*ts
        self.w = (256/300)*self.h
        EYE_WIDTH = self.w/4
        
        Ghost.DIMENSIONS = (self.w, self.h)
        
        Ghost.EYE_SIZE = (EYE_WIDTH, (128*EYE_WIDTH)/65)
        Ghost.GHOST_SPRITES = [Utils.load_res(os.path.join("ghosts", "ghost1.png"), Ghost.DIMENSIONS), Utils.load_res(os.path.join("ghosts", "ghost2.png"), Ghost.DIMENSIONS),
                                Utils.load_res(os.path.join("ghosts", "ghost3.png"), Ghost.DIMENSIONS), Utils.load_res(os.path.join("ghosts", "ghost4.png"), Ghost.DIMENSIONS),
                                Utils.load_res(os.path.join("ghosts", "ghost5.png"), Ghost.DIMENSIONS), Utils.load_res(os.path.join("ghosts", "ghost6.png"), Ghost.DIMENSIONS), 
                                Utils.load_res(os.path.join("ghosts", "ghost7.png"), Ghost.DIMENSIONS), Utils.load_res(os.path.join("ghosts", "ghost8.png"), Ghost.DIMENSIONS)]
        Ghost.EYE_SPRITES = [Utils.load_res(os.path.join("ghosts", "eyes1.png"), Ghost.EYE_SIZE), Utils.load_res(os.path.join("ghosts", "eyes2.png"), Ghost.EYE_SIZE),
                             Utils.load_res(os.path.join("ghosts", "eyes3.png"), Ghost.EYE_SIZE), Utils.load_res(os.path.join("ghosts", "eyes4.png"), Ghost.EYE_SIZE)]
    
    def node_selection(self):
        if self.respawning:
            self.target_node = self.world.get_node_from_pos((self.spawn_x, self.spawn_y))
        elif self.eatable:
            furthest_node = [None, 0]
            for node in self.world.valid_tiles:
                px, py = self.world.grid_coords_from_pos((self.pacman.x, self.pacman.y))
                distance = Utils.get_distance(px, py, node.gx, node.gy)
                if furthest_node[1] < distance:
                    furthest_node = [node, distance]
            furthest_node[0].set_colour(self.colour)
            self.target_node = furthest_node[0]
        elif self.world_mode == "scatter":
            self.target_node = random.choice(self.world.valid_tiles)
        elif self.world_mode == "chase":
            self.target_node = self.world.get_node_from_pos((self.pacman.x, self.pacman.y))

    def reset(self):
        self.x, self.y = self.spawn_x, self.spawn_y
        self.eatable = False
        self.selected_node = None

    def do_pathfinding(self):
        if self.selected_node == None:
            tile_coords = self.world.grid_coords_from_pos((self.x, self.y))
            start_node = self.world.tiles[tile_coords[1]][tile_coords[0]]
            self.node_selection()

            if self.target_node == None:
                return
            self.current_path = self.world.search_for_shortest_path(self.world.tiles, start_node, self.target_node)
            if self.current_path == None or len(self.current_path) <= 0:
                return
            
            for node in self.world.valid_tiles:
                node.set_colour((255, 255, 255))
            for node in self.current_path:
                node.set_colour((self.colour))
            
            self.path_index = len(self.current_path)-1
            self.selected_node = self.current_path[self.path_index]
        else:
            
            if self.path_index == 0:
                if self.respawning:
                    self.toggle_respawn()
                self.selected_node = None
                return
            
            tile_coords = self.world.grid_coords_from_pos((self.x, self.y))
            current_tile = self.world.tiles[tile_coords[1]][tile_coords[0]]
            
            condition_x = (self.selected_node.mx<=self.x+(self.speed//2) and self.selected_node.mx>=self.x-(self.speed//2))
            condition_y = (self.selected_node.my<=self.y+(self.speed//2) and self.selected_node.my>=self.y-(self.speed//2))
            if current_tile == self.selected_node and (condition_x and condition_y):
                self.path_index -= 1
                self.selected_node = self.current_path[self.path_index]
            else:
                if not condition_x:
                    if self.selected_node.mx < self.x:
                        self.x -= self.speed
                        self.x_vel = -1
                        self.y_vel = 0
                    elif self.selected_node.mx > self.x:
                        self.x += self.speed
                        self.x_vel = 1
                        self.y_vel = 0
                if not condition_y:
                    if self.selected_node.my < self.y:
                        self.y -= self.speed
                        self.y_vel = -1
                        self.x_vel = 0
                    elif self.selected_node.my > self.y:
                        self.y += self.speed
                        self.y_vel = 1
                        self.x_vel = 0

    def update(self, mode : str):

        self.active = self.pacman.game_over_timer <= 0 and self.pacman.game_win_timer <= 0

        if self.active:
            self.do_pathfinding()

        self.world_mode = mode
        
        if self.x_vel == 1:
            self.eye_direction = 2
        elif self.x_vel == -1:
            self.eye_direction = 3
        elif self.y_vel == 1:
            self.eye_direction = 1
        elif self.y_vel == -1:
            self.eye_direction = 0
        
        self.do_collision()
    
    def toggle_respawn(self):
        if self.respawning:
            self.eatable = False
            self.speed -= 8
        else:
            self.speed += 8
            pass
        self.respawning = not self.respawning

    def do_collision(self):
        if Utils.get_distance(self.x+Ghost.SIZE/2, self.y+Ghost.SIZE/2, self.pacman.x, self.pacman.y) < (self.pacman.SIZE/2) + (Ghost.SIZE/2):
            if self.pacman.eat_mode and self.eatable:
                if not self.respawning:
                    self.pacman.ate_ghost(self)
                    self.toggle_respawn()
                    self.selected_node = None
            else:
                self.pacman.take_life()

    def animate_ectoplasm(self):
        if self.lifetime % 5 == 0:
            self.current_sprite = Ghost.GHOST_SPRITES[self.sprite_index]

            if self.sprite_index >= len(Ghost.GHOST_SPRITES)-1:
                self.sprite_index = 0
            else:
                self.sprite_index += 1

    def set_flee_colour(self):
        timer = pg.time.get_ticks() - self.pacman.eat_time
        if timer >= Pacman.EAT_LENGTH * (7/10):
            if (timer // 300) % 2 == 0:
                colour = GHOST_RUN_COLOUR
            else:
                colour = (255, 255, 255)
        else:
            colour = GHOST_RUN_COLOUR
        return colour

    def flood_colour(self, colour):
        colour_image = pg.Surface(self.current_sprite.get_size()).convert_alpha()
        colour_image.fill(colour)
        self.final_surf = self.current_sprite.copy()
        self.final_surf.blit(colour_image, (0, 0), special_flags=pg.BLEND_MULT)

    def render_full_body(self, screen : pg.Surface):
        if not self.respawning:
            screen.blit(self.final_surf, (self.x-(self.w//2), self.y-(self.h//2))) # BODY
        
        screen.blit(Ghost.EYE_SPRITES[self.eye_direction], (self.x-12, self.y-12)) # LEFT EYE
        screen.blit(Ghost.EYE_SPRITES[self.eye_direction], (self.x+2, self.y-12)) # RIGHT EYE

    def render(self, screen : pg.Surface):

        if self.pacman.eat_mode and self.eatable:
            colour = self.set_flee_colour()
        else:
            self.eatable = False
            colour = self.colour
        
        self.animate_ectoplasm()
        self.flood_colour(colour)
        self.render_full_body(screen)

        self.lifetime += 1

class Blinky(Ghost):
    def __init__(self, pacman : Pacman, x, y):
        super().__init__(pacman, x, y)
        self.name = "Blinky"
        self.colour = (237, 34, 12)
    
    def update(self, mode : str):
        super().update(mode)

class Pinky(Ghost):
    def __init__(self, pacman : Pacman, x, y):
        super().__init__(pacman, x, y)
        self.name = "Pinky"
        self.colour = (255, 138, 220)

class Inky(Ghost):
    def __init__(self, pacman : Pacman, x, y):
        super().__init__(pacman, x, y)
        self.name = "Inky"
        self.colour = (75, 142, 250)

class Clyde(Ghost):
    def __init__(self, pacman : Pacman, x, y):
        super().__init__(pacman, x, y)
        self.name = "Clyde"
        self.colour = (255, 128, 0)
