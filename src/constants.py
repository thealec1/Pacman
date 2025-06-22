import pygame as pg
from math import pi
import os

pg.font.init()

TITLE_FONT = pg.font.Font(None, 50)
SUBTITLE_FONT = pg.font.Font(None, 30)
NORMAL_FONT = pg.font.Font(None, 32)
MASSIVE_FONT = pg.font.Font(None, 150)

BACKGROUND_COLOUR = (0, 0, 0)
PACMAN_COLOUR = (255, 255, 0)
GHOST_RUN_COLOUR = (0, 0, 100)
STICKY_TEXT_COLOUR = (253, 182, 255)
GHOST_SCORE_COLOUR = (166, 234, 255)

ICON_ANGLE = 40*pi/180
ICON_SIZE = 512

COLOUR_PACMAN = False
COLOUR_WORLD = False

EAT_GHOST_SCORE = 200

FPS = 60

DATA_FILE_PATH = "data/data.txt"
LEVEL_FILE_PATH = "data/level.txt"

WINDOW_TITLE = "Pacman 2024"
