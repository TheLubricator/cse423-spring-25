from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import numpy as np
import time

# Camera-related variables
camera_pos = [0,180,255]


first_person = False  # Flag for first-person view
fovY = 120  # Field of view
GRID_LENGTH = 299  # Length of grid lines (total size 299*2=598)
rand_var = 423
start_time = time.time()  # Record the start time for enemy fattening
enemy_pos=[]
player_rotation = 0
player_pos = [0, 0]
hits=0
player_life=5
boolet_pos = []  # Stores the current position of the boolet
boolet_direction = [] 
boolets_missed=0
game_end_flag=False
cheat_mode=False
last_fired_time = 0  # Initialize last fired time
cheat_vision=False  
radian_calc_for_cheat_vision=0
regular_condition=1
game_end_condition=0
left_arm_angle=-90
right_arm_angle=-90



def generate_enemy():
    global enemy_pos
    for i in range(5):
        enemy_pos.append({'enemy_posX':random.choice([random.randrange(-250, 100,10),random.randrange(100, 250,10)]), 'enemy_posY':random.choice([random.randrange(-250, 100,10),random.randrange(100, 250,10)])})
    enemy_pos=sorted(enemy_pos, key=lambda x: (x["enemy_posY"], x["enemy_posX"]))


def draw_grid():
    step=46
    for x in range(-GRID_LENGTH, GRID_LENGTH, step):
        for y in range(-GRID_LENGTH, GRID_LENGTH, step):
        
            if (x /step + y / step) % 2 == 0:
                glColor3f(1, 1, 1)  # Purple
            else:
                glColor3f(0.7, 0.5, 0.95)  # White
                
            

            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + step, y, 0)
            glVertex3f(x + step, y + step, 0)
            glVertex3f(x, y + step, 0)
            glEnd()

    

    wall_height = 50+15  # Set the height of the walls, 50 was too short for our player
    thickness = 3  # Set the thickness of the walls, 3 was creating gaps
    
   
    glColor3f(1, 1, 1)  
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH - thickness, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH - thickness, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()

    # Right wall (Dark Blue)
    glColor3f(0, 0, 0.5)  # Dark Blue
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH + thickness, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH +thickness, -GRID_LENGTH, wall_height)
    glEnd()

    # Front wall (Light Blue)
    glColor3f(0.678, 0.847, 0.902)  # Light Blue
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH + thickness, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH + thickness, wall_height)
    glEnd()

    # Back wall (Green)
    glColor3f(0, 1, 0)  # Green
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH - thickness, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH - thickness, wall_height)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """
    Draws 2D text on the screen at the specified (x, y) position.
    """
    glDisable(GL_DEPTH_TEST)  # Disable depth testing to ensure text is always on top
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection for 2D rendering
    gluOrtho2D(0, 625, 0, 500)  # Match the window dimensions

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Set text color and position
    glColor3f(1, 1, 1)  # White color for text
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore the original matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)  # Re-enable depth testing



def draw_player():
    global player_pos, player_rotation, regular_condition, game_end_condition
    global left_arm_angle, right_arm_angle  # Add global variables for arm angles

    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 30)
    glRotatef(player_rotation, 0, game_end_condition, regular_condition)  # Two conditions added to invert axis when player is dead

    # Body (cuboid)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(1.0, 0.5, 2.0)
    glColor3f(0.0, 1.0, 0.0)  # Green
    glutSolidCube(25)
    glPopMatrix()

    # Draw the left arm (move up and down based on left_arm_angle)
    glPushMatrix()
    glTranslatef(-18, 0, 40)
    glRotatef(left_arm_angle, 1, 0, 0)  # Rotate up and down
    glColor3f(1.0, 0.8, 0.6)
    gluCylinder(gluNewQuadric(), 3, 3, 30, 10, 10)
    glPopMatrix()

    # Draw the right arm (move up and down based on right_arm_angle)
    glPushMatrix()
    glTranslatef(18, 0, 40)
    glRotatef(right_arm_angle, 1, 0, 0)  # Rotate up and down
    glColor3f(1.0, 0.8, 0.6)
    gluCylinder(gluNewQuadric(), 3, 3, 30, 10, 10)
    glPopMatrix()

    glColor3f(0.0, 0.0, 1.0)  # Blue color for body

    # Left leg (vertical cylinder)
    glPushMatrix()
    glTranslatef(-8, 0, 5)  # Adjust Z to 5 to place above the grid
    glRotatef(-180, 1, 0, 0)  # Rotate to make it vertical
    glColor3f(0.0, 0.0, 1.0)  # Blue color for legs
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    # Right leg (vertical cylinder)
    glPushMatrix()
    glTranslatef(8, 0, 5)  # Adjust Z to 5 to place above the grid
    glRotatef(-180, 1, 0, 0)  # Rotate to make it vertical
    glColor3f(0.0, 0.0, 1.0)  # Blue color for legs
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    # Gun (positioned in the middle of the chest, pointing outward)
    glPushMatrix()
    glTranslatef(0, 35, 35)  # Position gun more centrally between arms
    glRotatef(90, 1, 0, 0)  # Adjust to align horizontally
    glColor3f(0.75, 0.75, 0.75)  # Silver color for the gun
    gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)  # Draw the gun
    glPopMatrix()

    # Draw the head (sphere on top of body)
    glPushMatrix()
    glTranslatef(0, 0, 50 + 10)  # Adjust head position based on body size
    glColor3f(0.0, 0.0, 0.0)  # Black color for the head
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

    glPopMatrix()  # End of player translation and drawing

