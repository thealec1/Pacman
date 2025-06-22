from utils import Utils
from tile import Tile

class Consumable(Tile):

    COLOUR = (255, 255, 255)

    def __init__(self, x, y, gx, gy, row, pacman, world):
        super().__init__(x, y, x, y, gx, gy, world, row, True)
        self.world = world
        self.SIZE = 5
        self.pacman = pacman

    def do_collision(self):
        if Utils.get_distance(self.x, self.y, self.pacman.x, self.pacman.y) < ((self.pacman.SIZE / 2)*(3/5)) + (self.SIZE/2):
            self.on_consumed()
    
    def on_consumed(self):
        self.active = False

    def update(self):
        self.do_collision()

    def render(self, screen):
        super().render(screen)
