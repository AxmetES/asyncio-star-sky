import asyncio
import curses
import random
import time
import glob, os

from itertools import cycle
from random import randint

from fire_animation import fire
from obstacles import show_obstacles, Obstacle, show_obstacle
from physics import update_speed
from trash.space_garbage import fly_garbage, check_in_obstacles
from curses_tools import draw_frame, read_controls, get_frame_size
import utils
from sleep import Sleep


obstacles = []
coroutines = []


async def starship_animation(canvas, start_row, start_column, images):
    row_speed, column_speed = 0, 0
    image_row, image_col = get_frame_size(images[0])
    max_row, max_col = canvas.getmaxyx()
    row_bottom = max_row - image_row
    col_right = max_col - image_col
    for image in cycle(images):
        rows_direct, columns_direct, space_pressed = read_controls(canvas)

        start_row = start_row + row_speed
        start_column = start_column + column_speed

        if space_pressed:
            coroutines.append(fire(canvas, obstacles, start_row, start_column=start_column+2))

        if max(start_row, 0) == 0:
            start_row = 0
        if min(start_row, row_bottom) == row_bottom:
            start_row = row_bottom
        if max(start_column, 0) == 0:
            start_column = 0
        if min(start_column, col_right) == col_right:
            start_column = col_right

        row_speed, column_speed = update_speed(row_speed,
                                               column_speed,
                                               rows_direction=rows_direct,
                                               columns_direction=columns_direct)

        draw_frame(canvas, start_row, start_column, image, negative=False)
        canvas.refresh()
        await Sleep(1)
        draw_frame(canvas, start_row, start_column, image, negative=True)


async def blink(canvas, row, column, symbol='*'):
    for _ in range(0, random.randint(1, 10)):
        await Sleep(1)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await get_sleep(3)

        canvas.addstr(row, column, symbol)
        await get_sleep(2)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await get_sleep(2)

        canvas.addstr(row, column, symbol)
        await get_sleep(3)


async def get_sleep(tics=1):
    for _ in range(0, tics):
        await Sleep(1)


async def fill_orbit_with_garbage(canvas, x):
    os.chdir("trash")
    while True:
        for file in cycle(glob.glob('*.txt')):
            frame = utils.get_image(file)
            await get_sleep(tics=20)
            coroutines.append(fly_garbage(canvas=canvas,
                                          obstacles=obstacles,
                                          column=randint(1, x),
                                          garbage_frame=frame,
                                          file=file))
            coroutines.append(check_in_obstacles(canvas, obstacles))


def draw(canvas):
    canvas.border()
    symbols = '*.*.:.:+.'
    img_1 = utils.get_image('rocket_frame_1.txt')
    img_2 = utils.get_image('rocket_frame_2.txt')
    images = [img_1, img_2]
    maxy, maxx = window.getmaxyx()
    global coroutines

    coroutines = [(blink(canvas,
                         row=randint(0, maxy - 2),
                         column=randint(0, maxx - 2),
                         symbol=random.choice(symbols))) for _ in range(300)]
    row_middle = (maxy / 2)
    col_middle = (maxx / 2)
    coroutines.append(starship_animation(canvas, row_middle, col_middle, images))
    coroutines.append(fill_orbit_with_garbage(canvas, maxx))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(False)
    curses.wrapper(draw)
