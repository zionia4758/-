import glfw
import numpy as np
from OpenGL.GL import *

array=np.array([[0,0,0],[0.3,0,0],[0.3,0.3,0],[0,0.3,0],[0,0.3,0.3],
                  [0.3,0.3,0.3],[0.3,0,0.3],[0,0,0.3],[0,0,0]])

def render():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLoadIdentity()

   # gluPerspective(45,1,1,10)

    gluLookAt(3,3,3,0,0,0,0,1,0)
    drawFrame()
    glColor3ub(255,255,255)
    drawCubeArray()


def drawCubeArray():
    glBegin(GL_LINE_LOOP)
    for i in range(0,8):
        glVertex3f(array[i])
       

def main():
    if not glfw.init():
        return
  
    window=glfw.create_window(480,480,"2016025196",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=="__main__":
    main()
