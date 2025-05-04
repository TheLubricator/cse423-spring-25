#####TASK 1####################################


import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

r_sky, g_sky, b_sky = 255, 255, 255
alternator_stat=True
raindrops = []
rain_direction = 0  #initializing w 0 ie falls str8
num_raindrops = 100  #100 raindrops made, any more looks ugly for 500x500



for i in range(num_raindrops):
    x = random.uniform(-250, 250)
    y = random.uniform(120, 250) #iof y kept as same range as x then it wouldd seem rain if formed from ground for random drops so initial ones are kept in range of sky only
    raindrops.append([x, y])


def keyboardListener(key, x, y):
    global r_sky, g_sky, b_sky
    if key == b'w' and r_sky<239:
        r_sky += 17
        g_sky += 17
        b_sky += 17
        print("Daylight Inbound")
    if key == b's' and r_sky > 16:
        r_sky -= 17
        g_sky -= 17
        b_sky -= 17
        print("Night Approaching")
    glutPostRedisplay()
def specialKeyListener(key, x, y):
    global rain_direction
    if key==GLUT_KEY_LEFT:
        if rain_direction > -0.45:
            rain_direction -= 0.05  
        print("Rain bending left:", round(rain_direction,2))
    if key== GLUT_KEY_RIGHT:		
        if rain_direction < 0.45:
            rain_direction += 0.05  
        print("Rain bending right:", round(rain_direction,2))
    glutPostRedisplay()

def draw_points(x, y):
    glPointSize(5)  
    glBegin(GL_POINTS)
    glVertex2f(x, y)  
    glEnd()

def sky_ground():
    global r_sky, g_sky, b_sky
    glPointSize(2)  
    glBegin(GL_QUADS)
    glColor3f(r_sky / 255, g_sky / 255, b_sky / 255)
    glVertex2f(-250, 250)
    glVertex2f(250, 250)
    glVertex2f(250, 120)
    glVertex2f(-250, 120) 
    #ground
    glColor3f(128 / 255, 86 / 255, 45 / 255)
    glVertex2f(-250, 120)
    glVertex2f(250, 120)
    glVertex2f(250, -250)
    glVertex2f(-250, -250)
    glEnd()

def draw_house():
    glPointSize(5)
    glBegin(GL_TRIANGLES)
    #roof
    glColor3f(59 / 255, 6 / 255, 112 / 255)
    glVertex2f(0, 80)
    glVertex2f(-110, 20)
    glVertex2f(110, 20)
    #room
    glColor3f(179 / 255, 180 / 255, 186 / 255)
    glVertex2f(-90, 20)
    glVertex2f(-90, -70)
    glVertex2f(90, 20)
    
    glVertex2f(90, 20)
    glVertex2f(-90, -70)
    glVertex2f(90, -70)
    #door
    glColor3f(40 / 255, 62 / 255, 201 / 255)
    glVertex2f(-15, -70)
    glVertex2f(15, -70)
    glVertex2f(15, -10)

    glVertex2f(15, -10)
    glVertex2f(-15, -70)
    glVertex2f(-15, -10)
    #window-1
    glVertex2f(45, -10)
    glVertex2f(45, -30)
    glVertex2f(65, -30)

    glVertex2f(65, -30)
    glVertex2f(65, -10)
    glVertex2f(45, -10)
    #window-2
    glVertex2f(-45, -10)
    glVertex2f(-45, -30)
    glVertex2f(-65, -30)

    glVertex2f(-65, -30)
    glVertex2f(-65, -10)
    glVertex2f(-45, -10)
    glEnd()


def draw_raindrop(x, y):
    global alternator_stat
    glBegin(GL_LINES)
    if alternator_stat==True:
        glColor3f(0, 0, 1)  # Blue color for raindrops
        alternator_stat=False
    else:
        alternator_stat=True #alternate to grey color like demo
        glColor3f(179/255, 174/255, 170/255)
    glVertex2f(x, y)  
    glVertex2f(x, y - 10)  #rain kept to 10 length
    glEnd()


