import asyncio
import curses
import random
import time
from random import randint


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        for _ in range(1):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for _ in range(1):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for _ in range(1):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    symbols = '..+..*..:..'
    x, y = window.getmaxyx()
    coroutines = [(blink(canvas, row=randint(0, x - 2), column=randint(0, y - 2), symbol=random.choice(symbols))) for _
                  in range(500)]

    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    curses.wrapper(draw)
    curses.curs_set(True)
