import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def render():
    global distance,elev,azi,r_x,r_y
    global Mt
    global isperspec
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glLoadIdentity()
    d=distance


    #시점 구현
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)
    glMatrixMode(GL_MODELVIEW)
    glOrtho(-5,5,-5,5,-5,5)
    d=distance
    if isperspec:
       # glMatrixMode(GL_PROJECTION)
        gluPerspective(45,1,1,10)
        d*=3
       # glMatrixMode(GL_MODELVIEW)
        
    glTranslatef(Mt[0],Mt[1],Mt[2])
    glRotate(r_y,1,0,0)
    glRotate(r_x,0,1,0)
    gluLookAt(d,0,d,0,0,0,0,1,0)
   # print(distance*np.cos(np.rad2deg(azi))*np.cos(np.rad2deg(elev)),
        #      distance*np.sin(np.rad2deg(elev)),
      #        distance*np.sin(np.rad2deg(azi))*np.cos(np.rad2deg(elev)))
  #  gluPerspective(45,1,1,10)


  
    ####single mesh mode
    glColor3ub(125,125,125)
    drawFrame()
       #light구현
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
        
    glPushMatrix()
    lightPos=(30,40,50,0)
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
    glPopMatrix()

    lightColor=(1,1,1,1)

    ambientLightColor=(.1,.1,.1,.1)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,lightColor)
    glLightfv(GL_LIGHT0,GL_SPECULAR,lightColor)
    glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLightColor)

        #glPushMatrix()

        #glPopMatrix()
    objectColor=(1,0,0,0)
    specularObjectColor=(1,1,1,1)
    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,objectColor)
    glMaterialfv(GL_FRONT,GL_SHININESS,10)
    glMaterialfv(GL_FRONT,GL_SPECULAR,specularObjectColor)


    if isanimating:
        for objs in get_objlist():
            drawCube_glDrawElements(objs)


    if not isanimating:
        #obj파일 구현
        
        objlist=get_obj()

        if obj:
            glColor3ub(240,240,240)
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
            drawCube_glDrawElements(obj)
  #   print(distance*np.cos(np.rad2deg(azi))*np.cos(np.rad2deg(elev)))

isperspec=False
isanimating=False
positionSet=np.array([0.5,0.5,0.5])
distance=1
elev,azi=45,-45
objlist=[]
obj=[]

def parsingVertexAndIndexArray(filename):
  #  varr=np.array([[]])
    varr=np.array([])
    narr=np.array([])
    iarr_quad=np.array([])
    iarr_tri=np.array([])
    iarr_poly=np.array([])
    v=[]
    n=[]
    i_q=[]
    i_t=[]
    i_p=[]
    with open(filename) as data:
        for line in data.readlines():
            parseline=line.split(' ',10)
            if parseline[0]=="v":
                v.append((parseline[1],parseline[2],parseline[3][:-1]))
                #varr=np.append(varr,[np.array([parseline[1],parseline[2],parseline[3][:-1]])])
            if parseline[0]=="vn":
                n.append((parseline[1],parseline[2],parseline[3][:-1])) 
                
            if parseline[0]=="f":
                indexed_t=[]
                indexed_q=[]
                indexed_p=[]
                if len(parseline)==4:
                    for toparse in parseline[1:]:
                        pparseline=toparse.split('/',3)
                        indexed_t.append(pparseline[0])
                        i_t.append(indexed_t)
                elif len(parseline)==5:
                    for toparse in parseline[1:]:
                        pparseline=toparse.split('/',4)
                        indexed_q.append(pparseline[0])
                        i_q.append(indexed_q)
                elif len(parseline)>5:
                    for toparse in parseline[1:]:
                        pparseline=toparse.split('/')
                        indexed_p.append(pparseline[0])
                        i_p.append(indexed_p)
    #print(v)
    varr=np.asarray(v,float)
    #적정 크기로 변환
    div=np.max(varr)-np.min(varr)
    varr/=(div/5)   
    narr=np.asarray(n,float)
    iarr_tri=np.asarray(i_t,int)
    iarr_tri-=1
    iarr_quad=np.asarray(i_q,int)
    iarr_quad-=1
    iarr_poly=np.asarray(i_p,int)
    iarr_poly-=1
    
    print("Filename : "+filename.split('\\')[-1])
    print("Number of face : "+str(len(iarr_tri)+len(iarr_quad)))
    print("Number of 3-vertices : "+str(len(iarr_tri)))
    print("Number of 4-vertices : "+str(len(iarr_quad)))
    print("Number of more than 4-vertices : "+str(len(iarr_poly)))
    
   # print(varr)
   # print(narr)
   # print(iarr)
    return varr,narr,iarr_tri,iarr_quad ,iarr_poly

