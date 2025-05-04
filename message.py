from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time

screen_w, screen_h= 800,600


shooter_circle_w = screen_w // 2
bullet_x = shooter_circle_w
shoot_circle = False
bullet_y = 50
score=0
missed_shots = 0 
game_over=False
paused= False
falling_circles = []
falling_speed=0.05
falling_circle_speed = 3
last_falling_circle_time=0
max_falling_circles=random.randint(4,20)


def circle_points(x,y,cx,cy):
    glVertex2f(x+cx,y+cy)
    glVertex2f(y+cx,x+cy)
    
    glVertex2f(y+cx,-x+cy)
    glVertex2f(x+cx,-y+cy)
    
    glVertex2f(-x+cx,-y+cy)
    glVertex2f(-y+cx,-x+cy)
    
    glVertex2f(-y+cx,x+cy)
    glVertex2f(-x+cx,y+cy)


def midpoint_circle(cx,cy,radius):
    d=1-radius
    x=0
    y=radius
    circle_points(x,y,cx,cy)
    while x<y :
        if d<0:
            d=d+ 2*x +3
        else:
            d=d + 2 * x - 2 * y +5
            y=y-1
        x=x+1
        circle_points(x,y,cx,cy)

def circle_draw(cx, cy, radius):
    glBegin(GL_POINTS)
    midpoint_circle(cx, cy, radius)
    glEnd()




def shot_circle(x, y, radius):
    num_circles = 50
    colors = [(1.0, 0.2, 0.2), (1.0, 0.5, 0.0), (1.0, 0.8, 0.0), (1.0, 0.9, 0.0)] 
    for i in range(num_circles):
        glColor3f(*colors[i % len(colors)])  
        circle_draw(x, y + i * radius, radius // (i + 1))

def shooter_circle(cx, cy, radius):
    glColor3f(0.0, 0.0, 0.0)
    circle_draw(cx, cy, radius)


def create_falling_circles():
    global falling_circles, max_falling_circles, last_falling_circle_time, paused
    current_time = time.time()
    
    if paused:
        return
    
    if len(falling_circles) < max_falling_circles and current_time - last_falling_circle_time > 1:
        last_falling_circle_time = current_time
        new_circle = draw_falling_circle()
        min_gap = 10
        for circle in falling_circles:
            distance = ((new_circle['x'] - circle['x'])**2 + (new_circle['y'] - circle['y'])**2)**0.5
            if distance < (new_circle['radius'] + circle['radius'] + min_gap):
                return

        falling_circles.append(new_circle)


def update_circles():
    global score, falling_circles, last_falling_circle_time, falling_circle_speed, falling_speed, game_over, remaining_chances
    if not paused:
        current_time = time.time()
        if current_time - last_falling_circle_time > falling_circle_speed:
            last_falling_circle_time = current_time
            create_falling_circles()

        for circle in falling_circles:
            circle['y'] -= falling_speed
            if circle['y'] - circle['radius'] <= 0:
                game_over = True
                print("Game Over! A falling circle reached the bottom.")
                print(" Final Score is: ", score)
                glutLeaveMainLoop()
                break 

            if circle['y'] < 70 and circle['x'] >= shooter_circle_w - 20 and circle['x'] <= shooter_circle_w + 20:
                game_over = True
                print("Game Over! Falling circle touched the shot_circle circle.")
                print(" Final Score is: ", score)
                glutLeaveMainLoop()


def draw_falling_circle():
    global screen_w, screen_h
    radius = random.randint(10, 30)
    x_position = random.randint(radius, screen_w - radius) 
    return {'x': x_position, 'y': screen_h, 'radius': radius, 'shot': False}



def draw_falling_circles():
    global falling_circles
    glColor3f(1.0, 0.6, 0.0) 
    for circle in falling_circles:
        circle_draw(circle['x'], circle['y'], circle['radius'])


def draw_line(x1, y1, x2, y2):
    
    dx = x2 - x1
    dy = y2 - y1
    x = x1
    y = y1

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    x_increment = dx / float(steps)
    y_increment = dy / float(steps)
    
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)

    for i in range(int(steps)):
        x += x_increment
        y += y_increment
        glVertex2f(x, y)

    glEnd()


def restart_button():
    glColor3f(0.0, 1, 1)
    draw_line(10, screen_h - 30, 40, screen_h - 30)
    draw_line(10, screen_h - 30, 20, screen_h - 20)
    draw_line(10, screen_h - 30, 20, screen_h - 40)



