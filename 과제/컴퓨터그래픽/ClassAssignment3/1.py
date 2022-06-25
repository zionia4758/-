import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
startNum=0
count=0
def render():
    global distance,gCamAngY,gCamAngX
    global isBVH,count
    global isperspe,iswire
    global frame,startNum
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


    if isBVH==True:
        startNum=0
        drawBVH(root,count,len(root.channels))
        count=(count+1)%frame
        


isperspec=False
iswire=False
distance=1
isBVH=False
root=0
isanimate=False


frame=0
frameTime=0
framelist=[]
namelist=[]
totalNum=0
motion=[]
class BVH:




    def __init__(self):
        self.jointNum=0
        self.joints=[]
        self.isEnd=False
        self.isRoot=False
        self.isJoint=False
        self.name=""
        

    def setChannels(self,channels):
        self.channels=channels
    def setOffset(self,offset):
        self.offset=offset


    def addJoint(self):
        newJoint=BVH()
        self.joints.append(newJoint)
        self.jointNum+=1
        newJoint.parent=self



def parsingBVH(filename):
    global root
    global namelist,totalNum,framelist,frame,frameTime
    framecount=0
    parseInfo=False
    root=BVH()
    root.isEnd=False
    depth=0
    totalNum=0
    framelist=[]
    frameTime=0
    namelist=[]
    isMotion=False
    
    with open(filename) as data:
        for line in data.readlines():
            line=line.expandtabs(1)
            line=line.strip()
            if parseInfo==True:
                print(line)
            if line=='\n':
                continue

            parseline=line.split(' ')
            if parseInfo==True:
                print(parseline)

            if isMotion==False:
                if parseline[0]=="ROOT":
                    if parseInfo==True:
                        print("Root생성")
                    totalNum=1
                    current=root
                    current.name=parseline[1]
                    namelist.append(parseline[1])
                elif parseline[0]=="OFFSET":

                    offset=np.array([parseline[1],parseline[2],parseline[3]],'float64')
                    if parseInfo==True:
                        print("Offset:"+str(offset))
                    current.setOffset(offset)               
                elif parseline[0]=="CHANNELS":
                    current.setChannels(np.array(parseline[2:]))
                    if parseInfo==True:
                        print("Channels:"+str(current.channels))
                elif parseline[0]=="JOINT":
                    depth+=1
                    totalNum+=1
                    if parseInfo==True:
                        print("Joint생성 depth ; "+str(depth))
                    current.addJoint()
                    current=current.joints[current.jointNum-1]
                    current.name=parseline[1]
                    namelist.append(parseline[1])
                    current.isJoint=True
                elif parseline[0]=="End":
                    depth+=1
                    if parseInfo==True:
                        print("End point 생성 depth ; "+str(depth))
                    current.addJoint()
                    current=current.joints[current.jointNum-1]
                    current.isEnd=True
                elif parseline[0]=="}":
                    if depth>0:
                        if parseInfo==True:
                            print("Depth -1")
                        depth-=1
                        current=current.parent
                elif parseline[0]=="MOTION":
                    isMotion=True

            elif isMotion==True:   
                if parseline[0]=="Frames:":
                    frame=int(parseline[1])
                elif parseline[0]=="Frame":
                    frameTime=float(parseline[2])

                else:
                    ##print(parseline)
                    parseline=list(map(float,parseline))
                    framelist.append(parseline)
                   ## print(len(root.framelist[0]))
                   ## print(root.framelist[0])
                    framecount+=1

    if parseInfo==True:
        if root!=current:
            print("depth:"+str(depth))
        else:
            print("Good")

        


def set_bvh(filename):
    global isBVH,root,count
    isBVH=True
    count=0
    print("Filename : "+filename)
    parsingBVH(filename)
    print("Total Joints num : ",totalNum)
    print("Name list : ",namelist)
    print("Frame num : ",frame)
    print("Frame time : ",frameTime)
    print("FPS : ",1/frameTime)




def drawBVH(root,count,channelNum):

    global startNum
    global isanimate
    if root.isEnd==True:
        return

    ##print(count,startNum,startNum+channelNum)
    ##print(framelist[count])
    

    rlist=framelist[count][startNum:startNum+channelNum]
    channel=root.channels
    if len(rlist)==6:
        root.offset=rlist[0:3]
        rlist=rlist[3:6]
        channel=root.channels[3:6]
       # print(root.offset)
        if isanimate:
            glTranslatef(root.offset[0],root.offset[1],root.offset[2])
    if isanimate:
        rotateOffset(channel,rlist)
    startNum+=len(root.channels)
    glBegin(GL_LINES)
    
    for nextJoint in root.joints:
        glVertex3fv(np.array([0,0,0]))
        glVertex3fv(nextJoint.offset)
    glEnd()
    for nextJoint in root.joints:
        if nextJoint.isEnd==True:
            continue
        glPushMatrix()
        offset=nextJoint.offset
        glTranslatef(offset[0],offset[1],offset[2])

        drawBVH(nextJoint,count,len(nextJoint.channels))
        glPopMatrix()
    
def rotateOffset(channel,rlist):
    #print(channel,rlist)
    #print(type(rlist[0]))
    for pick in channel:
        if pick.upper()=="XROTATION":
            glRotatef(rlist[0],1,0,0)
        elif pick.upper()=="YROTATION":
            glRotatef(rlist[1],0,1,0)
        elif pick.upper()=="ZROTATION":
            glRotatef(rlist[2],0,0,1)


def key_callback(window,key,scancode,action,mods):
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            print('Y')
            global isperspec
            if isperspec==True:
                isperspec=False
            else:
                isperspec=True
        elif key==glfw.KEY_SPACE:
            global isanimate
            isanimate=True

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
    set_bvh(paths[0])

           
            
          




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
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glBegin(GL_QUADS)
    glColor3ub(150,150,150)
    for i in range(-5,5):
        for j in range(-10,10):
            glVertex3fv(np.array([10*(2*i+j%2),0,10*(j+1)]))
            glVertex3fv(np.array([10*(2*i+1+j%2),0,10*(j+1)]))
            glVertex3fv(np.array([10*(2*i+1+j%2),0,10*(j+2)]))
            glVertex3fv(np.array([10*(2*i+j%2),0,10*(j+2)]))            
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)


def main():
    global frameTime
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


    lastUpdateTime=0
    lastFrameTime=0
    isRender=False
    #filename="../../obj/cube-tri.obj"

    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        now=glfw.get_time()
        deltaTime=now-lastUpdateTime
        
        glfw.poll_events()
        if isRender==False:
            render()
            isRender=True
        
        if(now-lastFrameTime)>=frameTime:
            glfw.swap_buffers(window)
            lastFrameTime=now
            isRender=False
        lastUpdateTime=now

    glfw.terminate()
    return

if __name__=='__main__':
    main()
