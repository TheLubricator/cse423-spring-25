from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
def my_draw():
    glPointSize(15) #pixel size. by default 1 thake
    glBegin(GL_QUADS)
    glColor3f(1,1,1)
    glVertex2f(-250,250)
    glVertex2f(250,250)
    glVertex2f(250,120)
    glVertex2f(-250,120) #jekhane show korbe pixel
    
    
   
    
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho( -250, 250, -250, 250, 0.0, 1.0)
    # xmin xmax y min y max zmin z max
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    r,b,g= 50,10,82
    glColor3f(r/255, g/255, b/255) #konokichur color set (RGB)
    #call the draw methods here
    draw_points(0, 251)
    my_draw()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()