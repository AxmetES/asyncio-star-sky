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


async def starship_animation(canvas, x_middle, y_middle, images):
    x = x_middle
    y = y_middle
    for image in cycle(images):
        frame_size = get_frame_size(image)
        print(frame_size)
        print('frame_size-------')

        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        x = x + rows_direction
        y = y + columns_direction

        draw_frame(canvas, x, y, image, negative=False)
        canvas.refresh()
        for _ in range(0, 2):
            await asyncio.sleep(0)

            draw_frame(canvas, x, y, image, negative=True)


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
    x, y = window.getmaxyx()
    coroutines = [(blink(canvas, row=randint(0, x - 2), column=randint(0, y - 2), symbol=random.choice(symbols))) for _
                  in range(100)]

    x_middle = (x // 2) - 3
    y_middle = (y // 2) - 3

    coroutines.append(starship_animation(canvas, x_middle, y_middle, images))

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
