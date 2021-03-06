import asyncio
import curses
import random
import time
from itertools import cycle
from random import randint, choices
from trash.space_garbage import fly_garbage
import glob, os

from curses_tools import draw_frame, read_controls, get_frame_size

coroutines = []


def get_image(image_name):
    with open(image_name, 'r') as file:
        image_content = file.read()
    return image_content


async def starship_animation(canvas, start_row, start_column, images):
    for image in cycle(images):
        image_row, image_col = get_frame_size(image)
        rows_number, columns_number = canvas.getmaxyx()

        row_bottom = rows_number - image_row
        col_right = columns_number - image_col

        rows_direct, columns_direct, space_pressed = read_controls(canvas)
        start_row = start_row + rows_direct
        start_column = start_column + columns_direct

        if max(start_row, image_row) == image_row:
            start_row = 0
        if min(start_row, row_bottom) == row_bottom:
            start_row = row_bottom
        if max(start_column, image_col) == image_col:
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
        await get_sleep(5)

        canvas.addstr(row, column, symbol)
        await get_sleep(2)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await get_sleep(5)

        canvas.addstr(row, column, symbol)
        await get_sleep(2)


async def get_sleep(tics):
    for _ in range(tics):
        await asyncio.sleep(0)


async def fill_orbit_with_garbage(canvas, x):
    os.chdir("trash")
    garbage_images = [get_image(file) for file in glob.glob('*.txt')]

    while True:
        for frame in cycle(garbage_images):
            await get_sleep(20)
            coroutines.append(fly_garbage(canvas=canvas, column=randint(1, x), garbage_frame=frame))


def draw(canvas):
    canvas.border()
    symbols = '..+..:::..'
    img_1 = get_image('rocket_frame_1.txt')
    img_2 = get_image('rocket_frame_2.txt')
    images = [img_1, img_2]
    y, x = window.getmaxyx()
    global coroutines
    coroutines = [(blink(canvas, row=randint(0, y - 2),
                         column=randint(0, x - 2),
                         symbol=random.choice(symbols))) for _ in range(150)]

    row_middle = (y // 2) - 3
    col_middle = (x // 2) - 3

    coroutines.append(starship_animation(canvas, row_middle, col_middle, images))
    coroutines.append(fill_orbit_with_garbage(canvas, x))

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
