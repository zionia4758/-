import glfw
import numpy as np
from OpenGL.GL import *

global keyset
keyset=[glfw.KEY_Q,glfw.KEY_E,glfw.KEY_A,glfw.KEY_D,glfw.KEY_1]
global transf
transf=np.identity(4)

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
    glMultMatrixf(transf)
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0,0.5]))
    glVertex2fv(np.array([0,0]))
    glVertex2fv(np.array([0.5,0]))
    glEnd()

def key_callback(window,key,scancode,action,mods):
    global transf
    if action==glfw.PRESS:
        if key==keyset[0]:
            transf[3,0]-=0.1
        elif key==keyset[1]:
            transf[3,0]+=0.1   
        elif key==keyset[2]:
            degree=np.pi/18
            arr=np.identity(4)
            arr[0:2,0:2]=[[np.cos(degree),np.sin(degree)],
                          [-np.sin(degree),np.cos(degree)]]
            transf=transf@arr
        elif key==keyset[3]:
            degree=np.pi/18
            arr=np.identity(4)
            arr[0:2,0:2]=[[np.cos(degree),-np.sin(degree)],
                          [np.sin(degree),np.cos(degree)]]
            transf=transf@arr
        elif key==keyset[4]:
            transf=np.identity(4)

def main():
    if not glfw.init():
        return
  
    window=glfw.create_window(480,480,"2016025196",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window,key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=="__main__":
    main()
