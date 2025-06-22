from math import sqrt, sin, cos, pi
import pygame as pg
import os

class Utils:

    FPS = 60
    COLOUR_WAVE_FREQ = FPS*20

    @staticmethod
    def get_distance(x1 : float, y1 : float, x2 : float, y2 : float) -> float:
        d = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
        return d

    @staticmethod
    def draw_pie(screen : pg.Surface, colour : tuple, centre : tuple, radius : int, start_angle : float, end_angle : float, aa=True, thickness=1) -> None:
        theta = start_angle
        t = pg.time.get_ticks()
        while theta <= end_angle:

            freq = Utils.COLOUR_WAVE_FREQ
            r = Utils.colour_wave(freq, t, theta+10)
            g = Utils.colour_wave(freq, t, theta)
            b = Utils.colour_wave(freq, t, theta+20)

            # colour = (r, g, b)
            if aa:
                pg.draw.aaline(screen, colour, centre, ( (radius*cos(theta)+centre[0]), (radius*sin(-theta)+centre[1]) ), thickness)
            else:
                pg.draw.line(screen, colour, centre, ( (radius*cos(theta)+centre[0]), (radius*sin(-theta)+centre[1]) ), thickness)

            theta += 0.01

    @staticmethod
    def draw_pie(screen : pg.Surface, colour : tuple, centre : tuple, radius : int, start_angle : float, end_angle : float, special_colour=False, aa=True, thickness=1, ring=False) -> None:
        theta = start_angle
        t = pg.time.get_ticks()
        while theta <= end_angle:

            freq = Utils.COLOUR_WAVE_FREQ
            r = Utils.colour_wave(freq, t, theta+10)
            g = Utils.colour_wave(freq, t, theta)
            b = Utils.colour_wave(freq, t, theta+20)

            if ring:
                pg.draw.aaline(screen, colour, ( (radius*9/10*cos(theta)+centre[0]), (radius*9/10*sin(-theta)+centre[1]) ), ( (radius*cos(theta)+centre[0]), (radius*sin(-theta)+centre[1]) ), thickness)
            else:
                if special_colour:
                    colour = (r, g, b)
                if aa:
                    pg.draw.aaline(screen, colour, centre, ( (radius*cos(theta)+centre[0]), (radius*sin(-theta)+centre[1]) ), thickness)
                else:
                    pg.draw.line(screen, colour, centre, ( (radius*cos(theta)+centre[0]), (radius*sin(-theta)+centre[1]) ), thickness)

            theta += 0.01
    
    @staticmethod
    def load_res(resource_name : str, dimensions : tuple = ()) -> pg.Surface:
        directory = os.path.join("res", resource_name)
        
        surf = pg.image.load(directory).convert_alpha()

        if not len(dimensions):
            return surf
        
        return pg.transform.smoothscale(surf, (dimensions[0], dimensions[1]))
    
    @staticmethod
    def colour_wave(freq, time, phase_shift) -> float:
        max = 255
        min = 0
        a = (max - min) / 2
        c = (max + min) / 2
        return a * sin (((2*pi)/(freq)) * time - phase_shift) + c
