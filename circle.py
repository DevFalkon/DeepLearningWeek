from pygame import gfxdraw
import math
import pygame as pg


class Circle:
    def __init__(self, screen, centre_x, centre_y, rad, color, update=False) -> None:
        self.screen = screen
        # Drawing circle outline with antialiasing
        gfxdraw.aacircle(self.screen, centre_x, centre_y, rad, color)
        # Filling in the circle
        gfxdraw.filled_circle(self.screen, centre_x, centre_y, rad, color)

        if update:
            pg.display.update(pg.Rect(centre_x - rad - 2, centre_y - rad - 2, 2 * rad + 4, 2 * rad + 4))

        self.centre_x = centre_x
        self.centre_y = centre_y
        self.rad = rad

    def circle_dist(self, mouse_pos):  # Returns True is the cursor is inside the circle
        x_pos = mouse_pos[0] - self.centre_x
        y_pos = mouse_pos[1] - self.centre_y
        # Finding the distance of the cursor from the centre off the circle
        dist = math.sqrt(math.pow(x_pos, 2) + math.pow(y_pos, 2))
        if dist <= self.rad:
            return True
        return False