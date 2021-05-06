import asyncio
import curses
import random
import time
from random import randint


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


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

    x_middle = x // 2
    y_middle = y // 2
    time.sleep(20)
    coroutines.append(fire(canvas, start_row=x_middle, start_column=y_middle))
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
    curses.curs_set(False)
    curses.wrapper(draw)
