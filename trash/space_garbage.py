from curses_tools import draw_frame, get_frame_size
import asyncio

from explosion import explode
from obstacles import Obstacle


async def fly_garbage(canvas, obstacles, obstacles_in_last_collisions, column, garbage_frame, file, speed=0.2):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()
    column = max(column, 0)
    column = min(column, columns_number - 1)
    row = 0

    row_s, column_s = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, row_s, column_s, uid=file)
    obstacles.append(obstacle)
    while row < rows_number:
        obstacle.row = row
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        if obstacle in obstacles_in_last_collisions:
            obstacles.remove(obstacle)
            await explode(canvas, obstacle.row + obstacle.rows_size / 2, column + obstacle.columns_size / 2)
            return


async def remove_from_obstacles(canvas, obstacles, obstacles_in_last_collisions):
    rows_number, columns_number = canvas.getmaxyx()
    for obstacle in obstacles:
        if round(obstacle.row) == rows_number:
            obstacles.remove(obstacle)