def update_raindrops():
    global raindrops, rain_direction
    for drop in raindrops:
        drop[1] -= 0.5  # y-axis change indicates speed of rain
        drop[0] += round(rain_direction,2)  # x-axis chang indicatess cchange in direction
        if drop[1] < -250:  
            drop[1] = random.uniform(120, 250) #regenrates old raindrop points if it goes out of screen width of 500x500
            drop[0] = random.uniform(-250, 250)
    glutPostRedisplay()



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0.0, 1.0)  # xmin xmax y min y max zmin z max
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    sky_ground()
    draw_house()
    update_raindrops()
    for drop in raindrops:
        draw_raindrop(drop[0], drop[1])
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)  # Window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # Window name

glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()




#####################################################################################################################

#####TASK 2#################



# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random 

# coordinate_arr = []
# ball_speed = 0.01
# speed_x = random.uniform(0.1,0.5)
# speed_y = random.uniform(0.1,0.5)
# blink = False 
# freeze = False 


# def draw_points(x,y,colour):
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     glColor3f(colour[0],colour[1],colour[2])
#     glVertex2f(x,y)
#     glEnd()

# def update_point():
#     global ball_speed
#     for i in coordinate_arr:
#         if freeze==False: 
#                 #x boundary
#             if i['x']>=495 and i['x_direction']==True:  
#                 i['x_direction']=False  #direction siifted to lefrt
#             elif i['x']<=2 and i['x_direction']==False:             #these two only checks boundary hit or nah
#                 i['x_direction']=True  # direction revertetdd ti right
#             else:
#                 if i['x_direction']==True:  #within bouondary and actual movement(after appropriate direction adjustment)
#                     i['x']+=ball_speed*speed_x
#                 else:  
#                     i['x']-=ball_speed*speed_x

             

#             #y boundaryu
#             if i['y'] >= 495 and i['y_direction']==True:  # y same as x
#                 i['y_direction']=False 
#             elif i['y']<= 2 and i['y_direction']==False:  
#                 i['y_direction']=True 
#             else:           
#                 if i['y_direction'] :  
#                     i['y']+=ball_speed*speed_y
#                 else: 
#                     i['y']-=ball_speed*speed_y
#         else:  # freeze ccondiition
#             pass #doesnt change squat ie stays in same pos



# def mouseListener(button,state,x,y) :
#     global blink, freeze
#     if (freeze == False) : 
#         if (button==GLUT_RIGHT_BUTTON) and (state==GLUT_DOWN): 
#             print("point created")
#             coordinate_arr.append({'x': random.randrange(50,400,1),'y': random.randrange(50,450,1), 'colour':[random.random(),random.random(),random.random()],'x_direction':random.choice([True,False]),'y_direction':random.choice([True,False])})
        
#         if (button==GLUT_LEFT_BUTTON) and (state==GLUT_DOWN) and blink==False : 
#             blink = True 
#             print("Blink!")
#         elif (button==GLUT_LEFT_BUTTON) and (state==GLUT_DOWN) and blink==True: 
#             blink = False 
#             print("Blink off!")
#         glutPostRedisplay()


# def specialKeyListener(key,x,y) :
#     global ball_speed 
#     if (freeze==False) : 
#         if (key==GLUT_KEY_UP) :
#             ball_speed*=2 
#             print("Speed increased by",ball_speed)           
#         if (key==GLUT_KEY_DOWN) :
#             ball_speed/=2
#             print("Speed decreased by",ball_speed)
#     glutPostRedisplay()   

    

# def keyBoardListener(key,x,y) :
#     global freeze
#     if (key==b' ')  and freeze!=True:
#         print("Freeze initiated")
#         freeze=True
#     elif (key==b' ')  and freeze==True:
#         print("Unfreezing screen")
#         freeze=False

        
#     glutPostRedisplay()


# def animation(): 
#     global freeze 
#     if (freeze == False): 
#         update_point()
#     else:
#         pass 

#     glutPostRedisplay()
  

# def iterate():
#     glViewport(0, 0, 500, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()


# def showScreen():

#     glClearColor(0,0,0,0)
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()

#     for i in coordinate_arr : # setting x,y,colour for the draw_points from the coordinate_arr of points info 
#         x=i['x']
#         y=i['y']
#         if (blink==False) :
#             colour=i['colour']
#         else :
#             colour=[0.0,0.0,0.0]
        
#         draw_points(x,y,colour)

#     glutSwapBuffers()


# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(500, 500) #window size
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
# glutDisplayFunc(showScreen)
# glutMouseFunc(mouseListener)
# glutSpecialFunc(specialKeyListener)
# glutKeyboardFunc(keyBoardListener)
# glutIdleFunc(animation)
# glutMainLoop()