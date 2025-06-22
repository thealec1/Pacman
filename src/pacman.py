import pygame as pg
from math import sin, pi
from constants import *
from barrier import Barrier
from utils import Utils
import time

class Pacman:
    
    ANIM_FREQUENCY = FPS * 0.3 # ticks
    DIE_ANIM_LENGTH = FPS * 3 # ticks
    WIN_ANIM_LENGTH = FPS * 5 # ticks
    LOSE_ANIM_LENGTH = FPS * 5 # ticks
    
    EAT_LENGTH = 10 * 1000 # ms

    def __init__(self, world):
        self.highscore = self.get_highscore()
        self.speed = (world.tile_size*3)/15
        self.SIZE = world.tile_size*3*(4/5)
        self.eat_mode = False
        self.die_time = 0
        self.walk_ticks = 0
        self.game_over_timer = 0
        self.game_win_timer = 0
        self.is_colliding = False
        self.collision = False
        self.world = world
        # 0: right, 1: down, 2: left, 3: up
        self.orientation = 0
        self.vicinity_rect = pg.Rect(0, 0, 0, 0)
        self.collision_rect = pg.Rect(0, 0, 0, 0)
        self.is_moving = True
        self.is_eating = True
        self.is_rendering = True
        self.ate_ghost_timer = 0
        self.ghost_eaten = None
        self.digested_ghosts = 0

        self.ang = 0
        self.rot = 0

        self.new_game()
    
    def new_game(self):
        self.eat_time = 0
        self.lives = 3
        self.consumed_pellets = 0
        self.score = 0
        self.world.regenerate_pellets()

    def reset(self):
        self.x, self.y = self.spawn_x, self.spawn_y
        self.x_direction = self.y_direction = 0
        self.dx_direction = self.dy_direction = 0
        self.orientation = 0

    def set_location(self, position : list):
        self.spawn_x = position[0]
        self.spawn_y = position[1]
        self.reset()
    
    def add_score(self, value):
        self.score += value

        if self.score > self.highscore:
            self.highscore = self.score
    
    def get_highscore(self):
        f = open(DATA_FILE_PATH)
        return int(f.read())

    def handle_events(self, event : pg.event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.dx_direction = 0
                self.dy_direction = -1
            if event.key == pg.K_s:
                self.dx_direction = 0
                self.dy_direction = 1
            if event.key == pg.K_a:
                self.dx_direction = -1
                self.dy_direction = 0
            if event.key == pg.K_d:
                self.dx_direction = 1
                self.dy_direction = 0

    def at_barrier(self, x : int, y: int) -> bool:
        ts = self.world.tile_size*3
        self.collision_rect = pg.Rect(x-ts/2, y-ts/2, ts, ts)
        rect = self.collision_rect
        for barrier in Barrier.barriers:
            if barrier.rect.colliderect(rect):
                self.collision = True
                return True
        self.collision = False
        return False

    def update(self):

        if not self.collision:
            self.walk_ticks += 1

        #### The following is commented out movement code
        #### TODO come back to this eventually and delete / clean it up
        # pg.display.set_caption(f"{self.world.get_tile(self.dx_direction*self.world.tile_size + self.x, self.y)}, {self.world.get_tile(self.x, 2*self.dy_direction*self.world.tile_size + self.y)}")
        # if self.dx_direction != self.x_direction and self.world.get_tile(self.dx_direction*self.world.tile_size + self.x, self.y) != "*":
        #     self.x_direction = self.dx_direction
        
        # if self.dy_direction != self.y_direction and self.world.get_tile(self.x, 2*self.dy_direction*self.world.tile_size + self.y) != "*":
        #     self.y_direction = self.dy_direction

        ts = self.world.tile_size

        if self.world.get_tile_coords(self.x-ts*2, self.y) == (41, 24):
            self.x, self.y = self.world.get_pixels_from_tile(0, 24)
        if self.world.get_tile_coords(self.x+ts*2, self.y) == (0, 24):
            self.x, self.y = self.world.get_pixels_from_tile(41, 24)

        if self.is_moving:
            self.move()

    def move(self):

        length = self.world.tile_size*3
        width = (length - self.SIZE)/2

        if self.dx_direction != 0:
            self.vicinity_rect = pg.Rect((self.x - width/2)+(length/2)*self.dx_direction, self.y - length/2, width, length)
            collision = False
            for barrier in Barrier.barriers:
                if self.vicinity_rect.colliderect(barrier.rect):
                    collision = True
                    break
            if not collision:
                self.x_direction = self.dx_direction
                self.y_direction = 0
        elif self.dy_direction != 0:
            self.vicinity_rect = pg.Rect(self.x - length/2, (self.y-width/2)+(length/2)*self.dy_direction, length, width)
            collision = False
            for barrier in Barrier.barriers:
                if self.vicinity_rect.colliderect(barrier.rect):
                    collision = True
                    break
            if not collision:
                self.y_direction = self.dy_direction
                self.x_direction = 0

        if self.y_direction == -1 and not self.at_barrier(self.x, self.y - self.speed):
            self.y -= self.speed
            self.orientation = 3
        elif self.y_direction == 1 and not self.at_barrier(self.x, self.y + self.speed):
           self.y += self.speed
           self.orientation = 1
        elif self.x_direction == 1 and not self.at_barrier(self.x + self.speed, self.y):
            self.x += self.speed
            self.orientation = 0
        elif self.x_direction == -1 and not self.at_barrier(self.x - self.speed, self.y):
            self.x -= self.speed
            self.orientation = 2

        if self.eat_time > 0:
            if pg.time.get_ticks() - self.eat_time >= Pacman.EAT_LENGTH:
                self.eat_mode = False
                self.eat_time = 0
                self.digested_ghosts = 0
            else:
                self.eat_mode = True
    
    def init_eat_mode(self):
        self.eat_time = pg.time.get_ticks()
        self.digested_ghosts = 0
        self.world.make_ghosts_eatable()

    def take_life(self):
        if self.die_time <= 0:
            self.is_eating = False
            self.is_moving = False
            self.ang = pi/4
            self.die_time = Pacman.DIE_ANIM_LENGTH

    def game_won(self):
        self.game_win_timer = Pacman.WIN_ANIM_LENGTH
        self.is_moving = False
        self.is_eating = False

    def game_won_animation(self):
        
        self.game_win_timer -= 1

        if self.ang != 0:
            self.ang = max(0, self.ang-pi/100)

        if (self.game_win_timer // 30) % 2 == 0:
            Barrier.colour = Barrier.SAVED_COLOUR
        else:
            Barrier.colour = (255, 255, 255)
        
        if self.game_win_timer == 0:
            self.world.reset_ghosts()
            self.eat_mode = False
            self.is_moving = True
            self.is_eating = True
            self.lives = 3
            self.consumed_pellets = 0
            self.world.regenerate_pellets()
            self.reset()

    def game_over(self):
        self.game_over_timer = Pacman.LOSE_ANIM_LENGTH
        self.is_moving = False
        self.is_rendering = False
    
    def game_over_animation(self, screen : pg.Surface):
        self.game_over_timer -= 1

        game_over_text = MASSIVE_FONT.render("Game Over", True, (200, 0, 0), BACKGROUND_COLOUR)
        w = game_over_text.get_rect().width
        h = game_over_text.get_rect().height
        
        x = (pg.display.get_window_size()[0] - w)/2
        y = (pg.display.get_window_size()[1] - h)/2

        if (self.game_over_timer // 30) % 2 == 0:
            screen.blit(game_over_text, (x, y))

        if self.game_over_timer == 0:
            self.world.reset_ghosts()
            self.is_rendering = True
            self.is_moving = True
            self.reset()
            self.new_game()

    def lose_life_animation(self):
        self.die_time -= 1
        if self.rot != 3*pi/2:
            self.rot += (self.get_circle_direction(3*pi/2, self.rot) * (pi/20))
            self.rot %= 2*pi
            
        if self.die_time <= 120:
            self.ang += pi/100
            
        if self.die_time == 0:
            self.world.reset_ghosts()
            self.lives -= 1
            self.is_eating = True
            self.is_moving = True
            self.is_rendering = True
            if self.lives == 0:
                self.game_over()
            self.reset()
    
    def ate_ghost(self, ghost):
        
        self.digested_ghosts += 1
        self.add_score(self.calc_ghost_score(self.digested_ghosts))

        self.ate_ghost_timer = 2
        self.ghost_eaten = ghost
        self.world.render_ghosts = False
        self.is_rendering = False
        self.is_eating = False
    
    def calc_ghost_score(self, x : int) -> int:
        return (2 ** (x-1)) * EAT_GHOST_SCORE
    
    def ate_ghost_animation(self , screen : pg.Surface):
        self.ate_ghost_timer -= 1
        freeze_text = NORMAL_FONT.render(str(self.calc_ghost_score(self.digested_ghosts)), True, GHOST_SCORE_COLOUR)
        w = freeze_text.get_width()
        h = freeze_text.get_height()
        screen.blit(freeze_text, (self.ghost_eaten.x-(w//2), self.ghost_eaten.y-(h//2)))
        
        if self.ate_ghost_timer == 0:
            time.sleep(2)
            self.world.render_ghosts = True
            self.is_rendering = True
            self.is_eating = True
    
    def do_animations(self, screen : pg.Surface):
        if self.game_over_timer > 0:
            self.game_over_animation(screen)
        
        if self.die_time > 0:
            self.lose_life_animation()

        if self.game_win_timer > 0:
            self.game_won_animation()
        
        if self.ate_ghost_timer > 0:
            self.ate_ghost_animation(screen)
    
    def get_circle_direction(self, target_angle, current_angle) -> int:
        ccw_distance = (target_angle-current_angle) % (2*pi)
        cw_distance = (current_angle-target_angle) % (2*pi)

        if ccw_distance > cw_distance:
            return -1
        elif cw_distance > ccw_distance:
            return 1
        else:
            return 1
    
    def render_pacman(self, screen : pg.Surface):
        t = self.walk_ticks
        
        freq = Pacman.ANIM_FREQUENCY

        radius = self.SIZE/2
        
        x = self.x
        y = self.y
        max_angle = pi/4

        ang = self.ang
        rot = self.rot

        if self.is_eating:
            self.rot = self.orientation * (pi/2)
            a_c = max_angle * 1/2
            self.ang = a_c * sin ( ((2*pi)/freq) * t ) + a_c

        if self.is_rendering:
            Utils.draw_pie(screen, PACMAN_COLOUR, (x, y), radius, ang-rot, ((2*pi)-ang)-rot, special_colour=COLOUR_PACMAN)

    def render(self, screen : pg.Surface):
        self.do_animations(screen)
        self.render_pacman(screen)
