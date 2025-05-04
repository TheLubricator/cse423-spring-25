from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as rd

width, height = 600, 800

#score
score = 0
game_over = False

#diamond
x_mid = rd.randint(-250,250)
d_top = 345
d_bottom = None
d_left = None
d_right = None
gap = 30

color = rd.uniform(0.5,1), rd.uniform(0.5,1), rd.uniform(0.5,1)
speed = 0.5
temp = speed

#pause/play
pause = False
btn = [[(-5,380,-5,350),(5,380,5,350)],[(-5,380,-5,350), (-5,350, 15,365),(15,365, -5,380)]]

#catcher
c_left = -35
c_right = 30
c_top = -375
c_bottom = -390
catcher_speed = 15

def points(x,y):
    global r,g,b
    glPointSize(2)
    glColor3f(r,g,b)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def lines(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx>=0 and dy>=0:
        if abs(dx)>abs(dy):
            drawLine_0(x1, y1, x2, y2, 0)
        else:
            drawLine_0(y1, x1, y2, x2, 1)
    if dx<0 and dy>=0:
        if abs(dx)>abs(dy):
            drawLine_0(-x1, y1, -x2, y2, 3)
        else:
            drawLine_0(y1, -x1, y2, -x2, 2)
    if dx<0 and dy<0:
        if abs(dx)>abs(dy):
            drawLine_0(-x1, -y1, -x2, -y2, 4)
        else:
            drawLine_0(-y1, -x1, -y2, -x2, 5)
    if dx>=0 and dy<0:
        if abs(dx)>abs(dy):
            drawLine_0(x1, -y1, x2, -y2, 7)
        else:
            drawLine_0(-y1, x1, -y2, x2, 6)

def drawZones(x, y, zone):
    if zone==0:
        points(x,y)
    elif zone==1:
        points(y,x)
    elif zone==2:
        points(-y,x)
    elif zone==3:
        points(-x,y)
    elif zone==4:
        points(-x,-y)
    elif zone==5:
        points(-y,-x)
    elif zone==6:
        points(y,-x)
    elif zone==7:
        points(x,-y)

def drawLine_0(x1, y1, x2, y2, zone):       #converted to zone 0 coordinates 
    x = x1                                  
    y = y1
    
    dx = x2 - x1
    dy = y2 - y1
    p = 2*dy - dx
    
    while (x<=x2):
        drawZones(x,y, zone)
        x += 1

        if p<0:
            p += 2*dy
        else:
            p += 2*dy - 2*dx
            y += 1

def buttons():
    global r,g,b, btn, pause
    # exit button
    r,g,b = 1,0,0
    lines(250,380, 280,350)
    lines(250,350, 280,380)

    #pause/play
    r,g,b = 1,1,0
    if not pause:
        i = 0
    else:
        i = 1
    for co_ordinates in btn[i]:
        x1, y1, x2, y2 = co_ordinates
        lines(x1,y1,x2,y2)
    
    #restart
    r,g,b = 0,1,1
    lines(-280,365, -265,380)
    lines(-280,365, -245,365)
    lines(-280,365, -265,350)



    
def diamond():
    global x_mid, d_top, d_bottom, d_left, d_right, gap, r,g,b, color

    x = x_mid
    d_left = x - (gap/2)
    d_right = x + (gap/2)
    d_bottom = d_top - gap
    y_mid = d_top - (gap/2)

    r, g, b = color
    lines(x,d_top, d_left, y_mid)
    lines(d_left, y_mid, x,d_bottom)
    lines(x,d_bottom, d_right, y_mid)
    lines(d_right, y_mid, x,d_top)

def reset_diamond():
    global x_mid, d_top, color

    x_mid = rd.randint(-250,250)
    d_top = 345
    color = rd.uniform(0.5,1), rd.uniform(0.5,1), rd.uniform(0.5,1)

def catcher():
    global r,g,b, c_left, c_right, c_top, c_bottom, game_over
    
    if not game_over:
        r,g,b = 1,1,1
    else:
        r,g,b = 1,0,0
    lines(c_left,c_top, c_right,c_top)          #top horizontal line
    lines(c_left,c_bottom, c_right,c_bottom)    #bottom horizontal line
    lines(c_left,c_bottom, c_left,c_top)        #bottom horizontal line
    lines(c_right,c_bottom, c_right,c_top)      #bottom horizontal line


def convertXY(x,y):
    global width, height

    x = x- (width/2)
    y = (height-y) - (height/2)

    return x,y

def mouse(button, state, x, y):
    global pause, game_over, score, speed, temp

    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            x, y = convertXY(x,y)

            #restart
            if (-280<=x<=-245) and (350<=y<=380):
                score = 0
                speed = 0.5
                game_over = False
                pause = False
                print("Starting over....")
                reset_diamond()
                glutPostRedisplay()

            #exit button
            if (250<=x<=280) and (350<=y<=380):                           
                print("Goodbye")
                glutLeaveMainLoop()
            
            
            if not game_over: 
                #pause

                if (not pause) and (-5<=x<=5) and (350<=y<=380):
                    speed = 0
                    print(x,y)
                    pause = True

                #resume
                elif pause and (-5<=x<=15) and (350<=y<=380):
                    speed = temp
                    pause = False


def specKey(key, x,y):
    global catcher_speed, c_left, c_right, c_top, c_bottom, game_over, pause

    if not game_over and not pause:
        if key==GLUT_KEY_RIGHT:
            if c_right <300:
                c_left += catcher_speed
                c_right += catcher_speed

            if c_right>300:
                c_right = 300
            
        if key==GLUT_KEY_LEFT:
            if c_left >-300:
                c_left -= catcher_speed
                c_right -= catcher_speed
            if c_left<-300:
                c_left = -300

    glutPostRedisplay()

def animate():
    global speed, gap, d_top, d_bottom, x_mid, c_top, c_left, c_right, color, score, high_score, game_over

    d_top -= speed
    if not game_over:
        bottom_next = d_top - gap
        if (d_bottom == c_top or bottom_next<c_top) and ((c_left<=d_left<=c_right) or (c_left<=d_right<=c_right)):
            score+=1
            print(f"Score: {score}")
            reset_diamond()
    
        if d_bottom<-400:
            game_over = True
            print(f'''Game Over!
Your Score: {score}''')   

        #handling speed with time
        time = glutGet(GLUT_ELAPSED_TIME)
        if (time%3000)==0 and speed<1:
            speed += 0.1
            print("Speed increased")
        glutPostRedisplay()    

def iterate():
    global width, height

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0-(width/2), width - (width/2), 0-(height/2), height - (height/2), -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global game_over, speed

    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    catcher()
    buttons()
    if not game_over:
        diamond()
     
    glutSwapBuffers()
    

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(width, height) 
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Catch the Diamonds!") 
glutMouseFunc(mouse)
glutSpecialFunc(specKey)
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutMainLoop()

