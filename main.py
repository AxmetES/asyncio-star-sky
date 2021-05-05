import asyncio
import curses


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

    def __init__(self, seconds):
        self.seconds = seconds


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)
        await Sleep(2)
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        await Sleep(0.3)
        canvas.refresh()

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)
        await Sleep(0.5)
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        await Sleep(0.3)
        canvas.refresh()


def draw(canvas):
    canvas.border()
    coroutine = blink(canvas, row=5, column=20, symbol='*')
    while True:
        coroutine.send(None)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
