import glfw
import numpy as np
from OpenGL.GL import *

global d
d=-np.pi/360

global M1,M2
M1=np.array([[1,0,0.5],
            [0,1,0],
            [0,0,1]])
M2=np.array([[1,0,0],
            [0,1,0.5],
            [0,0,1]])
 
def render():
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0,0]))
    glVertex2fv(np.array([1,0]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0,0]))
    glVertex2fv(np.array([0,1]))
    glEnd()

    glColor3ub(255,255,255)

    global M1,M2

    p1=np.array([0.5,0,1])
    p2=np.array([0,0.5,1])
    v1=np.array([0.5,0,0])
    v2=np.array([0,0.5,0])

    M1=np.array([[np.cos(d),-np.sin(d),0],
                 [np.sin(d),np.cos(d),0],
                 [0,0,1]])@M1

    M2=np.array([[np.cos(d),-np.sin(d),0],
                 [np.sin(d),np.cos(d),0],
                 [0,0,1]])@M2
    p1=M1@p1
    p2=M2@p2
    v1=M1@v1
    v2=M2@v2

    glBegin(GL_POINTS)
    glVertex2fv(p1[:2])
    glEnd()
    glBegin(GL_POINTS)
    glVertex2fv(p2[:2])
    glEnd()

    glBegin(GL_LINES)
    glVertex2fv(np.array([0,0]))
    glVertex2fv(v1[:2])
    glEnd()
    glBegin(GL_LINES)
    glVertex2fv(np.array([0,0]))
    glVertex2fv(v2[:2])
    glEnd()


def main():
    if not glfw.init():
        return
  
    window=glfw.create_window(480,480,"2016025196",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=="__main__":
    main()
