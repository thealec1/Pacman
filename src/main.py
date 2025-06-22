import pygame as pg
import time
import os
from world import World
from constants import *
from utils import Utils
from math import pi

class Main:

    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode((1024, 800), flags=pg.SCALED, vsync=1)
        pg.display.set_caption(WINDOW_TITLE)
        self.create_and_assign_icon()
        
        self.world = World(self)
        self.current_FPS = 0
        
        self.clock = pg.time.Clock()
        self.debugging = False
        self.running = True
        self.paused = False
        self.loop()
    
    def create_and_assign_icon(self):

        ICON = pg.Surface((ICON_SIZE, ICON_SIZE), flags=pg.SRCALPHA)
        ICON_CENTRE = ICON_SIZE//2

        Utils.draw_pie(ICON, PACMAN_COLOUR, (ICON_CENTRE, ICON_CENTRE), ICON_CENTRE-2, ICON_ANGLE, (2*pi)-(ICON_ANGLE), aa=False, thickness=5)
        
        pg.display.set_icon(pg.transform.smoothscale(ICON, (ICON_SIZE, ICON_SIZE)))
    
    def loop(self):
        while self.running:

            then = time.time()*1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F3:
                        self.debugging = not self.debugging
                    if event.key == pg.K_ESCAPE:
                        self.paused = not self.paused
                if event.type == pg.WINDOWSIZECHANGED:
                    self.update_window()
                # if event.type == pg.WINDOWRESIZED:
                #     print("Event: Window Resized")

                if not self.paused:
                    self.world.pacman.handle_events(event)

            mx, my = pg.mouse.get_pos()

            if not self.paused:
                self.world.render(self.current_FPS)
                self.world.update()
                self.render_ui()

                pg.display.update()
                self.screen.fill(BACKGROUND_COLOUR)

                self.tick()

            self.compute_fps(then)
        
        self.quit()
    
    def compute_fps(self, then : int):
        ms = ((time.time()*1000) - then)
        if ms != 0.0:
            self.current_FPS = 1000/ms

    def tick(self):
        if os.name == "nt":
            self.clock.tick_busy_loop(FPS)
        else:
            self.clock.tick(FPS)
    
    def quit(self):
        # Serialize data
        f = open(DATA_FILE_PATH, "r+")
        hs = self.world.pacman.highscore
        file_score = int(f.read())
        if hs != file_score:
            f.seek(0)
            f.write(str(hs))
            f.truncate()
        
        # Terminate media library
        pg.quit()

    def update_window(self):
        window_width = pg.display.get_window_size()[0]
        window_height = pg.display.get_window_size()[1]
        print(window_width, window_height)
        self.world.update_dimensions(window_width, window_height)

    def render_text(self):
        highscore_title = TITLE_FONT.render("High Score", True, (255, 255, 255))
        highscore_value = SUBTITLE_FONT.render(str(self.world.pacman.highscore), True, (255, 255, 255))

        score_title = TITLE_FONT.render("Score", True, (255, 255, 255))
        score_value = SUBTITLE_FONT.render(str(self.world.pacman.score), True, (255, 255, 255))

        self.screen.blit(highscore_title, (10, 75))
        self.screen.blit(highscore_value, (10, 120))

        self.screen.blit(score_title, (10, 170))
        self.screen.blit(score_value, (10, 205))
    
    def render_life_row(self):
        life_count = self.world.pacman.lives
        starting_x = 70
        radius = 15
        for i in range(life_count):
            Utils.draw_pie(self.screen, PACMAN_COLOUR, (starting_x+i*(2*radius+5), 750), radius, ICON_ANGLE, (2*pi)-(ICON_ANGLE))

    def render_ui(self):
        self.render_text()
        self.render_life_row()


if __name__ == "__main__":
    main = Main()
