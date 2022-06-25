import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import*


def render():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLoadIdentity()

    myFrustum(-1,1,-1,1,1,10)
    myLookAt(np.array([5,3,5]),np.array([1,1,-1]),np.array([0,1,0]))

    #glFrustum(-1,1, -1,1, 1,10)
    #gluLookAt(5,3,5, 1,1,-1, 0,1,0)


    drawFrame()

    glColor3ub(255,255,255)
    drawCubeArray()
    
def myFrustum(left,right,bottom,top,near,far):
    Mpers=np.zeros((4,4))
    Mpers[0,0]=2/(right-left)
    Mpers[0,3]=-(right+left)/(right-left)
    Mpers[1,1]=2/(top-bottom)
    Mpers[1,3]=-(top+bottom)/(top-bottom)
    Mpers[2,2]=-2/(far-near)
    Mpers[2,3]=-(far+near)/(far-near)
    Mpers[3,3]=1
    glMultMatrixf(Mpers)

def myLookAt(arr1,arr2,arr3):

    w=(arr1-arr2)
    w=w/np.sqrt(np.dot(w,w))
    u=np.cross(arr3,w)
    u=u/np.sqrt(np.dot(u,u))
    v=np.cross(w,u)

    Mcam=np.identity(4)
    Mcam[0,0:3]=u
    Mcam[1,0:3]=v
    Mcam[2,0:3]=w
    Mcam[0:3,3]=[-u@arr1,-v@arr1,-w@arr1]

    glMultMatrixf(Mcam.T)





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

    glColor3ub(0,0,255)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)

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
