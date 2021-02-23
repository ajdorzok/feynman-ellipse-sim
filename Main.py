import sys
import threading
import math
import pygame as pg
from pygame import gfxdraw

pg.init()
screen = pg.display.set_mode((0, 0),pg.FULLSCREEN|pg.HWSURFACE|pg.DOUBLEBUF )
screenH = screen.get_height()
screenW = screen.get_width()
if screenW > screenH: #this ensures that everything fits on any screen resolution.
    screenMin = screenH
else:
    screenMin = screenW
radius = 0.45 * screenMin
cx = screenW//2
cy = screenH//2
pg.gfxdraw.aacircle(screen, cx, cy,int(0.45 * screenMin), (255, 255, 255))
gfxdraw.filled_circle(screen, cx, cy, 2, (255, 0, 0))
font = pg.font.SysFont(pg.font.get_fonts()[20],32)
text1 = font.render("Click anywhere inside the circle.", True, (255, 255, 255), (0, 0, 0))
screen.blit(text1, (0, 0))
pg.display.update() #display everything so far
clicked = False #used to prevent multiple clicks, starting multiple threads doing the same thing

def dist_check():#check to see if distance from mouse to center of screen is less than the radius
    if math.sqrt(((cx - mpos[0])*(cx - mpos[0])) + ((cy - mpos[1])*(cy - mpos[1]))) < radius:
        return True
    else:
        return False

def mousepos():#update mouse position
    while threading.main_thread().is_alive():
        global mpos # global variable is used by the calculate function to track its position
        mpos = pg.mouse.get_pos()

def mouseclicked():
    while threading.main_thread().is_alive():
        screen.fill((0,0,0))
        #redraw the main circle
        pg.gfxdraw.aacircle(screen, cx, cy,
                        int(0.45 * screenMin), (255, 255, 255))
        #draw the center point
        gfxdraw.filled_circle(screen, cx, cy, 2, (255, 0, 0))
        calculate()
        text2 = font.render("Press the 'Esc' key to quit.", True, (255, 255, 255), (0, 0, 0))
        screen.blit(text2, (0, 0))
        pg.display.flip() #update the display with the new information

def calculate():
    if dist_check(): #if the mouse is inside the circle
        for i in range(0,720,1): #iterate from 0 to 360 in steps of 1.
            x = mpos[0]
            x2 = cx + (radius * math.cos(i * 3.14159 / 360))
            midx = (x + x2) / 2
            y = mpos[1]
            y2 = cy + (radius * math.sin(i * 3.14159 / 360))
            midy = (y + y2) / 2
            d = math.sqrt(((x - x2) * (x - x2)) + ((y - y2) * (y - y2)))
            theta = math.atan2(x - x2, y2 - y)
            r = d*2 #this can any lenght. Longer is better for extreme values.
            x3 = midx + (r * math.cos(theta))
            y3 = midy + (r * math.sin(theta))
            x4 = (2 * midx) - x3 #the reflection of x3 across the ray
            y4 = (2 * midy) - y3 #the reflection of y3 across the ray
            #gfxdraw.line(screen,x,y,int(x2),int(y2),(255,0,255)) #rays
            #the line above draws lines from the cursor to points on the outer white circle
            gfxdraw.line(screen, int(midx), int(midy), int(x3), int(y3), (0, 255, 0)) # half of rotated rays
            gfxdraw.line(screen, int(midx), int(midy), int(x4), int(y4), (0, 255, 0)) #other side of the rotated ray
            #gfxdraw.filled_circle(screen, int(midx), int(midy),2, (0, 0, 255)) #ray midpoints colored blue
            gfxdraw.filled_circle(screen, int(x), int(y), 2, (0, 255, 0)) #green dot for cursor position.

#start a thread that will keep the position of the mouse updated
iothread = threading.Thread(target=mousepos)
iothread.start()
while threading.main_thread().is_alive():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        # if user presses the Esc key, then close the application
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
        if not clicked:
            if event.type == pg.MOUSEBUTTONDOWN:
                t1 = threading.Thread(target=mouseclicked)
                t1.start()
                clicked = True