def drawCube_glDrawElements(objfile):
    varr=objfile[0]
    #print(varr)
    narr=objfile[1]
    iarr_tri=objfile[2]
    iarr_quad=objfile[3]
    iarr_poly=objfile[4]
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3,GL_FLOAT,0,varr)
    glNormalPointer(GL_FLOAT,3*narr.itemsize,narr)
    glDrawElements(GL_TRIANGLES, iarr_tri.size, GL_UNSIGNED_INT, iarr_tri)
    glDrawElements(GL_QUADS, iarr_quad.size, GL_UNSIGNED_INT, iarr_quad)
    glDrawElements(GL_POLYGON,iarr_poly.size,GL_UNSIGNED_INT,iarr_poly)


    
#단일 obj파일 갱신
def set_obj(filename):
    global obj
    varr,narr,iarr_tri,iarr_quad,iarr_poly=parsingVertexAndIndexArray(filename)
    obj=[varr,narr,iarr_tri,iarr_quad,iarr_poly]

def get_obj():
    global obj
    return obj


#여러 obj파일 추가
def add_objlist(filename,x,y,z):
    global objlist
    varr,narr,iarr_tri,iarr_quad,iarr_poly=parsingVertexAndIndexArray(filename)
    if x != 0:
        varr[:,0]+=x
    if y !=0:
        varr[:,1]+=y
    if z!=0:
        varr[:,2]+=z
    obj=[varr,narr,iarr_tri,iarr_quad,iarr_poly]

    objlist.append(obj)
    
def get_objlist():
    global objlist
    
    return objlist



def key_callback(window,key,scancode,action,mods):
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            global isperspec
            if isperspec==True:
                isperspec=False
            else:
                isperspec=True
        elif key==glfw.KEY_H:
            global isanimating
            if isanimating==True:
                isanimating=False
            else:
                isanimating=True

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
r_x=45
r_y=45
def cursor_callback(window,xpos,ypos):
    global before_xpos,before_ypos
    global leftClick,rightClick

    if leftClick==True:
        global elev,azi,r_x,r_y
        x=xpos-before_xpos
        y=ypos-before_ypos
        #print(x,y)
        before_xpos=xpos
        before_ypos=ypos
     #   print(elev)

        elev-=y*0.0005
        azi+=x*0.0005
        r_x+=x*0.3
        r_y+=y*0.3
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
        Mt[2]-=0
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

            
def drop_callback(count,paths):
    print(paths[0])
    set_obj(paths[0])

           
            
          




def drawFrame():

    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([5.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,5.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,5.]))
    glEnd()

    glBegin(GL_QUADS)
    glColor3ub(150,150,150)
    glVertex3f(5,0,5)
    glVertex3f(-5,0,5)
    glVertex3f(-5,0,-5)
    glVertex3f(5,0,-5)
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
    glfw.set_drop_callback(window,drop_callback)

    #filename="../../obj/cube-tri.obj"
    add_objlist("./obj/cube-tri.obj",0,0,0)
    add_objlist("./obj/cylinder-tri.obj",3,0,0)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=='__main__':
    main()
