import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def render():
    global distance,gCamAngY,gCamAngX

    global isperspec,isanimate,iswire
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    d=distance

    #시점 구현
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_NORMALIZE)
    glMatrixMode(GL_MODELVIEW)
    glOrtho(-5,5,-5,5,-5,5)
    if isperspec:
        gluPerspective(45,1,1,10)
        gluLookAt(d*np.sin(gCamAngX),d*np.sin(gCamAngY),d*np.cos(gCamAngX),0,0,0,0,1,0)

    else :
        glScalef(1/d,1/d,1/d)
        gluLookAt(d*np.sin(gCamAngX),d*np.sin(gCamAngY),d*np.cos(gCamAngX),0,0,0,0,1,0)
    glTranslatef(offsetX,offsetY,offsetZ)



    glColor3ub(125,125,125)
    drawFrame()
       #light구현
    
    if iswire:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    if not iswire:
        glEnable(GL_NORMALIZE)
        
    ##1번빛 태양
    lightPos=(30,40,50,0)
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos)

    lightColor=(1,1,1,1)

    ambientLightColor=(.1,.1,.1,.1)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,lightColor)
    glLightfv(GL_LIGHT0,GL_SPECULAR,lightColor)
    glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLightColor)
    ##2번빛 조
    lightpos=(50,0,10,1)
    glLightfv(GL_LIGHT1,GL_POSITION,lightPos)

    lightColor=(0,1,1,1)

    ambientLightColor=(.3,.3,.3,.3)
    glLightfv(GL_LIGHT1,GL_DIFFUSE,lightColor)
    glLightfv(GL_LIGHT1,GL_SPECULAR,lightColor)
    glLightfv(GL_LIGHT1,GL_AMBIENT,ambientLightColor)    

        #glPushMatrix()

        #glPopMatrix()
    objectColor=(1,0,0,0)
    specularObjectColor=(1,1,1,1)
    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,objectColor)
    glMaterialfv(GL_FRONT,GL_SHININESS,8)
    glMaterialfv(GL_FRONT,GL_SPECULAR,specularObjectColor)
  
    ####single mesh mode
    if isanimating:
        #for objs in get_objlist():
            #drawCube_glDrawElements(objs)
        objs=get_objlist()
        
        animate(objs)
        #drawCube_glDrawElements(objs[5:10])
    if not isanimating:
        #obj파일 구현
        
        objlist=get_obj()

        if obj:
            glColor3ub(240,240,240)
            drawCube_glDrawElements(obj)
  #   print(distance*np.cos(np.rad2deg(azi))*np.cos(np.rad2deg(elev)))


isperspec=False
isanimating=False
iswire=False
isforcedsmooth=False
positionSet=np.array([0.5,0.5,0.5])
distance=1

objlist=np.empty((0,6),dtype='object')
obj=[]

def parsingVertexAndIndexArray(filename):
    
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
    fnarr=np.array([])
    with open(filename) as data:
        for line in data.readlines():
            if line=="\n":
                continue
            line=line[:-1]


            parseline=line.split(' ')
            if len(parseline)<=1 or parseline[0]=='#':
                continue



            if parseline[0]=="v":
                parseline=list(filter(None,parseline))

                v.append((parseline[1],parseline[2],parseline[3]))

                #varr=np.append(varr,[np.array([parseline[1],parseline[2],parseline[3][:-1]])])
            if parseline[0]=="vn":
                parseline=list(filter(None,parseline))
                n.append((parseline[1],parseline[2],parseline[3])) 
                
            if parseline[0]=="f":
                parseline=list(filter(None,parseline))
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




    try:
        varr=np.asarray(v,float)
    except:
        print(v)
    #적정 크기로 변환

    narr=np.asarray(n,float)
    try:
        iarr_tri=np.asarray(i_t,int)
    except Exception as e:
        print("in iarr "+ e)
        #print(i_t)
    iarr_tri-=1
    try:
        iarr_quad=np.asarray(i_q,int)
    except Exception as E:
        print("in narr "+e)
        #print(i_q)
    iarr_quad-=1
    try:
        iarr_poly=np.asarray(i_p,int)
    except Exception as e:
        #print(i_p)
        print(e)
    iarr_poly-=1

    ##법선 계산
    for new in iarr_tri:
        fnarr=np.append(fnarr,getNorm(varr,new))
    for new in iarr_quad:
        fnarr=np.append(fnarr,getNorm(varr,new))
    for new in iarr_poly:
        fnarr=np.append(fnarr,getNorm(varr,new))
    

    
    
    print("Filename : "+filename.split('\\')[-1])
    print("Number of face : "+str(len(iarr_tri)+len(iarr_quad)))
    print("Number of 3-vertices : "+str(len(iarr_tri)))
    print("Number of 4-vertices : "+str(len(iarr_quad)))
    print("Number of more than 4-vertices : "+str(len(iarr_poly)))
    
   # print(varr)
   # print(narr)
   # print(iarr)
    return varr,narr,fnarr,iarr_tri,iarr_quad ,iarr_poly,

