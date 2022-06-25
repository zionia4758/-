import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def render():
    global distance
    global isperspec
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glLoadIdentity()

    d=distance

    glOrtho(-5,5,-5,5,-5,5)
    if isperspec:
        gluPerspective(45,1,1,10)
        gluLookAt(d*np.sin(gCamAngX),d*np.sin(gCamAngY),d*np.cos(gCamAngX),0,0,0,0,1,0)

    else :
        glScalef(1/d,1/d,1/d)
        gluLookAt(d*np.sin(gCamAngX),d*np.sin(gCamAngY),d*np.cos(gCamAngX),0,0,0,0,1,0)
    glTranslatef(offsetX,offsetY,offsetZ)
    drawFrame()
    drawCubeArray()

isperspec=False
positionSet=np.array([0.5,0.5,0.5])
distance=1




def key_callback(window,key,scancode,action,mods):
    if key==glfw.KEY_V and action==glfw.PRESS:
        global isperspec
        if isperspec==True:
            isperspec=False
        else:
            isperspec=True

def scroll_callback(window,xoffset,yoffset):
    global distance,Mt
    if yoffset>0:
        if distance>=0.1:
            distance*=1-(yoffset/10)

    else :
        distance*=1-(yoffset/10)


            
    

before_xpos=0
before_ypos=0
gCamAngX=0
gCamAngY=0
leftClick=False
rightClick=False
offsetX=0
offsetY=0
offsetZ=0
def cursor_callback(window,xpos,ypos):
    global before_xpos,before_ypos
    global leftClick,rightClick
    global gCamAngX,gCamAngY
    if leftClick==True:

        x=xpos-before_xpos
        y=ypos-before_ypos
        before_xpos=xpos
        before_ypos=ypos

        if x!=0:
            gCamAngX+=x*np.radians(-2)
        if y!=0:
            gCamAngY+=y*np.radians(2)
            if gCamAngY>=np.pi/2:
                gCamAngY=np.pi/2-0.001
            elif gCamAngY<=-np.pi/2:
                gCamAngY=-np.pi/2+0.001
        

        return

    if rightClick==True:
        global offsetX,offsetY,offsetZ
        x=xpos-before_xpos
        y=ypos-before_ypos
        before_xpos=xpos
        before_ypos=ypos
        offsetY-=y*np.cos(gCamAngY)*0.01
        offsetX+=x*np.cos(gCamAngX)*0.01
        offsetZ-=x*np.sin(gCamAngX)*0.01

   # print(Mt)


def button_callback(window,button,action,mod):
    global leftClick,rightClick
    global before_xpos,before_ypos
    
    #print(before_xpos)
    if action==glfw.PRESS:
        before_xpos,before_ypos=glfw.get_cursor_pos(window)
        if button==glfw.MOUSE_BUTTON_RIGHT:
            rightClick=True
        if button ==glfw.MOUSE_BUTTON_LEFT:
            leftClick=True

    if action==glfw.RELEASE:
        rightClick=False
        leftClick=False

    #print(rightClick,leftClick)

            
            
           
            
          




def drawFrame():

    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    glBegin(GL_QUADS)
    glColor3ub(100,100,100)
    glVertex3f(1,0,1)
    glVertex3f(-1,0,1)
    glVertex3f(-1,0,-1)
    glVertex3f(1,0,-1)
    glEnd()
    
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
    glColor3ub(255,255,255)
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

def main():
    if not glfw.init():
        return

    window=glfw.create_window(480,480,"2016025196",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_key_callback(window,key_callback)

    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_cursor_pos_callback(window,cursor_callback)
    glfw.set_mouse_button_callback(window,button_callback)
    
   # glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=='__main__':
    main()
