import asyncio
import curses
import random
import time

from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size

TIC_TIMEOUT = 0.1

class EventLoopCommand:
    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):
    def __init__(self, seconds):
        self.seconds = seconds


async def sleep(times):
    for _ in range(times):
        await Sleep(0.1) 


async def blink(canvas, row, column, symbol='*'): 
    time_offset = random.randint(0, 20)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(time_offset)
        time_offset = 20

        canvas.addstr(row, column, symbol)
        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await sleep(2)

    canvas.addstr(round(row), round(column), 'O')
    await sleep(2)
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


async def animate_spaceship(canvas, start_row, start_column, rocket_frames):
    """Display animation of a spaceship with changing the frame rate and movement control."""
    rows_number, columns_number = canvas.getmaxyx()
    min_tic, min_frame_rate = 1, 4
    max_tic, max_frame_rate = 2, 6

    tic, frame_rate = max_tic, max_frame_rate

    for frame in cycle(rocket_frames):
        rows_direction, columns_direction, _ = read_controls(canvas)
        frame_rows, frame_columns = get_frame_size(frame)

        if 0 < start_row + rows_direction < rows_number - frame_rows:
            start_row += rows_direction 
        if 1 < start_column + columns_direction < columns_number - frame_columns - 1:
            start_column += columns_direction    
       
        draw_frame(canvas, start_row, start_column, frame)
        await sleep(tic)

        draw_frame(canvas, start_row, start_column, frame, negative=True)
        await sleep(0)

        frame_rate -= 1
        if frame_rate > 0:
            continue

        if tic == max_tic:
            tic, frame_rate = min_tic, min_frame_rate
        else:
            tic, frame_rate = max_tic, max_frame_rate
    

def draw(canvas):
    with open("animation_frames/rocket_frame_1.txt", "r") as rocket_1:
        rocket_frame_1 = rocket_1.read()
    with open("animation_frames/rocket_frame_2.txt", "r") as rocket_2:
        rocket_frame_2 = rocket_2.read()
    rocket_frames = [rocket_frame_1, rocket_frame_2] 

    curses.curs_set(False)
    canvas.nodelay(True)   
    canvas.border()

    stars_number = 100
    stars = '+*.:'
    rows_number, columns_number = canvas.getmaxyx()
    rows_centre = rows_number // 2
    columns_centre = columns_number // 2
    start_row = rows_centre + 1
    start_column = columns_centre - 2
    rows_speed = -1.5
    columns_speed = 0

    coroutines = [fire(canvas, rows_centre, columns_centre, rows_speed, columns_speed)]

    for _ in range(1, stars_number):
        row = random.randint(1, rows_number - 2)
        column = random.randint(1, columns_number - 2)
        star =  random.choice(stars)
        coroutine = blink(canvas, row, column, star)
        coroutines.append(coroutine)

    coroutines.append(animate_spaceship(canvas, start_row, start_column, rocket_frames))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
               coroutines.remove(coroutine)   
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
