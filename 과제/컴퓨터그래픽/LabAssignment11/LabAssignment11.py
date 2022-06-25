import glfw
from OpenGL.GL import *
import numpy as np

p=np.array([[100,200],
            [200,300],
            [300,300],
            [400,200]])
gEditingPoint = ''

def Lerp(t, q0, q1):
    pass

def draw_curve(t, pointlist):
    pass

def render():
    global p0, p1
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,480, 0,480, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



    glColor3ub(255, 255, 255)
    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,0.01):
        q0=p[0,:]*(1-t)+p[1,:]*t
        q1=p[1,:]*(1-t)+p[2,:]*t
        q2=p[2,:]*(1-t)+p[3,:]*t
        q3=q0*(1-t)+q1*t
        q4=q1*(1-t)+q2*t
        q5=q3*(1-t)+q4*t
        glVertex2fv(q5)
    glEnd()

    glColor3ub(0,255,0)
    glBegin(GL_LINE_STRIP)

    for t in range(0,5):
        glVertex2fv(p[t%4,:])
    glEnd()

    glPointSize(20.)
    glBegin(GL_POINTS)
    glVertex2fv(p[0])
    glVertex2fv(p[1])
    glVertex2fv(p[2])
    glVertex2fv(p[3])
    glEnd()

def button_callback(window, button, action, mod):
    global p ,gEditingPoint
    if button==glfw.MOUSE_BUTTON_LEFT:
        x, y = glfw.get_cursor_pos(window)
        y = 480 - y
        
        if action==glfw.PRESS:
            if np.abs(x-p[0,0])<10 and np.abs(y-p[0,1])<10:
                gEditingPoint = 'p0'
            elif np.abs(x-p[1,0])<10 and np.abs(y-p[1,1])<10:
                gEditingPoint = 'p1'
            elif np.abs(x-p[2,0])<10 and np.abs(y-p[2,1])<10:
                gEditingPoint='p2'
            elif np.abs(x-p[3,0])<10 and np.abs(y-p[3,1])<10:
                gEditingPoint='p3'
                
        elif action==glfw.RELEASE:
            gEditingPoint = ''


def cursor_callback(window, xpos, ypos):
    global p, gEditingPoint
    ypos = 480 - ypos

    if gEditingPoint=='p0':
        p[0,0]=xpos; p[0,1]=ypos
    elif gEditingPoint=='p1':
        p[1,0]=xpos; p[1,1]=ypos
    elif gEditingPoint=='p2':
        p[2,0]=xpos; p[2,1]=ypos
    elif gEditingPoint=='p3':
        p[3,0]=xpos; p[3,1]=ypos
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2016025196', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


