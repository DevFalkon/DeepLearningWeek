import pygame as pg
import sys
import numpy as np

WIDTH = 700
HEIGHT = 700
GRID_WIDTH = WIDTH-200
GRID_HEIGHT = HEIGHT-100
FPS = 100

pg.init()
pg.display.init()
pg.display.set_caption("DeepLearningWeek")
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


def create_grid(rows, columns):
    ls = [[0 for j in range(columns)] for i in range(rows)]
    return ls


def render_grid(grid):
    x_pos = 0
    y_pos = 0

    x_increment = GRID_WIDTH/len(grid[0])
    y_increment = GRID_HEIGHT/len(grid)

    for row in grid:
        pg.draw.rect(screen, (255,255,255), rect=(0, y_pos, GRID_WIDTH, 1))
        y_pos += y_increment
    pg.draw.rect(screen, (255, 255, 255), rect=(0, y_pos, GRID_WIDTH, 1))

    for column in grid[0]:
        pg.draw.rect((screen), (255,255,255), (x_pos, 0, 1, GRID_HEIGHT))
        x_pos += x_increment
    pg.draw.rect((screen), (255, 255, 255), (x_pos, 0, 1, GRID_HEIGHT))

    pg.display.update(pg.Rect(0, 0, GRID_WIDTH+1, GRID_HEIGHT+1))


grid = create_grid(50, 50)
render_grid(grid)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)
