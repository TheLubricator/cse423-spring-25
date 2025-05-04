from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

# ----------------------- Global Variables ----------------------- #
# Camera variables
camera_pos = [0, 50, 20]
first_person = False  # False = third-person; True = first-person
camera_angle = 0 
# Game state variables
GRID_LENGTH = 600
fovY = 120

# Player variables
player_pos = [0.0, 0.0, 0.0]
gun_angle = 0.0
player_speed = 5

# Game status
player_life = 5
score = 0
bullets_missed = 0
game_over = False

# Mode toggles
cheat_mode = False
cheat_vision = False

# Bullets
bullets = []
BULLET_SPEED = 10

# Enemies
enemies = []
ENEMY_SPEED = 1.0
NUM_ENEMIES = 5

# ----------------------- Utility Functions ----------------------- #
def reset_game():
    global player_pos, gun_angle, player_life, score, bullets_missed, game_over, bullets, enemies
    player_pos = [0.0, 0.0, 0.0]
    gun_angle = 0.0
    player_life = 5
    score = 0
    bullets_missed = 0
    game_over = False
    bullets = []
    enemies = []
    for _ in range(NUM_ENEMIES):
        ex = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        ey = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        enemies.append({'pos': [ex, ey, 0], 'dir': 0})

reset_game()

# ----------------------- Drawing Functions ----------------------- #
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2] + 10)  # Lift the whole player

    # Draw green body (shorter)
    glPushMatrix()
    glScalef(1.0, 0.5, 1.5)  # Scale to rectangle shape
    glColor3f(0.0, 1.0, 0.0)  # Green
    glutSolidCube(30)
    glPopMatrix()

    # Draw black head (on top of body)
    glPushMatrix()
    glTranslatef(0, 0, 35)
    glColor3f(0.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

    # Left hand (perpendicular)
    glPushMatrix()
    glTranslatef(-25, 0, 15)
    glRotatef(90, 0, 1, 0)
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    gluCylinder(gluNewQuadric(), 3, 3, 20, 10, 10)
    glPopMatrix()

    # Right hand (perpendicular)
    glPushMatrix()
    glTranslatef(25, 0, 15)
    glRotatef(-90, 0, 1, 0)
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    gluCylinder(gluNewQuadric(), 3, 3, 20, 10, 10)
    glPopMatrix()

    # Left leg
    glPushMatrix()
    glTranslatef(-8, 0, -15)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(8, 0, -15)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    # Gun in the middle, pointing outward from chest
    glPushMatrix()
    glTranslatef(0, 20, 20)  # Between the arms
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.75, 0.75, 0.75)  # Silver
    gluCylinder(gluNewQuadric(), 3, 3, 40, 10, 10)
    glPopMatrix()

    glPopMatrix()



def draw_enemy(enemy):
    """Draws an enemy with a large red sphere (body) and a small black sphere (head) on top."""
    glPushMatrix()
    x, y, z = enemy['pos']
    glTranslatef(x, y, z)

    # Draw large red body sphere
    glColor3f(1.0, 0.0, 0.0)  # Red
    gluSphere(gluNewQuadric(), 20, 20, 20)

    # Draw smaller black head sphere above it
    glTranslatef(0, 0, 30)  # Lift upward to stack above the body
    glColor3f(0.0, 0.0, 0.0)  # Black
    gluSphere(gluNewQuadric(), 10, 20, 20)

    glPopMatrix()

def draw_bullet(bullet):
    glPushMatrix()
    glTranslatef(*bullet['pos'])
    glColor3f(1.0, 0.0, 0.0)  # Red color for the bullet
    glutSolidCube(10)
    glPopMatrix()


def draw_grid():
    step = 50
    # Draw the alternating grid blocks
    for x in range(-GRID_LENGTH, GRID_LENGTH, step):
        for y in range(-GRID_LENGTH, GRID_LENGTH, step):
            # Alternate between purple and white for each block
            if (x // step + y // step) % 2 == 0:
                glColor3f(0.5, 0, 0.5)  # Purple
            else:
                glColor3f(1, 1, 1)  # White
            
            # Draw a filled square for each block
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + step, y, 0)
            glVertex3f(x + step, y + step, 0)
            glVertex3f(x, y + step, 0)
            glEnd()

    # Draw the vertical boundary walls with different colors

    wall_height = 50  # Set the height of the walls
    wall_thickness = 10  # Set the thickness of the walls
    
    # Left wall (White)
    glColor3f(1, 1, 1)  # White
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH - wall_thickness, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH - wall_thickness, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()

    # Right wall (Dark Blue)
    glColor3f(0, 0, 0.5)  # Dark Blue
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH + wall_thickness, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH + wall_thickness, -GRID_LENGTH, wall_height)
    glEnd()

    # Front wall (Light Blue)
    glColor3f(0.678, 0.847, 0.902)  # Light Blue
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH + wall_thickness, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH + wall_thickness, wall_height)
    glEnd()

    # Back wall (Green)
    glColor3f(0, 1, 0)  # Green
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH - wall_thickness, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH - wall_thickness, wall_height)
    glEnd()





