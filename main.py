import asyncio
import curses
import random
import time
from random import randint


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        for _ in range(random.randint(1, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for _ in range(random.randint(1, 2)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        for _ in range(random.randint(1, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for _ in range(random.randint(1, 5)):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    symbols = '..+..:::..'
    x, y = window.getmaxyx()
    coroutines = [(blink(canvas, row=randint(0, x - 2), column=randint(0, y - 2), symbol=random.choice(symbols))) for _
                  in range(100)]

    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        time.sleep(0.2)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    curses.curs_set(False)
    curses.wrapper(draw)

