import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def render():
    global distance,elev,azi
    global Mt,Mr
    global isperspec
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glLoadIdentity()


    glMatrixMode(GL_MODELVIEW)
    if isperspec:
        glMultMatrixf(Mt.T)
        gluLookAt(distance,0,0,0,0,0,0,1,0)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45,1,1,10)
        glMatrixMode(GL_MODELVIEW)


    else :
        #gluLookAt(distance,0,0,0,0,0,0,1,0)

        glOrtho(-5,5,-5,5,-5,5)

        glMultMatrixf(Mt.T)
        gluLookAt(1,0,0,0,0,0,0,1,0)


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
        distance*=1+(yoffset/10)
        Mt[0:3,0:4]*=1+(yoffset/10)
    else :
        if distance>0.001:
            distance*=1+(yoffset/10)
            Mt[0:3,0:4]*=1+(yoffset/10)
            
            
    

before_xpos=0
before_ypos=0
azi=0
elev=0
leftClick=False
rightClick=False
Mt=np.identity(4)
Mr=np.identity(4)
def cursor_callback(window,xpos,ypos):
    global before_xpos,before_ypos
    global leftClick,rightClick
    global Mr,Mt
    if leftClick==True:

        x=xpos-before_xpos
        y=ypos-before_ypos
        before_xpos=xpos
        before_ypos=ypos

        deg_x=np.deg2rad(x)
        deg_y=np.deg2rad(y)

        print(x,y)
        if x!=0:
            rM=np.identity(4)
            rM[0:3,0:3]=np.array([[np.cos(deg_x),0,np.sin(deg_x)],
                         [0,1,0],
                         [-np.sin(deg_x),0,np.cos(deg_x)]])
            Mt=rM@Mt


        if y!=0:
            rM=np.identity(4)
            rM[1:3,1:3]=np.array([[np.cos(deg_y),-np.sin(deg_y)],
                         [np.sin(deg_y),np.cos(deg_y)]])

            Mt=rM@Mt

        

        return

    if rightClick==True:

        x=xpos-before_xpos
        y=ypos-before_ypos
        before_xpos=xpos
        before_ypos=ypos
        tM=np.identity(4)
     #   print(y)
        tM[0,3]+=x*0.005
        tM[1,3]-=y*0.005
        Mt=tM@Mt
        return 
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
