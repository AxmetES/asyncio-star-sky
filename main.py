import asyncio
import curses
import random
import time
import glob, os

from itertools import cycle
from random import randint

from fire_animation import fire
from physics import update_speed
from trash.space_garbage import fly_garbage, remove_from_obstacles
from curses_tools import draw_frame, read_controls, get_frame_size
import utils
from sleep import Sleep


year = 1956
obstacles = []
coroutines = []
obstacles_in_last_collisions = []
PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


async def count_years(canvas):
    global year
    while True:
        subwin = canvas.derwin(3, 10, 0, 0)
        subwin.border()
        draw_frame(subwin, 1, 3, str(year))
        await get_sleep(15)
        draw_frame(subwin, 1, 3, str(year), negative=True)
        year += 1
        if year in [1957, 1961, 1969, 1971, 1981, 1998, 2011, 2020]:
            await write_center(canvas, PHRASES[year])


async def write_center(canvas, text):
    maxy, maxx = window.getmaxyx()
    row_third = (maxy / 4)
    col_middle = (maxx / 2)
    image_row, image_col = get_frame_size(text)
    start_row = row_third - (image_row / 2)
    start_col = col_middle - (image_col / 2)
    for tics in range(3):
        draw_frame(canvas, start_row, start_col, text)
        await get_sleep(10)
        draw_frame(canvas, start_row, start_col, text, negative=True)
    return


async def show_gameover(canvas, obstacles, collision_row, collision_column):
    maxy, maxx = window.getmaxyx()
    row_middle = (maxy / 2)
    col_middle = (maxx / 2)

    text = """   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
                                                      
                                                      """

    image_row, image_col = get_frame_size(text)
    start_row = row_middle - (image_row / 2)
    start_col = col_middle - (image_col / 2)

    for obstacle in obstacles:
        if obstacle.has_collision(collision_row, collision_column):
            while True:
                draw_frame(canvas, start_row, start_col, text, negative=False)
                await asyncio.sleep(0)
                draw_frame(canvas, start_row, start_col, text, negative=True)


async def animate_starship(canvas, start_row, start_column, images):
    row_speed, column_speed = 0, 0
    image_row, image_col = get_frame_size(images[0])
    max_row, max_col = canvas.getmaxyx()
    row_bottom = max_row - image_row
    col_right = max_col - image_col
    start_row = start_row - (image_row / 2)
    start_column = start_column - (image_col / 2)

    for image in cycle(images):
        rows_direct, columns_direct, space_pressed = read_controls(canvas)

        start_row = start_row + row_speed
        start_column = start_column + column_speed

        if space_pressed and year > 2020:
            coroutines.append(fire(canvas,
                                   obstacles,
                                   obstacles_in_last_collisions,
                                   start_row,
                                   start_column=start_column+2))

        start_row = max(start_row, 0)
        start_row = min(start_row, row_bottom)
        start_column = max(start_column, 0)
        start_column = min(start_column, col_right)
        row_speed, column_speed = update_speed(row_speed,
                                               column_speed,
                                               rows_direction=rows_direct,
                                               columns_direction=columns_direct)

        await show_gameover(canvas, obstacles, start_row, start_column)

        draw_frame(canvas, start_row, start_column, image, negative=False)
        await Sleep(1)
        draw_frame(canvas, start_row, start_column, image, negative=True)


async def blink(canvas, row, column, offset_tics, symbol='*'):
    for _ in range(0, offset_tics):
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


def get_garbage_delay_tics(year):
    if year < 1957:
        return 40, 0.2
    elif year < 1969:
        return 20, 0.3
    elif year < 1981:
        return 14, 0.4
    elif year < 1995:
        return 10, 0.6
    elif year < 2010:
        return 8, 0.8
    elif year < 2020:
        return 6, 0.9
    else:
        return 4, 2


async def fill_orbit_with_garbage(canvas, x):
    os.chdir("trash")
    while True:
        coroutines.append(remove_from_obstacles(canvas, obstacles, obstacles_in_last_collisions))
        for file in cycle(glob.glob('*.txt')):
            garbage_tics, garbage_speed = get_garbage_delay_tics(year)
            frame = utils.get_image(file)
            await get_sleep(tics=garbage_tics)
            coroutines.append(fly_garbage(canvas=canvas,
                                          obstacles=obstacles,
                                          obstacles_in_last_collisions=obstacles_in_last_collisions,
                                          column=randint(1, x),
                                          garbage_frame=frame,
                                          file=file,
                                          speed=garbage_speed))


def draw(canvas):
    canvas.border()
    symbols = '*.*.:.:+.'
    img_1 = utils.get_image('rocket_frame_1.txt')
    img_2 = utils.get_image('rocket_frame_2.txt')
    images = [img_1, img_1, img_2, img_2]
    maxy, maxx = window.getmaxyx()
    global coroutines

    coroutines = [(blink(canvas,
                         row=randint(0, maxy - 2),
                         column=randint(0, maxx - 2),
                         offset_tics=random.randint(1,10),
                         symbol=random.choice(symbols))) for _ in range(300)]
    row_middle = (maxy / 2)
    col_middle = (maxx / 2)
    coroutines.append(count_years(canvas))
    coroutines.append(fill_orbit_with_garbage(canvas, maxx))
    coroutines.append(animate_starship(canvas, row_middle, col_middle, images))
    while True:
        try:
            for coroutine in coroutines.copy():
                coroutine.send(None)
                canvas.refresh()
        except StopIteration:
            coroutines.remove(coroutine)
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(False)
    curses.wrapper(draw)