def draw_pause_button():
    if paused:
        glColor3f(0.7, 0.7, 0.0)
        draw_line(screen_w // 2 - 5, screen_h - 20, screen_w // 2 - 5, screen_h - 50)
        draw_line(screen_w // 2 - 5, screen_h - 50, screen_w // 2 + 20, screen_h - 35)
        draw_line(screen_w // 2 - 5, screen_h - 20, screen_w // 2 + 20, screen_h - 35)

    else:
        glColor3f(0.7, 0.7, 0.0)
        draw_line(screen_w // 2 - 5, screen_h - 20, screen_w // 2 - 5, screen_h - 50)
        draw_line(screen_w // 2 + 5, screen_h - 20, screen_w // 2 + 5, screen_h - 50)


def draw_exit_button():
    glColor3f(1.0, 0.2, 0.2)
    draw_line(screen_w - 30, screen_h - 20, screen_w - 10, screen_h - 40)
    draw_line(screen_w - 30, screen_h - 40, screen_w - 10, screen_h - 20)

def collision_checker():
    global shoot_circle, bullet_y, falling_circles, score

    if shoot_circle:
        for circle in falling_circles:
            if (shooter_circle_w - circle['x'])**2 + (bullet_y - circle['y'])**2 <= (20 + circle['radius'])**2:
                falling_circles.remove(circle)
                shoot_circle = False 
                bullet_y = 50 
                score += 1 
                print("Score:", score)
                break 


def reset():
    global score, falling_speed, falling_circle_speed, falling_circles, missed_shots
    score = 0
    missed_shots = 0
    falling_speed = 0.1
    falling_circle_speed = 2  
    falling_circles = []

def drawSpaceship(shooter_circle_w):
    glColor3f(1.0, 0.6, 0.0)
    draw_line(shooter_circle_w-20, 40, shooter_circle_w+20, 40)
    draw_line(shooter_circle_w-5, 40, shooter_circle_w-5, 60)
    draw_line(shooter_circle_w+5, 40, shooter_circle_w+5, 60)
    draw_line(shooter_circle_w-5, 60, shooter_circle_w+5, 60)
    draw_line(shooter_circle_w-5, 60, shooter_circle_w, 70)
    draw_line(shooter_circle_w+5, 60, shooter_circle_w, 70)



def show_screen():
    global score, bullet_y, shoot_circle, bullet_x, missed_shots, game_over
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    restart_button()
    draw_pause_button()
    draw_exit_button()
    shooter_circle(shooter_circle_w, 50, 20)
    drawSpaceship(shooter_circle_w)
    
    if not paused:
        update_circles() 
        create_falling_circles()
        collision_checker()
        
        if shoot_circle:
            circle_draw(bullet_x, bullet_y, 10)  
            bullet_y += 5  

            if bullet_y >= screen_h:
                shoot_circle = False  
                missed_shots += 1  
                if missed_shots >= 3:
                    game_over = True
                    print("Game Over! Shot missed the target 3 times.")
                    print(" Final Score is: ", score)
                    glutLeaveMainLoop()  
    else:
        if shoot_circle:
            circle_draw(bullet_x, bullet_y, 10)

    draw_falling_circles()
    animate()

    glutSwapBuffers()


def keyboard_actions(key, x, y):
    global shooter_circle_w, shoot_circle, bullet_y, bullet_x, paused
    if key == GLUT_KEY_LEFT:
        shooter_circle_w = max(20, shooter_circle_w - 10) 
    elif key == GLUT_KEY_RIGHT:
        shooter_circle_w = min(screen_w - 20, shooter_circle_w + 10)  
    elif key == b' ':
        if not shoot_circle and not paused:
            shoot_circle = True
            bullet_y = 50 
            bullet_x = shooter_circle_w  

    glutPostRedisplay()


def mouse_clicks(button, state, x, y):
    global paused, score, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = screen_h - y
        if screen_w - 30 <= x <= screen_w and screen_h - 30 <= y <= screen_h:
            print("Goodbye!!! Your score:", int(score))
            glutLeaveMainLoop()
        elif screen_w // 2 - 25 <= x <= screen_w // 2 + 25 and screen_h - 50 <= y <= screen_h:
            if game_over == False:
                paused = not paused
        elif 0 <= x <= 50 and screen_h - 50 <= y <= screen_h:
            reset()
            print("Starting Over!")
            score = 0


def animate():
    glutPostRedisplay()

def initialize():
    global falling_circles, last_falling_circle_time, last_frame_time
    last_frame_time = time.time()
    falling_circles = []

    glViewport(0, 0, screen_w, screen_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, screen_w, 0.0, screen_h, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(screen_w, screen_h)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Circle shot_circle Game")

glutDisplayFunc(show_screen)
glutMouseFunc(mouse_clicks)
glutKeyboardFunc(keyboard_actions)
glutSpecialFunc(keyboard_actions)
glutIdleFunc(animate)
glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()