# ----------------------- Game Update Logic ----------------------- #
def update_bullets():
    global bullets, bullets_missed
    new_bullets = []
    for bullet in bullets:
        dx = BULLET_SPEED * math.cos(math.radians(bullet['angle']))
        dy = BULLET_SPEED * math.sin(math.radians(bullet['angle']))
        bullet['pos'][0] += dx
        bullet['pos'][1] += dy
        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][1]) > GRID_LENGTH:
            bullets_missed += 1
        else:
            new_bullets.append(bullet)
    bullets = new_bullets

def update_enemies():
    global enemies, score, player_life, game_over
    for enemy in enemies:
        ex, ey, _ = enemy['pos']
        dx, dy = player_pos[0] - ex, player_pos[1] - ey
        dist = math.hypot(dx, dy)
        if dist:
            enemy['pos'][0] += ENEMY_SPEED * (dx / dist)
            enemy['pos'][1] += ENEMY_SPEED * (dy / dist)
        if math.hypot(dx, dy) < 40:
            player_life -= 1
            enemy['pos'] = [random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50),
                            random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50), 0]
            if player_life <= 0:
                game_over = True
    for bullet in bullets[:]:
        for enemy in enemies:
            if math.hypot(bullet['pos'][0]-enemy['pos'][0], bullet['pos'][1]-enemy['pos'][1]) < 25:
                score += 1
                bullets.remove(bullet)
                enemy['pos'] = [random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50),
                                random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50), 0]
                break

def cheat_fire():
    global gun_angle
    gun_angle = (gun_angle + 5) % 360
    for enemy in enemies:
        dx = enemy['pos'][0] - player_pos[0]
        dy = enemy['pos'][1] - player_pos[1]
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        diff = abs((angle_to_enemy - gun_angle + 180) % 360 - 180)
        if diff < 10:
            fire_bullet()
            break

def fire_bullet():
    start_x = player_pos[0] + 25 + 40 * math.cos(math.radians(gun_angle))
    start_y = player_pos[1] + 40 * math.sin(math.radians(gun_angle))
    bullets.append({'pos': [start_x, start_y, 0], 'angle': gun_angle})

def update_game():
    if not game_over:
        update_bullets()
        update_enemies()
        if cheat_mode:
            cheat_fire()
    glutPostRedisplay()

# ----------------------- OpenGL Setup ----------------------- #
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if first_person:
        # First-person camera (gun-following view)
        eyeX, eyeY = player_pos[0], player_pos[1]
        eyeZ = 50
        centerX = eyeX + math.cos(math.radians(gun_angle)) * 100
        centerY = eyeY + math.sin(math.radians(gun_angle)) * 100
        centerZ = eyeZ
        gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, 0, 0, 1)
    else:
        # Third-person orbiting camera around center (0, 0)
        radius = 500
        eyeX = radius * math.cos(math.radians(camera_angle))
        eyeY = radius * math.sin(math.radians(camera_angle))
        eyeZ = camera_pos[2]  # Keep using current height
        gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, 0, 0, 1)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 1000, 800)
    setupCamera()

    draw_grid()
    for bullet in bullets:
        draw_bullet(bullet)
    for enemy in enemies:
        draw_enemy(enemy)
    draw_player()

    draw_text(10, 770, f"Score: {score}    Life: {player_life}    Bullets Missed: {bullets_missed}")
    if game_over:
        draw_text(400, 400, "GAME OVER! Press 'r' to restart.")
    glutSwapBuffers()

# ----------------------- Event Handlers ----------------------- #
def keyboardListener(key, x, y):
    global gun_angle, player_pos, cheat_mode, cheat_vision, game_over, player_speed
    if key == b'r':
        reset_game()
        player_speed = 5  # Reset speed after restarting
        return
    if game_over:
        return
    if key == b'w':
        # Move forward with increased speed
        player_pos[0] += player_speed * math.cos(math.radians(gun_angle))
        player_pos[1] += player_speed * math.sin(math.radians(gun_angle))
        player_speed += 0.1  # Gradually increase speed when moving forward
    elif key == b's':
        # Move backward with increased speed
        player_pos[0] -= player_speed * math.cos(math.radians(gun_angle))
        player_pos[1] -= player_speed * math.sin(math.radians(gun_angle))
        player_speed += 0.1  # Gradually increase speed when moving backward
    elif key == b'a':
        gun_angle = (gun_angle + 5) % 360
    elif key == b'd':
        gun_angle = (gun_angle - 5) % 360
    elif key == b'c':
        cheat_mode = not cheat_mode
    elif key == b'v':
        cheat_vision = not cheat_vision
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global camera_pos, camera_angle

    if key == GLUT_KEY_UP:
        camera_pos[2] += 10  # Move camera up
    elif key == GLUT_KEY_DOWN:
        camera_pos[2] -= 10  # Move camera down
    elif key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle + 5) % 360  # Orbit left
    elif key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle - 5) % 360  # Orbit right

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global first_person
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person  # Toggle view mode
    glutPostRedisplay()

def idle():
    update_game()

# ----------------------- Main Function ----------------------- #
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D OpenGL Game: Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()

"""
DESCRIPTION:
The player controls a gun that can move, rotate, and fire at enemies.
- Move forward: W key
- Move backward: S key
- Rotate left: A key
- Rotate right: D key
- Fire bullet: Left mouse button
- Toggle camera (1st/3rd person): Right mouse button
- Toggle cheat mode: C key (auto-aim & shoot)
- Restart game: R key
"""  