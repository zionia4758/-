import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

#array=np.array([[0,0,0],[0.3,0,0],[0.3,0.3,0],[0,0.3,0],[0,0.3,0.3],
           #       [0.3,0.3,0.3],[0.3,0,0.3],[0,0,0.3],[0,0,0]])

def render():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLoadIdentity()

    gluPerspective(45,1,1,10)

  #  gluLookAt(3,3,3,0,0,0,0,1,0)
   
    glRotatef(36.264,1,0,0)
    glRotatef(-45,0,1,0)
    glTranslatef(-3,-3,-3)
    drawFrame()
    glColor3ub(255,255,255)
    drawCubeArray()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glEnd()
    glBegin(GL_LINES)
    glColor3ub(0,0,255)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()
    glBegin(GL_LINES)

    glColor3ub(0,255,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glEnd()

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
