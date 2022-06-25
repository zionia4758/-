import glfw
import numpy as np
from OpenGL.GL import *

    
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


    T=np.identity(3)
    T=np.array([[1,0,0.5],
                [0,1,0],
                [0,0,1]])@T
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        degree=np.pi/180
        T=np.array([[np.cos(degree),-np.sin(degree),0],
                    [np.sin(degree),np.cos(degree),0],
                    [0,0,1]])@T
        render(T)
 
        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=="__main__":
    main()
