# import curses
# import time


# def draw(canvas):
#     curses.curs_set(False)  # Скрыть курсор
#     row, column = (5, 20)   
#     canvas.border()
#     while True:
#         canvas.addstr(row, column, '*', curses.A_DIM)
#         canvas.refresh()
#         time.sleep(2)
#         canvas.addstr(row, column, '*') 
#         canvas.refresh()
#         time.sleep(0.3)
#         canvas.addstr(row, column, '*', curses.A_BOLD)
#         canvas.refresh()
#         time.sleep(0.5)
#         canvas.addstr(row, column, '*')
#         canvas.refresh() 
#         time.sleep(0.3)

# if __name__ == '__main__':
#     curses.update_lines_cols()
#     curses.wrapper(draw)

#########    1   ########################################################



# import asyncio
# import curses
# import time


# def draw(canvas):
#     async def blink(canvas, row, column, symbol='*'):
#         while True:
#             canvas.addstr(row, column, symbol, curses.A_DIM)
#             await asyncio.sleep(0)

#             canvas.addstr(row, column, symbol)
#             await asyncio.sleep(0)

#             canvas.addstr(row, column, symbol, curses.A_BOLD)
#             await asyncio.sleep(0)

#             canvas.addstr(row, column, symbol)
#             await asyncio.sleep(0)

#     curses.curs_set(False)
#     row = 5   
#     canvas.border()

#     coroutines = [blink(canvas, row, column) for column in range(20, 30, 2)] 
#     while True: 
#         for coroutine in coroutines:
#             coroutine.send(None)
#         canvas.refresh()
#         time.sleep(2)
#         for coroutine in coroutines:           
#             coroutine.send(None)
#         canvas.refresh()    
#         time.sleep(0.3)
#         for coroutine in coroutines: 
#             coroutine.send(None)
#         canvas.refresh()
#         time.sleep(0.5) 
#         for coroutine in coroutines:          
#             coroutine.send(None)
#         canvas.refresh()
#         time.sleep(0.3)
 

# if __name__ == '__main__':
#     curses.update_lines_cols()
#     curses.wrapper(draw)


##############   2   #######################################################


# import asyncio
# import curses
# import time


# class EventLoopCommand():
#     def __await__(self):
#         return (yield self)


# class Sleep(EventLoopCommand):
#     def __init__(self, seconds):
#         self.seconds = seconds


# async def sleep(times):
#     for _ in range(times):
#         await Sleep(0.1) 


# async def blink(canvas, row, column, symbol='*'):
#     while True:
#         canvas.addstr(row, column, symbol, curses.A_DIM)
#         await sleep(20)

#         canvas.addstr(row, column, symbol)
#         await sleep(3)

#         canvas.addstr(row, column, symbol, curses.A_BOLD)
#         await sleep(5)

#         canvas.addstr(row, column, symbol)
#         await sleep(3)


# def draw(canvas):
#     curses.curs_set(False)
#     row = 5   
#     canvas.border()

#     coroutines = [blink(canvas, row, column) for column in range(20, 30, 2)] 
    
#     while True: 
#         for coroutine in coroutines:
#             coroutine.send(None)
#         canvas.refresh()
#         time.sleep(0.1)
   

# if __name__ == '__main__':
#     curses.update_lines_cols()
#     curses.wrapper(draw)


###############   3  #############################################################   

# import asyncio
# import curses
# import random
# import time

# TIC_TIMEOUT = 0.1

# class EventLoopCommand:
#     def __await__(self):
#         return (yield self)


# class Sleep(EventLoopCommand):
#     def __init__(self, seconds):
#         self.seconds = seconds


# async def sleep(times):
#     for _ in range(times):
#         await Sleep(0.1) 


# async def blink(canvas, row, column, symbol='*'):
#     while True:
#         canvas.addstr(row, column, symbol, curses.A_DIM)
#         await sleep(20)

#         canvas.addstr(row, column, symbol)
#         await sleep(3)

#         canvas.addstr(row, column, symbol, curses.A_BOLD)
#         await sleep(5)

#         canvas.addstr(row, column, symbol)
#         await sleep(3)


# def draw(canvas):
#     curses.curs_set(False)  
#     canvas.border()
#     height, width = canvas.getmaxyx()
#     number_stars = 300
#     stars = ['+', '*', '.', ':']

#     coroutines = []
#     for _ in range(1, number_stars):
#         row = random.randint(1, height - 2)
#         column = random.randint(1, width - 2)
#         star =  random.choice(stars)
#         coroutine = blink(canvas, row, column, star)
#         coroutines.append(coroutine)
    

#     while True: 
#         for coroutine in coroutines.copy():
#             coroutine.send(None)
#         canvas.refresh()
#         time.sleep(TIC_TIMEOUT)
   


# if __name__ == '__main__':
#     curses.update_lines_cols()
#     curses.wrapper(draw)


###############   4   ###############################################

import asyncio
import curses
import random
import time

from itertools import cycle

from curses_tools import draw_frame, read_controls

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


async def animate_spaceship(canvas, start_row, start_column, rocket_frames):
    """Display animation of a spaceship with cycling and changing the frame rate."""
    min_tic, min_frame_rate = 1, 4
    max_tic, max_frame_rate = 2, 6

    tic, frame_rate = max_tic, max_frame_rate

    for frame in cycle(rocket_frames):
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
    height, width = canvas.getmaxyx()
    number_stars = 100
    stars = '+*.:'
    height_centre = height // 2
    width_centre = width // 2
    rows_speed = -1.5
    columns_speed = 0

    coroutines = [fire(canvas, height_centre, width_centre, rows_speed, columns_speed)]
    for _ in range(1, number_stars):
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        star =  random.choice(stars)
        coroutine = blink(canvas, row, column, star)
        coroutines.append(coroutine)    
    coroutines.append(animate_spaceship(canvas, height_centre - 2, width_centre - 2, rocket_frames))

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


###############   5   ###############################################

# import time
# import curses


# def draw(canvas):
#     canvas.clear()
#     canvas.border()
    
#     # Отключаем отображение курсора
#     curses.curs_set(False)
    
#     # Устанавливаем координаты строки и столбца
#     row, col = 5, 20
#     canvas.addstr(row, col, 'Hello, World!')
#     canvas.refresh()
    
#     # Ждем нажатия клавиши для выхода
#     canvas.getch()


# # Основной цикл программы
# if __name__ == '__main__':
#     try:
#         curses.wrapper(draw)
#     except Exception as e:
#         print("Ошибка:", str(e))        



# import curses
# import time

# def main(stdscr):
#     # Устанавливаем скрытие курсора
#     curses.curs_set(False)
    
#     # Размер экрана
#     max_y, max_x = stdscr.getmaxyx()
    
#     # Центр экрана
#     star_row = max_y // 2
#     star_col = max_x // 2
    
#     # Настройка цветов
#     curses.start_color()
#     curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
#     brightness_levels = [
#         curses.A_DIM,
#         curses.A_NORMAL,
#         curses.A_BOLD
#     ]
    
#     try:
#         while True:
#             for level in brightness_levels + list(reversed(brightness_levels[:-1])):
#                 # Отображаем звезду с разной степенью яркости
#                 stdscr.attron(curses.color_pair(1))
#                 stdscr.attron(level)
#                 stdscr.addch(star_row, star_col, '*')
                
#                 # Обновляем экран
#                 stdscr.refresh()
                
#                 # Ждем небольшую паузу
#                 time.sleep(0.2)
#     except KeyboardInterrupt:
#         pass

# # Запустим приложение
# if __name__ == "__main__":
#     curses.wrapper(main)
