from curses_tools import draw_frame, get_frame_size
import asyncio

from obstacles import Obstacle


async def fly_garbage(canvas, obstacles, column, garbage_frame, file, speed=0.2):
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
        box = obstacle.dump_bounding_box()
        draw_frame(canvas, row, column, garbage_frame)
        draw_frame(canvas, box[0], box[1], box[2])
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        draw_frame(canvas, box[0], box[1], box[2], negative=True)
        row += speed


async def check_in_obstacles(canvas, obstacles):
    rows_number, columns_number = canvas.getmaxyx()
    for obstacle in obstacles:
        if round(obstacle.row) == rows_number:
            obstacles.remove(obstacle)
