import asyncio
import curses
import time


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
    coroutines = [blink(canvas, row=5, column=20 + _, symbol='*') for _ in range(5)]
    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(Fal
                    )