def updateEnemy():
    global enemy_pos,player_pos,player_rotation,player_life,game_end_flag,regular_condition,game_end_condition,first_person
    for i in range(5):
        if enemy_pos[i]['enemy_posX']<player_pos[0]:
            enemy_pos[i]['enemy_posX']+=0.1
        elif enemy_pos[i]['enemy_posX']>player_pos[0]:
            enemy_pos[i]['enemy_posX']-=0.1
        if enemy_pos[i]['enemy_posY']<player_pos[1]:
            enemy_pos[i]['enemy_posY']+=0.1
        elif enemy_pos[i]['enemy_posY']>player_pos[1]:
            enemy_pos[i]['enemy_posY']-=0.1
        enemy_posX=int(enemy_pos[i]['enemy_posX'])
        enemy_posY=int(enemy_pos[i]['enemy_posY'])
       
                       
        if int(player_pos[0]//1) in range (enemy_posX-20,enemy_posX+20) and int(player_pos[1]//1) in range (enemy_posY-20,enemy_posY+20):

           
            player_life-=1
            if player_life<=0:
                game_end_flag=True
                regular_condition=0
                game_end_condition=1
                player_rotation=90
                first_person=False
            enemy_pos[i]['enemy_posX']=random.choice([random.randrange(-250, 100,10),random.randrange(100, 250,10)])
            enemy_pos[i]['enemy_posY']=random.choice([random.randrange(-250, 100,10),random.randrange(100, 250,10)])


# def cheat_fire():
#     global player_rotation, enemy_pos, player_pos, boolet_pos, boolet_direction, last_fired_time

   
#     cooldown = 0.4 

    
#     current_time = time.time()
#     if current_time - last_fired_time < cooldown:
#         return  #dont fire if within cooldown period

#     # Find the closest enemy within a certain angle range
#     closest_enemy = None
#     closest_diff = float('inf')  # Start with a very large difference

#     for enemy in enemy_pos:
#         dx = enemy['enemy_posX'] - player_pos[0]
#         dy = enemy['enemy_posY'] - player_pos[1]
#         angle_to_enemy = math.degrees(math.atan2(dy, dx))
#         angle_to_enemy = (angle_to_enemy + 360) % 360  
#         player_angle = (player_rotation + 360) % 360  #

#         diff = abs(angle_to_enemy - player_angle)
#         if diff > 180:  # Adjust for the shortest angle difference
#             diff = 360 - diff

#         # Check if the enemy is within the firing angle range (e.g., 20 degrees)
#         if diff < 15 and diff < closest_diff:
#             closest_enemy = enemy
#             closest_diff = diff

   
#     if closest_enemy:
#         # print(f"Firing at enemy with angle difference: {closest_diff}")
#         dx = closest_enemy['enemy_posX'] - player_pos[0]
#         dy = closest_enemy['enemy_posY'] - player_pos[1]
#         distance = math.sqrt(dx**2 + dy**2)

#         # Calculate the boolet's direction
#         boolet_direction.append([dx / distance, dy / distance])
#         boolet_pos.append([player_pos[0], player_pos[1], 70])  # boolet fired from player

#         # Update the last fired time
#         last_fired_time = current_time

def cheat_fire():
    global player_rotation, enemy_pos, player_pos, boolet_pos, boolet_direction, last_fired_time

    cooldown = 0.3  # Cooldown time in seconds, prevent multiple firings as i couldnt find a way to fire only once

    current_time = time.time()
    if current_time - last_fired_time < cooldown:
        return  # Don't fire if within cooldown period

    # Iterate through all enemies and fire at those within the angle range
    for enemy in enemy_pos:
        dx = enemy['enemy_posX'] - player_pos[0]
        dy = enemy['enemy_posY'] - player_pos[1]
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        angle_to_enemy = (angle_to_enemy + 360) % 360  
        player_angle = (player_rotation + 360) % 360  

        diff = abs(angle_to_enemy - player_angle)
        if diff > 180:  # keeping it less than 180 degrees
            diff = 360 - diff

      # range is within 15 degrees, also since in normal mode bullet hit box is 20+20 range range of enemy position
        if diff < 15:
            # Fire a bullet at this enemy
            dx = enemy['enemy_posX'] - player_pos[0]
            dy = enemy['enemy_posY'] - player_pos[1]
            distance = math.sqrt(dx**2 + dy**2)

            # Calculate the bullet's direction
            boolet_direction.append([dx / distance, dy / distance])
            boolet_pos.append([player_pos[0], player_pos[1], 70])  # Bullet fired from player

    # Update the last fired time
    last_fired_time = current_time




def fire_boolet():
    global boolet_pos, boolet_direction, player_pos, player_rotation

    
    boolet_pos.append([player_pos[0], player_pos[1], 70])  

  
    radians = math.radians(player_rotation)
    boolet_direction.append([math.sin(-radians), math.cos(-radians)])  


def draw_boolet():
    global boolet_pos, boolet_direction

    if len(boolet_pos)!=0:
        for i in range(len(boolet_pos)):
      # Only draw the boolet if it exists
            glPushMatrix()
            glTranslatef(boolet_pos[i][0], boolet_pos[i][1], boolet_pos[i][2])  # Use the boolet's position
            glColor3f(1, 0.0, 0.0)  # Red 
            glutSolidCube(8) #boolet as a solid cube
            glPopMatrix()



def draw_shapes():

    glPushMatrix()  # Save the current matrix state
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)  
    glutSolidCube(60) # Take cube size as the parameter
    glTranslatef(0, 0, 100) 
    glColor3f(0, 1, 0)
    glutSolidCube(37.5) 

    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 25, 3, 93.75, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glTranslatef(100, 0, 100) 
    glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 25, 3, 93.75, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 20, 20, 20) 
    #   # parameters are: quadric, radius, slices, stacks
    # glTranslatef(0, 0, 40)
    # gluSphere(gluNewQuadric(), 10, 20, 20) 

    glPopMatrix()  # Restore the previous matrix state
