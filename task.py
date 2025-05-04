from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 

coordinate_arr = []
ball_speed = 0.01
speed_x = random.uniform(0.1,0.5)
speed_y = random.uniform(0.1,0.5)
blink = False 
freeze = False 


def draw_points(x,y,colour):
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(colour[0],colour[1],colour[2])
    glVertex2f(x,y)
    glEnd()

def update_point():
    global ball_speed
    for i in coordinate_arr:
        if freeze==False: 
                #x boundary
            if i['x']>=495 and i['x_direction']==True:  
                i['x_direction']=False  #direction siifted to lefrt
            elif i['x']<=2 and i['x_direction']==False:             #these two only checks boundary hit or nah
                i['x_direction']=True  # direction revertetdd ti right
            else:
                if i['x_direction']==True:  #within bouondary and actual movement(after appropriate direction adjustment)
                    i['x']+=ball_speed*speed_x
                else:  
                    i['x']-=ball_speed*speed_x

             

            #y boundaryu
            if i['y'] >= 495 and i['y_direction']==True:  # y same as x
                i['y_direction']=False 
            elif i['y']<= 2 and i['y_direction']==False:  
                i['y_direction']=True 
            else:           
                if i['y_direction'] :  
                    i['y']+=ball_speed*speed_y
                else: 
                    i['y']-=ball_speed*speed_y
        else:  # freeze ccondiition
            pass #doesnt change squat ie stays in same pos



def mouseListener(button,state,x,y) :
    global blink, freeze
    if (freeze == False) : 
        if (button==GLUT_RIGHT_BUTTON) and (state==GLUT_DOWN): 
            print("point created")
            coordinate_arr.append({'x': random.randrange(50,400,1),'y': random.randrange(50,450,1), 'colour':[random.random(),random.random(),random.random()],'x_direction':random.choice([True,False]),'y_direction':random.choice([True,False])})
        
        if (button==GLUT_LEFT_BUTTON) and (state==GLUT_DOWN) and blink==False : 
            blink = True 
            print("Blink!")
        elif (button==GLUT_LEFT_BUTTON) and (state==GLUT_DOWN) and blink==True: 
            blink = False 
            print("Blink off!")
        glutPostRedisplay()


def specialKeyListener(key,x,y) :
    global ball_speed 
    if (freeze==False) : 
        if (key==GLUT_KEY_UP) :
            ball_speed*=2 
            print("Speed increased by",ball_speed)           
        if (key==GLUT_KEY_DOWN) :
            ball_speed/=2
            print("Speed decreased by",ball_speed)
    glutPostRedisplay()   

    

def keyBoardListener(key,x,y) :
    global freeze
    if (key==b' ')  and freeze!=True:
        print("Freeze initiated")
        freeze=True
    elif (key==b' ')  and freeze==True:
        print("Unfreezing screen")
        freeze=False

        
    glutPostRedisplay()


def animation(): 
    global freeze 
    if (freeze == False): 
        update_point()
    else:
        pass 

    glutPostRedisplay()
  

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():

    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    for i in coordinate_arr : # setting x,y,colour for the draw_points from the coordinate_arr of points info 
        x=i['x']
        y=i['y']
        if (blink==False) :
            colour=i['colour']
        else :
            colour=[0.0,0.0,0.0]
        
        draw_points(x,y,colour)

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyBoardListener)
glutIdleFunc(animation)
glutMainLoop()