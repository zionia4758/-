import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
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
    return varr, iarr
frame=0
def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def render(t):
    global gCamAng, gCamHeight,frame
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    


    X1=np.array([[20,30,30],
                 [45,60,40],
                 [60,70,50],
                 [80,85,70]])
    
    X2=np.array([[15,30,25],
                 [25,40,40],
                 [40,60,50],
                 [55,80,65]])
    first=np.empty((4),dtype='object')
    second=np.empty((4),dtype='object')
    for i in range(0,4):
        first[i]=XYZEulerToRotMat(X1[i,0:3])

        second[i]=XYZEulerToRotMat(X2[i,0:3])


    
    #255,0,0  255,255,0 0,255,0 0,0,255
    for i in range (0,4):
        if i==0:
            objectColor=(1,0,0,1)
        elif i==1:
            objectColor=(1,1,0,1)
        elif i==2:
            objectColor=(0,1,0,1)
        elif i==3:
            objectColor=(0,0,1,1)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        

        glPushMatrix()
        glMultMatrixf(first[i].T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

        Tsecond=np.identity(4)
        Tsecond[0,3]=1


        glPushMatrix()
        glMultMatrixf((first[i]@Tsecond@second[i]).T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()
     
    objectColor = (1.,1.,1.,1.)

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)


        
    if int(frame/20)==0:
        J1=slerp(first[0],first[1],frame%20/20)
        J2=slerp(second[0],second[1],frame%20/20)
    elif int(frame/20)==1:
        J1=slerp(first[1],first[2],frame%20/20)
        J2=slerp(second[1],second[2],frame%20/20)
    else :
        J1=slerp(first[2],first[3],frame%20/20)
        J2=slerp(second[2],second[3],frame%20/20)
        

    frame+=1
    frame%=60
    print(frame)

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    Tsecond=np.identity(4)
    Tsecond[0,3]=1

    glPushMatrix()
    glMultMatrixf((J1@Tsecond@J2).T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glDisable(GL_LIGHTING)


def XYZEulerToRotMat(euler):
    zang, yang, xang = euler
    zang=np.deg2rad(zang)
    yang=np.deg2rad(yang)
    xang=np.deg2rad(xang)
    Rx = np.array([[1,0,0,0],
                   [0, np.cos(xang), -np.sin(xang),0],
                   [0, np.sin(xang), np.cos(xang),0],
                   [0,0,0,1]])
    Ry = np.array([[np.cos(yang), 0, np.sin(yang),0],
                   [0,1,0,0],
                   [-np.sin(yang), 0, np.cos(yang),0],
                   [0,0,0,1]])
    Rz = np.array([[np.cos(zang), -np.sin(zang), 0,0],
                   [np.sin(zang), np.cos(zang), 0,0],
                   [0,0,1,0],
                   [0,0,0,1]])

    return Rx @ Ry @ Rz


def log(R):
    theta=np.arccos((R[0,0]+R[1,1]+R[2,2]-1)/2)
    vone=(R[2,1]-R[1,2])/2/np.sin(theta)
    vtwo=(R[0,2]-R[2,0])/2/np.sin(theta)
    vthree=(R[1,0]-R[0,1])/2/np.sin(theta)
    # print(vone,vtwo,vthree)
    rv=np.array([vone,vtwo,vthree])
    rv*=theta
    return rv

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def exp(rv):

    ang=l2norm(rv)

    cos=np.cos(ang)
    sin=np.sin(ang)
    x=rv[0]
    y=rv[1]
    z=rv[2]
    R=np.array([[cos+x*x*(1-cos), x*y*(1-cos)-z*sin,x*z*(1-cos)+y*sin,0],
                [y*x*(1-cos)+z*sin, cos+y*y*(1-cos),y*z*(1-cos)-x*sin,0],
                [z*x*(1-cos)-y*sin, z*y*(1-cos)+x*sin, cos+z*z*(1-cos),0],
                [0,0,0,1]])

    return R

    
def slerp(R1,R2,t):
    return R1@exp(t*log(R1.T@R2))



def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2016025196', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        t = glfw.get_time()
        render(t)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

