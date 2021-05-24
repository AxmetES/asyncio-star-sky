import asyncio
import curses
import random
import time
from itertools import cycle
from random import randint

from curses_tools import draw_frame, read_controls, get_frame_size


def get_file(filename):
    with open(filename, 'r') as file:
        file_context = file.read()
    return file_context


async def starship_animation(canvas, start_row, start_column, images):
    for image in cycle(images):
        frame_row, frame_col = get_frame_size(image)
        rows_number, columns_number = canvas.getmaxyx()

        row_bottom = rows_number - frame_row
        col_right = columns_number - frame_col

        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        start_row = start_row + rows_direction
        start_column = start_column + columns_direction

        if max(start_row, frame_row) == frame_row:
            start_row = 0
        if min(start_row, row_bottom) == row_bottom:
            start_row = row_bottom
        if max(start_column, frame_col) == frame_col:
            start_column = 0
        if min(start_column, col_right) == col_right:
            start_column = col_right

        draw_frame(canvas, start_row, start_column, image, negative=False)
        canvas.refresh()
        for _ in range(0, 2):
            await asyncio.sleep(0)
            draw_frame(canvas, start_row, start_column, image, negative=True)


async def blink(canvas, row, column, symbol='*'):
    for _ in range(0, random.randint(1, 5)):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        for _ in range(1, 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for _ in range(1, 2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        for _ in range(1, 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for _ in range(1, 2):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    symbols = '..+..:::..'
    img_1 = get_file('rocket_frame_1.txt')
    img_2 = get_file('rocket_frame_2.txt')
    images = [img_1, img_2]
    y, x = window.getmaxyx()
    coroutines = [(blink(canvas, row=randint(0, y - 2), column=randint(0, x - 2), symbol=random.choice(symbols))) for _
                  in range(100)]

    row_middle = (y // 2) - 3
    col_middle = (x // 2) - 3

    coroutines.append(starship_animation(canvas, row_middle, col_middle, images))

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