def draw_enemy(enemy_x,enemy_y,size):
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(enemy_x, enemy_y, 30) 
    gluSphere(gluNewQuadric(), size, 20, 20) 
      # parameters are: quadric, radius, slices, stacks
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 30)
    gluSphere(gluNewQuadric(), size/2, 20, 20) 

    glPopMatrix()  # Restore the previous matrix state



def keyboardListener(key, x, y):
    global player_pos,player_rotation,enemy_pos,player_life,game_end_flag,hits,boolets_missed,boolet_pos,boolet_direction,player_life,first_person,camera_pos,cheat_mode,cheat_vision,radian_calc_for_cheat_vision,radian_calc_for_cheat_vision,game_end_condition,regular_condition
    
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # Move forward (W key)
    if key == b'w' and game_end_flag==False:  # Move forward
        radians = math.radians(player_rotation)
        player_pos[0] += 10 * math.sin(-radians)
        player_pos[1] += 10 * math.cos(-radians)
        


    if key == b's' and game_end_flag==False:  # Move backward
        radians = math.radians(player_rotation)
        player_pos[0] -= 10 * math.sin(-radians)
        player_pos[1] -= 10 * math.cos(-radians)
        
    
    # Limit player within grid
    player_pos[0] = max(-279, min(279, player_pos[0]))
    player_pos[1] = max(-279, min(279, player_pos[1]))
    # print(player_pos[0]//1,player_pos[1]//1)
    for i in range(5):
        enemy_posX=int(enemy_pos[i]['enemy_posX'])
        enemy_posY=int(enemy_pos[i]['enemy_posY'])
       
                       
        if int(player_pos[0]//1) in range (enemy_posX-20,enemy_posX+20) and int(player_pos[1]//1) in range (enemy_posY-20,enemy_posY+20):

            print('hit')
            player_life-=1
            if player_life<=0:
                game_end_flag=True
            enemy_pos[i]['enemy_posX']=random.choice([random.randrange(-250, 100,10),random.randrange(100, 250,10)])
            enemy_pos[i]['enemy_posY']=random.choice([random.randrange(-250, 100,10),random.randrange(100, 250,10)])


    if key == b'a' and game_end_flag==False and cheat_mode==False:  # Rotate left
        player_rotation += 10

    if key == b'd' and game_end_flag==False and cheat_mode==False:  # Rotate right
        player_rotation -= 10

    # # Toggle cheat mode (C key)
    if key == b'c':
        if cheat_mode:
            cheat_mode=False
            if cheat_vision:
                cheat_vision=False
                
        else:
            cheat_mode=True
            print('cheat mode on')

    # # Toggle cheat vision (V key)
    if key == b'v' and cheat_mode:
        if cheat_mode and not game_end_flag and first_person:
            cheat_vision = not cheat_vision  # Toggle cheat vision
            radian_calc_for_cheat_vision = player_rotation  # keeping angle of player without spinning 

    # # Reset the game if R key is pressed
    if key == b'r':
     
        player_pos = [0, 0]
        player_rotation = 0
       
        boolet_pos.clear()
        boolet_direction.clear()
        enemy_pos.clear()
      
        generate_enemy()
      
        hits = 0
        boolets_missed = 0
        player_life = 5
        game_end_flag = False
        cheat_mode = False  # Reset cheat mode
        first_person = False  # Reset camera mode
        cheat_vision = False
        radian_calc_for_cheat_vision = 0  # Reset cheat vision angle
        camera_pos = [0, 180, 255]
        game_end_condition=0
        regular_condition=1
        



def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos,left_arm_angle,right_arm_angle
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        if left_arm_angle<-5:
            left_arm_angle += 5
            print(left_arm_angle)

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        if left_arm_angle>-95:
            left_arm_angle-=5
            print(left_arm_angle)

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global camera_pos,first_person,cheat_mode,cheat_vision
    """
    Handles mouse inputs for firing boolets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a boolet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_boolet()

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print('yes',cheat_mode,cheat_vision)
        if first_person:
           first_person = False
           if cheat_vision:
                cheat_vision = False
                
        else:
            first_person = True
        print(first_person)

    
            
            


def setupCamera():
    global first_person,player_rotation,cheat_vision,cheat_mode,radian_calc_for_cheat_vision

    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(fovY, 1.25, 0.1, 1500)  
    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()  

    if first_person and not cheat_vision and not cheat_mode:
        # Eye (camera) position on head
        eyeX = player_pos[0]
        eyeY = player_pos[1]
        eyeZ = 70+24+13  # Near head

        # Calculate where to look based on rotation
        distance = 100  # how far to look forward
        rad = math.radians(player_rotation)
        targetX = eyeX + math.sin(-rad) * distance
        targetY = eyeY + math.cos(-rad) * distance
        targetZ = eyeZ  # Same Z (horizontal view)

        gluLookAt(eyeX, eyeY, eyeZ,
                  targetX, targetY, targetZ,
                  0, 0, 1)
    elif first_person and cheat_mode and not cheat_vision:
        eyeX = player_pos[0]-10  # Fixed X position
        eyeY = player_pos[1]-10 # Fixed Y position
        eyeZ = 70 + 27+10  # z position above head

       
        distance = 100  # how far to look forward
        rad = math.radians(radian_calc_for_cheat_vision) # keeping the angle of player without spinning
        targetX = eyeX + math.sin(-rad) * distance
        targetY = eyeY + math.cos(-rad) * distance
        targetZ = eyeZ  # Same Z (horizontal view)

        # Ensure the camera is looking in the player's direction
        gluLookAt(eyeX, eyeY, eyeZ,
                  targetX, targetY, targetZ,
                  0, 0, 1)
    elif first_person and cheat_mode and cheat_vision:
        # Eye (camera) position on head
        eyeX = player_pos[0]
        eyeY = player_pos[1]
        eyeZ = 70+24+13  # Near head

        # Calculate where to look based on rotation
        distance = 100  # how far to look forward
        rad = math.radians(player_rotation)
        targetX = eyeX + math.sin(-rad) * distance
        targetY = eyeY + math.cos(-rad) * distance
        targetZ = eyeZ  # Same Z (horizontal view)

        gluLookAt(eyeX, eyeY, eyeZ,
                  targetX, targetY, targetZ,
                  0, 0, 1)


    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z,
                  0, 0, 0,
                  0, 0, 1)



def idle():
    """
    Idle function that runs continuously:
    - Updates the player's rotation for cheat mode.
    - Updates boolet positions and checks for collisions.
    - Triggers screen redraw for real-time updates.
    """
    global boolet_pos, boolet_direction, boolets_missed, hits, enemy_pos, player_pos, player_rotation, player_life, game_end_flag, cheat_mode,regular_condition,game_end_condition,first_person

    # Rotate the player and fire boolets in cheat mode
    if cheat_mode and not game_end_flag:
        player_rotation = (player_rotation + 2) % 360  # Increment rotation and keep it within 0-360 degrees
        cheat_fire()  # Automatically fire boolets at enemies

    # Update the boolet's position if it exists
    if not game_end_flag:
        if len(boolet_pos) != 0:
            boolet_speed = 2  # Speed of the boolet

            # Iterate over the boolets in reverse order to avoid index shifting issues
            for i in range(len(boolet_pos) - 1, -1, -1):
                boolet_pos[i][0] += boolet_direction[i][0] * boolet_speed  # Update x position
                boolet_pos[i][1] += boolet_direction[i][1] * boolet_speed  # Update y position

                # Check for collisions with enemies
                for j in range(len(enemy_pos)):
                    enemy_posX = int(enemy_pos[j]['enemy_posX'])
                    enemy_posY = int(enemy_pos[j]['enemy_posY'])

                    if (
                        len(boolet_pos) != 0
                        and int(boolet_pos[i][0] // 1) in range(enemy_posX - 20, enemy_posX + 20)
                        and int(boolet_pos[i][1] // 1) in range(enemy_posY - 20, enemy_posY + 20)
                    ):
                        hits += 1
                        enemy_pos[j]['enemy_posX'] = random.choice(
                            [random.randrange(-250, 100, 10), random.randrange(100, 250, 10)]
                        )
                        enemy_pos[j]['enemy_posY'] = random.choice(
                            [random.randrange(-250, 100, 10), random.randrange(100, 250, 10)]
                        )
                        del boolet_pos[i]
                        del boolet_direction[i]
                        break  # Exit the inner loop to avoid further processing of the deleted boolet

                # Remove the boolet if it goes out of bounds
                for i in range(len(boolet_pos) - 1, -1, -1):
    # Check if the boolet is out of bounds
                    if abs(boolet_pos[i][0]) > GRID_LENGTH - 10 or abs(boolet_pos[i][1]) > GRID_LENGTH - 10:
                        del boolet_pos[i]  # Remove the boolet
                        del boolet_direction[i]  # Remove the corresponding direction
                        boolets_missed += 1  # Increment the missed boolets counter
                        if boolets_missed >= 10:
                            game_end_flag = True
                            regular_condition=0
                            game_end_condition=1
                            player_rotation=90
                            first_person=False


        # Update enemy positions
        # updateEnemy()

    # Ensure the screen updates with the latest changes
    glutPostRedisplay()

def showScreen():
    global pulse,enemy_pos,first_person,camera_pos,player_pos,player_life
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 625, 500)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    draw_grid()
   
    

    # Display game info text at a fixed screen position
    if not first_person and game_end_flag==False:
        draw_text(10, 470, f"Game Score: {hits}")
        draw_text(10, 440, f"Life left: {player_life}")
        draw_text(10, 410, f"boolets Missed: {boolets_missed}")
    elif first_person and game_end_flag==False:
        draw_text(10, 470, f"Game Score: {hits}")
        draw_text(10, 440, f"Life left: {player_life}")
        draw_text(10, 410, f"boolets Missed: {boolets_missed}")
    if game_end_flag:
        draw_text(10, 470, f"Game Over")
        draw_text(10, 440, f"Final Score: {hits}")
        draw_text(10, 410, f"boolets Missed: {boolets_missed}")
        draw_text(10, 380, f"Press R to Restart")
        

    # draw_shapes()
    current_time = (time.time() - start_time)*10  # Get elapsed time
    enemy_size = (np.sin(current_time) + 1) / 2 * (30 - 25) + 25  # Oscillate between 25 and 30


    # Draw the enemy with the calculated size
    for key in enemy_pos:
        enemy_posX=key['enemy_posX']
        enemy_posY=key['enemy_posY']
        draw_enemy(enemy_posX,enemy_posY,enemy_size)
    draw_player()
    draw_boolet()

    
        


    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(625, 500)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    
    generate_enemy()  # Generate enemies, initially
    print(enemy_pos)
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the boolet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
