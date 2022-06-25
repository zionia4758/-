import glfw
import numpy as np
from OpenGL.GL import *

global degree
global p
global keyset
p=0
keyset=[glfw.KEY_W,glfw.KEY_1,glfw.KEY_2,glfw.KEY_3,glfw.KEY_4,glfw.KEY_5,glfw.KEY_6,glfw.KEY_7,glfw.KEY_8,glfw.KEY_9,glfw.KEY_0,glfw.KEY_Q]

degree=np.linspace(450,120,12)
degree*=np.pi/180


def key_callback(window,key,scancode,action,mods):
    if key in keyset:
        if action==glfw.PRESS:
            global p
            p=keyset.index(key)
           
    return
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    for i in range(0,12):
        glVertex2f(np.cos(degree[i]),np.sin(degree[i]))
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(0,0)

    glVertex2f(np.cos(degree[p]),np.sin(degree[p]))
    glEnd()

    return

def main():
    if not glfw.init():
        return
  
    window=glfw.create_window(480,480,"2016025196",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window,key_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()
 
        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=="__main__":
    main()
