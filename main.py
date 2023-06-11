import asyncio
import curses
import random
import time
from itertools import cycle
from random import randint

from physics import update_speed
from trash.space_garbage import fly_garbage
import glob, os
from curses_tools import draw_frame, read_controls, get_frame_size

coroutines = []
row_speed, column_speed = 2, 2


def get_image(file_name):
    with open(file_name, 'r') as file:
        image_content = file.read()
    return image_content


async def starship_animation(canvas, start_row, start_column, images):
    global row_speed, column_speed
    image_row, image_col = get_frame_size(images[0])
    maxy, maxx = canvas.getmaxyx()
    row_bottom = maxy - image_row
    col_right = maxx - image_col

    for image in cycle(images):
        rows_direct, columns_direct, space_pressed = read_controls(canvas)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction=rows_direct,
                                               columns_direction=columns_direct)
        start_row = start_row + row_speed
        start_column = start_column + column_speed

        if max(start_row, 0) == 0:
            start_row = 0
        if min(start_row, row_bottom) == row_bottom:
            start_row = row_bottom
        if max(start_column, 0) == 0:
            start_column = 0
        if min(start_column, col_right) == col_right:
            start_column = col_right

        draw_frame(canvas, start_row, start_column, image, negative=False)
        canvas.refresh()
        await asyncio.sleep(0)
        draw_frame(canvas, start_row, start_column, image, negative=True)


async def blink(canvas, row, column, symbol='*'):
    for _ in range(0, random.randint(1, 10)):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(1, 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1, 2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(1, 2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1, 3):
            await asyncio.sleep(0)


async def get_sleep(tics):
    for _ in range(tics):
        await asyncio.sleep(0)


async def fill_orbit_with_garbage(canvas, x):
    os.chdir("trash")
    garbage_images = [get_image(file) for file in glob.glob('*.txt')]

    while True:
        for frame in cycle(garbage_images):
            await get_sleep(20)
            coroutines.append(fly_garbage(canvas=canvas,
                                          column=randint(1, x),
                                          garbage_frame=frame))


def draw(canvas):
    canvas.border()
    symbols = '*.:'
    img_1 = get_image('rocket_frame_1.txt')
    img_2 = get_image('rocket_frame_2.txt')
    images = [img_1, img_2]
    maxy, maxx = window.getmaxyx()
    global coroutines

    coroutines = [(blink(canvas,
                         row=randint(0, maxy - 2),
                         column=randint(0, maxx - 2),
                         symbol=random.choice(symbols))) for _ in range(100)]
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
        time.sleep(0.2)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(False)
    curses.wrapper(draw)