def getNorm(varr,iarr):
    a1=varr[iarr[0]]-varr[iarr[1]]
    a2=varr[iarr[2]]-varr[iarr[1]]
    nv=np.cross(a1,a2)
    nv=nv/np.sqrt(np.dot(nv,nv))
    return nv


def animate(objlist):
    #table
    glPushMatrix()
    t=glfw.get_time()
    glRotatef(-t*10,0,1,0)
    drawCube_glDrawElements(objlist[0:6])

    #column
    cnt=0
    for i in np.radians([0,45,90,135,180,225,270,315]):
        cnt+=1
        glPushMatrix()
        glTranslatef(5*np.cos(i),0,5*np.sin(i))
        glRotatef(-np.rad2deg(i),0,1,0)
        
        glPushMatrix()
        if cnt%2==0:
            glScalef(1,1-np.sin(t),1)
        else :
            glScalef(1,1+np.sin(t),1)
        drawCube_glDrawElements(objlist[6:12])
        glPopMatrix()
        
        #penguin
        glPushMatrix()
        #glTranslatef(0,np.cos(t),0)
        if cnt%2==0:
            glTranslatef(0,1.1-np.sin(t),0)
        else:
            glTranslatef(0,1.1+np.sin(t),0)
        
        drawCube_glDrawElements(objlist[12:18])
        glPopMatrix()
        glPopMatrix()


    glPopMatrix()

def drawCube_glDrawElements(objfile):
    global isforcedsmooth
    try:
        varr,narr,fnarr,iarr_tri,iarr_quad,iarr_poly=objfile
       # print(len(iarr_tri),len(iarr_quad),len(iarr_poly))
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3,GL_FLOAT,0,varr)
        if not isforcedsmooth:
            glNormalPointer(GL_FLOAT,3*narr.itemsize,narr)
        else :
            glNormalPointer(GL_FLOAT,3*fnarr.itemsize,fnarr)
        glDrawElements(GL_TRIANGLES, iarr_tri.size, GL_UNSIGNED_INT, iarr_tri)
        glDrawElements(GL_QUADS, iarr_quad.size, GL_UNSIGNED_INT, iarr_quad)
        glDrawElements(GL_POLYGON,iarr_poly.size,GL_UNSIGNED_INT,iarr_poly)
    except Exception as e:
        print(e)
        print(len(varr),len(narr),len(fnarr),len(iarr_tri),len(iarr_quad),len(iarr_poly))
        print(objfile)
        exit(0)



    
#단일 obj파일 갱신
def set_obj(filename):
    global obj

    if obj:
        print("기존 obj 제거")
        obj.clear()
    varr,narr,fnarr,iarr_tri,iarr_quad,iarr_poly=parsingVertexAndIndexArray(filename)
    obj=[varr,narr,fnarr,iarr_tri,iarr_quad,iarr_poly]

def get_obj():
    global obj
    return obj


#여러 obj파일 추가
def add_objlist(filename,x,y,z,s):
    global objlist
    varr,narr,fnarr,iarr_tri,iarr_quad,iarr_poly=parsingVertexAndIndexArray(filename)
    varr*=s
    if x != 0:
        varr[:,0]+=x
    if y !=0:
        varr[:,1]+=y
    if z!=0:
        varr[:,2]+=z

    obj=np.array([varr,narr,fnarr,iarr_tri,iarr_quad,iarr_poly],dtype='object')
    #print(obj)
    #print(len(iarr_tri),len(iarr_quad),len(iarr_poly))
    #print(obj)
    objlist=np.append(objlist,obj)

def get_objlist():
    global objlist
    
    return objlist



def key_callback(window,key,scancode,action,mods):
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            print('Y')
            global isperspec
            if isperspec==True:
                isperspec=False
            else:
                isperspec=True
        elif key==glfw.KEY_H:
            print('H')
            global isanimating
            if isanimating==True:
                isanimating=False
            else:
                isanimating=True
        elif key==glfw.KEY_Z:
            print('Z')
            global iswire
            if iswire==True:
                iswire=False
            else:
                iswire=True
        elif key==glfw.KEY_S:
            print('S')
            global isforcedsmooth
            if isforcedsmooth==True:
                isforcedsmooth=False
            else :
                isforcedsmooth=True

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
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glBegin(GL_QUADS)
    glColor3ub(150,150,150)
    glVertex3f(5,0,5)
    glVertex3f(-5,0,5)
    glVertex3f(-5,0,-5)
    glVertex3f(5,0,-5)
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)


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
    add_objlist("./srcobj/table.obj",0,0,0,1)
    add_objlist("./srcobj/column.obj",0,0,0,0.1)
    add_objlist("./srcobj/penguin.obj",0,0,0,1)

    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()
    return

if __name__=='__main__':
    main()
