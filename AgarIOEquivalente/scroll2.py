from __future__ import division
from Tkinter import *
import ttk
import time, random
from math import sqrt
import tkFont

def norm(x, y):
    return sqrt(x**2 + y**2)

def set_mouse_position(event):
    mouse_position[0] = event.x
    mouse_position[1] = event.y

def move_cell():
    global speed
    global window_width
    global window_height
    global board_width
    global board_height
    while True:
        dir1 = mouse_position[0] - window_width/2
        dir2 = mouse_position[1] - window_height/2
        canvas.move(cell1, speed*(dir1/norm(dir1, dir2)), speed*(dir2/norm(dir1, dir2)))
        cell_position[0] += speed*dir1/norm(dir1, dir2)
        cell_position[1] += speed*dir2/norm(dir1, dir2)
        pos_x = (cell_position[0] - window_width/2)/board_width
        pos_y = (cell_position[1] - window_height/2)/board_height
        canvas.xview_moveto(pos_x)
        canvas.yview_moveto(pos_y)
        time.sleep(0.02)
        window.update()


if __name__ == '__main__':    

    window = Tk()
    window.title("Bola persigue raton") 

    h = ttk.Scrollbar(window, orient=HORIZONTAL)
    v = ttk.Scrollbar(window, orient=VERTICAL)
   
    window_width = 800
    window_height = 600
    board_width = 5000
    board_height = 5000
    helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')

    canvas = Canvas(window,  width=window_width, height=window_height, 
        bg='firebrick', scrollregion=(0, 0, board_width, board_height), 
        yscrollcommand=v.set, xscrollcommand=h.set)
    h['command'] = canvas.xview
    v['command'] = canvas.yview

    canvas.grid(column=0, row=0, sticky=(N,W,E,S))

    canvas.create_oval(50, 50, 100, 100, fill='#017517', outline='#017517')
    canvas.create_oval(500, 500, 550, 550, fill='#D55E00', outline='#D55E00')
    canvas.create_oval(700, 100, 750, 150, fill='#017517', outline='#017517')
    canvas.create_oval(500, 500, 850, 900, fill='#D55E00', outline='#D55E00')
    canvas.create_text(800,100 , font=helv36, text='Bola persigue raton')

    mouse_position = [0,0]
    canvas.bind("<Motion>", set_mouse_position)

    coords = [350, 200, 380, 230]

    cell1 = canvas.create_oval(coords[0], coords[1], coords[2], coords[3], fill='darkgoldenrod', outline='darkgoldenrod')

    speed = 4

    cell_position = [(coords[0]+coords[2])/2, (coords[1]+coords[3])/2]

    move_cell()

    window.mainloop()
