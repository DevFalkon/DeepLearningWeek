import pygame as pg
import sys
import numpy as np

WIDTH = 700
HEIGHT = 700
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

    x_increment = WIDTH/len(grid[0])
    y_increment = HEIGHT/len(grid)

    for row in grid:
        pg.draw.rect(screen, (255,255,255), rect=(0, y_pos, WIDTH, 1))
        y_pos += y_increment

    for column in grid[0]:
        pg.draw.rect((screen), (255,255,255), (x_pos, 0, 1, HEIGHT))
        x_pos += x_increment

    pg.display.update()


grid = create_grid(50, 50)
render_grid(grid)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)
print('test')
