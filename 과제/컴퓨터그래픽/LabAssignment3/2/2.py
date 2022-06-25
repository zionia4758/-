import glfw
import numpy as np
from OpenGL.GL import *

global degree
global p
global keyset
p=0
keyset=[glfw.KEY_W,glfw.KEY_E,glfw.KEY_S,glfw.KEY_D,glfw.KEY_X]

degree=np.linspace(450,120,12)
degree*=np.pi/180


def key_callback(window,key,scancode,action,mods):
    global T
    degree_ten = np.pi/18
    if action==glfw.PRESS:
        if key == glfw.KEY_W:
            T=np.array([[1, 0 ,0],
                        [0, 0.9 ,0],
                        [0, 0, 1]])@T
        if key==glfw.KEY_E:
            T=np.array([[1 ,0 ,0],
                        [0, 1.1 ,0],
                        [0, 0, 1]])@T
        if key==glfw.KEY_S:
            T=np.array([[np.cos(degree_ten) ,-np.sin(degree_ten) ,0],
                        [np.sin(degree_ten), np.cos(degree_ten) ,0],
                        [0, 0, 1]])@T
        if key==glfw.KEY_D:
            T=np.array([[np.cos(-degree_ten) ,-np.sin(-degree_ten) ,0],
                        [np.sin(-degree_ten), np.cos(-degree_ten) ,0],
                        [0, 0, 1]])@T
        if key==glfw.KEY_X:
            T=np.array([[1 ,0 ,0.1],
                        [0, 1 ,0],
                        [0, 0, 1]])@T

        if key==glfw.KEY_C:
            T=np.array([[1 ,0 ,-0.1],
                        [0, 1 ,0],
                        [0, 0, 1]])@T
        if key == glfw.KEY_R:
            T=np.array([[-1, 0 ,0],
                        [0, -1 ,0],
                        [0, 0, 1]])@T
        if key==glfw.KEY_1:
            T=np.identity(3)
               
    return
    
def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()
    
def main():
    if not glfw.init():
        return
  
    window=glfw.create_window(480,480,"2016025196",None,None)
    if not window:
        glfw.terminate()
        return

    global T
    T=np.identity(3)
    glfw.set_key_callback(window,key_callback)
    
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(T)
 
        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=="__main__":
    main()
