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
def colorAlternator():
    global alternator_stat
    alternator_stat=True
    return (179/255, 174/255, 170/255)



def draw_raindrop(x, y):
    global alternator_stat
    glBegin(GL_LINES)
    if alternator_stat==True:
        glColor3f(0, 0, 1)  # Blue color for raindrops
        alternator_stat=False
    else:
        grey=colorAlternator()  #alternate to grey color like demo
        glColor3f(grey[0], grey[1], grey[2])
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
