import pygame as pg

class Rect:
    def __init__(self, screen, top_x, top_y, width, height, color='white') -> None:
        self.screen = screen
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.height = height
        # Drawing the rectangle to the screen
        pg.draw.rect(screen, color, pg.Rect(self.top_x, self.top_y,
                                            self.width, self.height))
    def update(self):
        pg.display.update(pg.Rect(self.top_x, self.top_y, self.width, self.height))

    def rect_dist(self, mouse_pos):  # Returns True is the cursor is inside the rectangle
        if self.top_x <= mouse_pos[0] <= self.top_x + self.width:
            if self.top_y <= mouse_pos[1] <= self.top_y + self.height:
                return True
        return False