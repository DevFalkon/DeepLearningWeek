import pygame as pg
from circle import Circle
from rect import Rect


class RoundedRect:
    def __init__(self, screen, top_x, top_y, width, height, radius, color, bg_color) -> None:
        self.screen = screen
        self.pos_x, self.pos_y = top_x, top_y
        self.width, self.height = width, height
        self.rad = radius
        self.color = color
        self.bg_color = bg_color

        self.circle_pos_arr = [[self.pos_x+self.rad, self.pos_y+self.rad], 
                               [self.pos_x+self.width-self.rad, self.pos_y+self.rad], 
                               [self.pos_x+self.rad, self.pos_y+self.height-self.rad], 
                               [self.pos_x+self.width-self.rad, self.pos_y+self.height-self.rad]]

        self.rect_pos_arr = [[self.pos_x, self.pos_y], 
                             [self.pos_x+self.width-self.rad, self.pos_y], 
                             [self.pos_x, self.pos_y+self.height-self.rad], 
                             [self.pos_x+self.width-self.rad, self.pos_y+self.height-self.rad]]
        
    def draw(self):
        Rect(self.screen, self.pos_x, self.pos_y, self.width, self.height, self.color)

        # Drawing the Rectangle to blend with the background
        for p_x, p_y in self.rect_pos_arr:
            Rect(self.screen, p_x, p_y, self.rad+5, self.rad+5, self.bg_color)
        
        #Drawing the Circle to complete the rounded rect
        for p_x, p_y in self.circle_pos_arr:
            Circle(self.screen, p_x, p_y, self.rad, self.color)

    def update(self):
        pg.display.update(pg.Rect(self.pos_x, self.pos_y, self.width, self.height))
