import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def render():
    global distance,elev,azi
    global Mt
    global isperspec
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLoadIdentity()
    d=distance
    if isperspec:
        gluPerspective(45,1,1,10)
        d=d*3
    glTranslatef(Mt[0],Mt[1],Mt[2])
    print(azi,elev)
    gluLookAt(d*np.cos(np.rad2deg(azi))*np.cos(np.rad2deg(elev)),
              d*np.sin(np.rad2deg(elev)),
              d*np.sin(np.rad2deg(azi))*np.cos(np.rad2deg(elev))
              ,0,0,0, 0,1,0)
   # print(distance*np.cos(np.rad2deg(azi))*np.cos(np.rad2deg(elev)),
        #      distance*np.sin(np.rad2deg(elev)),
      #        distance*np.sin(np.rad2deg(azi))*np.cos(np.rad2deg(elev)))
  #  gluPerspective(45,1,1,10)
    drawFrame()
    drawCubeArray()
 #   print(distance*np.cos(np.rad2deg(azi))*np.cos(np.rad2deg(elev)))

isperspec=False
positionSet=np.array([0.5,0.5,0.5])
distance=1
elev,azi=45,-45


def key_callback(window,key,scancode,action,mods):
    if key==glfw.KEY_V and action==glfw.PRESS:
        global isperspec
        if isperspec==True:
            isperspec=False
        else:
            isperspec=True

def scroll_callback(window,xoffset,yoffset):
    global distance
    if yoffset>0:
         if distance >0.1:
            distance*=1-yoffset/10
    else:
        distance*=1-yoffset/10
    #print(distance)


before_xpos=0
before_ypos=0
leftClick=False
rightClick=False
Mt=np.array([0.,0.,0.])
def cursor_callback(window,xpos,ypos):
    global before_xpos,before_ypos
    global leftClick,rightClick

    if leftClick==True:
        global elev,azi
        x=xpos-before_xpos
        y=ypos-before_ypos
        #print(x,y)
        before_xpos=xpos
        before_ypos=ypos
     #   print(elev)

        elev-=y*0.0005
        azi+=x*0.0005
        #print(elev,azi)

    if rightClick==True:
        global Mt
        x=xpos-before_xpos
        y=ypos-before_ypos
        before_xpos=xpos
        before_ypos=ypos
     #   print(y)
        Mt[1]-=y*0.005
        Mt[0]-=-np.cos(np.deg2rad(azi))*x*0.005
        Mt[2]-=np.cos(np.deg2rad(azi))*x*0.005
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
"""
def drawUnitCube():
    glBegin(GL_QUADS)
    glColor3ub(255,255,255)
    glVertex3f( 0., 0.,0.)
    glVertex3f(0.2, 0.,0.2)
    glVertex3f(0., 0.2, 0.2)
    glVertex3f( 0., 0.2, 0.) 
                             
    glVertex3f( 0.0,0.0, 0.0)
    glVertex3f(0.2,0.0, 0.)
    glVertex3f(0.2,0.2,0.0)
    glVertex3f( 0.,0.0,0.) 
                            
    glVertex3f( 0.0, 0.0, 0.0)
    glVertex3f(0.2, 0.0, 0.)
    glVertex3f(0.2,0., 0.2)
    glVertex3f( 0.,0., 0.2)
                             
    glVertex3f( 0.,0.2,0.2)
    glVertex3f(0.2,0.2,0.2)
    glVertex3f(0.2, 0.,0.2)
    glVertex3f( 0., 0.,0.2)
 
    glVertex3f(0.2, 0., 0.2) 
    glVertex3f(0.2, 0.2,0.2)
    glVertex3f(0.2,0.2,0.) 
    glVertex3f(0.2,0., 0.) 
                             
    glVertex3f( 0.2, 0.2,0.2) 
    glVertex3f( 0.2, 0.2, 0.)
    glVertex3f( 0.,0.2, 0.)
    glVertex3f( 0.,0.2,0.2)
    glEnd()
"""
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
