
import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

gCamAng = 0
gCamHeight = 1.

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -1 ,  1 ,  1 ), # v0
            (  1 ,  1 ,  1 ), # v1
            (  1 , -1 ,  1 ), # v2
            ( -1 , -1 ,  1 ), # v3
            ( -1 ,  1 , -1 ), # v4
            (  1 ,  1 , -1 ), # v5
            (  1 , -1 , -1 ), # v6
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    a=0.5773502691896258
    b=0.8164965809277261
    c=0.4082482904638631
    narr=np.array([
        (-a,a,a),
        (b,c,c),
        (c,-c,b),
        (-c,-b,c),
        (-c,c,-b),
        (c,b,-c),
        (a,-a,-a),
        (-b,-c,-c),
        ],'float32')
        
    return varr, iarr,narr
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight,objectColorArr
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_R:
            objectColorArr[0]=1-objectColorArr[0]
        elif key==glfw.KEY_G:
            objectColorArr[1]=1-objectColorArr[1]
        elif key==glfw.KEY_B:
            objectColorArr[2]=1-objectColorArr[2]

            
objectColorArr=np.array([0,0,0,1])
def render():
    global gCamAng, gCamHeight,objectColorArr
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object
    # glEnable(GL_RESCALE_NORMAL)

    # light position
    glPushMatrix()

    t = glfw.get_time()


    lightPos = (3.,4.,5.,1)   
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()


    lightColor = (1,1,1,1)
    ambientLightColor = (.1,.1,.1,.1)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (objectColorArr)
    specularObjectColor = (1,1,1,1)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    # glRotatef(t*(180/np.pi),0,1,0)    # try to uncomment: rotate object
    # glScalef(1.,.2,1.)    # try to uncomment: scale object

    glColor3ub(0, 0, 255) # glColor*() is ignored if lighting is enabled


    drawCube_glDrawElements()
    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray,gNormalArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    narr=gNormalArray

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3,GL_FLOAT,3*varr.itemsize,varr)
    glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
# ...
gVertexArrayIndexed = None
gIndexArray = None

def main():
    # ...
    global gVertexArrayIndexed, gIndexArray,gNormalArray

    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2016025196', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    gVertexArrayIndexed, gIndexArray,gNormalArray = createVertexAndIndexArrayIndexed()
    print(gVertexArrayIndexed)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
