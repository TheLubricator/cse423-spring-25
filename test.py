from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_12
import numpy as np
import time

# import pygame
# pygame.mixer.init()

# pygame.mixer.music.load('Shin Megami Tensei Nocturne & Imagine - Metatron\'s Theme (Dual Mix).mp3')
# pygame.mixer.music.play(-1)
GRID_RADIUS = 300  # Radius of the grid
STEP = 15  # Step between grid points
# Camera-related variables
camera_pos = [0,180,255]

cheat_vision=False
cheat_mode=False
first_person = True  # Flag for first-person view
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
regular_condition=1
game_end_condition=0
left_arm_angle=-90
right_arm_angle=-90
sword_angle=-20
enemy_position = (0, 0)
last_action=''
def limit_fps(target_fps):
  
    start_time = time.time()

    end_time = time.time()
    frame_time = end_time - start_time
    target_frame_time = 1 / target_fps  # Convert target 
    if frame_time < target_frame_time:
        time.sleep(target_frame_time - frame_time)

class Player:
    def __init__(self,x,y,hp,mp,attack_power,defensne_power,magic_power):
        self.guarding=False
        
        self.name=''
        self.player_hp=hp
        self.player_mp=mp
        self.og_hp=hp
        
        self.stats={'attack':attack_power,'defense':defensne_power,'magic':magic_power}
        self.buff_debuff=[0,0,0]

     
        self.shirt_color=(random.random(), random.random(), random.random())
        self.position = [x, y]
        self.rotation = -180
        self.life = 5
        self.left_arm_angle = -90
        self.right_arm_angle = -90
        self.action_execution_mode=False
        self.magic_execution_mode=False
        
        self.support_execution_mode=False
        self.support_state=5
        self.innermenu_active=False
        self.camera_x=self.position[0]
        self.camera_y=self.position[1]
        self.camera_rotation=self.rotation
        self.skill1=None
        self.skill2=None
        self.skill3=None
        self.original_position = [x, y]
        self.original_rotation = self.rotation
        self.alive_status=True
    def move(self, direction, distance):
        radians = math.radians(self.rotation)
        if direction == "forward":
            self.position[0] += distance * math.sin(-radians)
            self.position[1] += distance * math.cos(-radians)
        elif direction == "backward":
            self.position[0] -= distance * math.sin(-radians)
            self.position[1] -= distance * math.cos(-radians)
        self.position[0] = max(-279, min(279, self.position[0]))
        self.position[1] = max(-279, min(279, self.position[1]))

    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360

    def rotate_to_enemy(self, enemy_position):
        target_x, target_y = enemy_position
        delta_x = target_x - self.position[0]
        delta_y = target_y - self.position[1]

        # Calculate the angle from self to the enemy (no negative sign!)
        if self.position[0]<0:
            target_angle = math.degrees(math.atan2(delta_y, delta_x)-50) % 360
        else:
            target_angle = -math.degrees(math.atan2(delta_y, delta_x)) % 360

        # Compute shortest angle difference in range [-180, 180]
        angle_diff = (target_angle - self.rotation + 540) % 360 - 180

        # Rotate smoothly toward enemy
        if abs(angle_diff) > 1:
            rotation_step = angle_diff / 10  # smoothness factor
            self.rotation = (self.rotation + rotation_step) % 360
        else:
            self.rotation = target_angle  # Snap to target when close enough



    def move_towards_enemy(self, enemy_position, step_size, min_distance=50):
        target_x, target_y = enemy_position
        delta_x = target_x - self.position[0]
        delta_y = target_y - self.position[1]
        distance_to_target = math.hypot(delta_x, delta_y)  # Calculate the total distance to the target

        # If the player is not yet at the target and is further than the minimum distance, move towards it in steps
        if distance_to_target > min_distance:  # Only move if we are not too close to the target
            # Calculate direction towards the enemy
            angle_to_enemy = math.atan2(delta_y, delta_x)
            
            # Move in small steps along the direction
            step_x = step_size * math.cos(angle_to_enemy)
            step_y = step_size * math.sin(angle_to_enemy)

            # Update the position by a small step towards the enemy
            self.position[0] += step_x
            self.position[1] += step_y
        else:
            # If we are within the minimum distance, stop moving and adjust the position to stay at min_distance
            angle_to_enemy = math.atan2(delta_y, delta_x)  # Recalculate the angle once more
            self.position[0] = target_x - min_distance * math.cos(angle_to_enemy)
            self.position[1] = target_y - min_distance * math.sin(angle_to_enemy)



    def raise_right_arm(self):
     
        if self.right_arm_angle<=-24:
            self.right_arm_angle += 2  # Slowly raise the arm by 1 degree
    def lower_right_arm(self):
        if self.right_arm_angle > -90:
            self.right_arm_angle -= 2  # Slowly raise the arm by 1 degree

    def reset_position(self):
        self.position = self.original_position[:]
        self.rotation = self.original_rotation
    def perform_action_support(self, skill):
       
        if self.support_execution_mode and not self.magic_execution_mode and not self.action_execution_mode:
           
            return  # If already performing an action, ignore other inputs
        self.support_execution_mode = True
        self.support_state = 0  # Reset support state to 0 for a new action
        self.skill = skill
       
            

        
    def perform_action_phys(self, skill='regular attack'):
        if self.action_execution_mode and not self.magic_execution_mode:
            return  # If already performing an action, ignore other inputs

        self.action_execution_mode = True
        self.action_state = 0  # Start action sequence
        self.skill_trigger=skill
    def perform_action_mag(self, skill=''):
        if self.magic_execution_mode and not self.action_execution_mode :
            return  # If already performing an action, ignore other inputs
       

        self.magic_execution_mode = True
        self.magic_state = 0  # Start action sequence
        skills=[self.skill1,self.skill2,self.skill3]
        self.total_skill=skills[skill-1]
        if skill=='':
            self.skill_trigger=skill
        else:
            self.total_skill=skills[skill-1]
            self.type=self.total_skill[2]
            
            self.skill_trigger=self.type.split('_')[1]
    def update_mag(self, enemy_position):
        global last_action,boolet_pos
        if self.magic_execution_mode:
            if self.magic_state == 0:  # Step 1: Rotate towards the enemy
                self.rotate_to_enemy(enemy_position)

    
                
                if abs(self.rotation - math.degrees(math.atan2(enemy_position[1] - self.position[1], enemy_position[0] - self.position[0]))) <= 287:
           
                    self.magic_state = 1  # Move to next step

            elif self.magic_state == 1:
                print('fired')
                if self.skill_trigger=='electricity':
                    self.fire_boolet([1,1,0],'electricity')  # Fire after rotation
                elif self.skill_trigger=='ice':
                    self.fire_boolet([135/256,206/256,235/256],'ice')
                # elif self.skill_trigger=='fire':
                #     self.fire_boolet([1,0,0])
                print(boolet_pos)
                self.action_execution_mode = False
                self.action_state = 5
                self.magic_state = 2  # End of magic action
                print(self.magic_state)
            elif self.magic_state == 2:  # Step 3: End action
                self.reset_position()
                self.magic_execution_mode = False
                self.magic_state = 5  # Reset for next time
                self.action_state = 5  # Optional marker
                print(self.total_skill)
                self.use_magic(self.total_skill)

                # if self.skill_trigger=='regular attack':
                #     self.regular_attack()
                next_player()
    def update_support(self):
        
        if self.support_execution_mode:
         
            if self.support_state == 0:
              
                self.raise_right_arm()
                if self.right_arm_angle >= -24:
        
                    self.support_state = 1  # Move to next step
            elif self.support_state == 1:
            
                self.lower_right_arm()
                if self.right_arm_angle <= -90:
          
                    self.support_state = 2  # Final step
            elif self.support_state == 2:
               
                skills = [self.skill1, self.skill2, self.skill3]
                self.use_support_skill(skills[self.skill - 1])
                self.support_execution_mode = False  # End the action
                self.support_state = 5  # Set state to 5 to indicate that the action is complete
                next_player()

                          
    
    def use_support_skill(self,skill):
        global last_action
        fail=False
        if skill[7]=='team':
           
            teammates=[p1,p2,p3,p4]
            if  self.player_mp>= skill[4]:
                self.player_mp-=skill[4]
                for team in teammates:
                    if skill[5]=='attack':
                        if team.buff_debuff[0]!=3:
                            
                            team.buff_debuff[0]+=skill[6]
                        else:
                            fail=True
                            last_action=f'Attack already at max rank'
                    elif skill[5]=='defense':
                        if team.buff_debuff[1]!=3:
                            team.buff_debuff[1]+=skill[6]
                        else:
                            fail=True
                            last_action=f'Defense already at max rank'
                    elif skill[5]=='magic':
                        if team.buff_debuff[2]!=3:
                            team.buff_debuff[2]+=skill[6]
                        else:
                            fail=True
                            last_action=f'Magic already at max rank'

                    print(team.buff_debuff)
                if not fail:
                    last_action=f'{skill[5].upper()} of all allies raised by one'
                else:
                    last_action=f'{skill[5].upper()} already at max rank'
            else:
                last_action=f'Insufficient MP'
        elif skill[7]=='enemy':
             if  self.player_mp>= skill[4]:
                self.player_mp-=skill[4]
                
                if skill[5]=='attack':
                    if enemy.buff_debuff[0]!=-3:
                        
                        enemy.buff_debuff[0]+=skill[6]
                    else:
                        fail=True
                        
                elif skill[5]=='defense':
                    if enemy.buff_debuff[1]!=-3:
                        enemy.buff_debuff[1]+=skill[6]
                    else:
                        fail=True
                      
                elif skill[5]=='magic':
                    if enemy.buff_debuff[2]!=3:
                        enemy.buff_debuff[2]+=skill[6]
                    else:
                        fail=True
                        

                print(enemy.buff_debuff)
                if not fail:
                    last_action=f'{skill[5].upper()} of enemy decreased by one'
                else:
                    last_action=f'Enemy {skill[5].upper()} already at minimum rank'
        elif skill[7]=='heal':
             if  self.player_mp>= skill[4]:
                self.player_mp-=skill[4]
                teammates=[p1,p2,p3,p4]
                for team in teammates:
                    team.player_hp+=int(team.og_hp*0.38)
                    if team.player_hp>team.og_hp:
                        team.player_hp=team.og_hp
                    print(team.player_hp)
                
                
                        

                
                
                last_action=f'All players healed 38 percent of their original hp'

        



    def fire_boolet(self,color,shape):
        global boolet_pos, boolet_direction

    # Spawn the bullet at the player's current position and height
        boolet_pos.append([self.position[0], self.position[1], 70,color,shape])

        # Calculate the forward direction based on current rotation
        radians = math.radians(self.rotation)
        dx = math.sin(-radians)
        dy = math.cos(-radians)

    # Store the bullet's direction
        boolet_direction.append([dx, dy])
    def update_phys(self, enemy_position):
        global last_action
        if self.action_execution_mode:
            if self.action_state == 0:  # Step 1: Rotate towards the enemy
                self.rotate_to_enemy(enemy_position)
                # Check if rotation is close enough to stop
                
                if abs(self.rotation - math.degrees(math.atan2(enemy_position[1] - self.position[1], enemy_position[0] - self.position[0]))) <= 287:
                    self.action_state = 1  # Move to next step
            elif self.action_state == 1:  # Step 2: Move towards the enemy
                self.move_towards_enemy(enemy_position, 10)
            
                if math.hypot(self.position[0] - enemy_position[0], self.position[1] - enemy_position[1]) <= 50:
                    self.action_state = 2
                    print(f'first {self.right_arm_angle}')  # Move to next step
            elif self.action_state == 2:  # Step 3: Raise right arm
                self.raise_right_arm()
                if self.right_arm_angle >= -24:
                    self.action_state = 3  # Move to next step

            elif self.action_state == 3:  # Step 4: Lower right arm
                self.lower_right_arm()
                if self.right_arm_angle <= -90:
                    self.action_state = 4  # Final step

            elif self.action_state == 4:  # Step 4: Return to starting position and rotation
                self.reset_position()
                self.action_execution_mode = False  # End the action
                self.action_state = 5  # Mark that action is completely done
                print(self.skill_trigger)
                if self.skill_trigger=='regular attack':
                    self.regular_attack()
                else:
                    skills=[self.skill1,self.skill2,self.skill3]
                    self.skill_phys_attack(skills[self.skill_trigger-1])
                next_player()
    def random_chance(self,chance: float):
        return random.random() < chance        
    def regular_attack(self):
        global last_action
        
        will_it_crit=self.random_chance(0.3)
        base_power = 40
        
        variance = random.uniform(0.85, 1.1)
        if not will_it_crit:

            damage = round(max(1, int((self.stats['attack'] * base_power) / ((enemy.stats['defense']*(1+(enemy.buff_debuff[1]/8))) + 1)))*variance*(1+(self.buff_debuff[0]/8)))
            enemy.hp-=damage
        
            last_action=f'{self.name} dealt damage {damage} using regular swing'
        else:
            damage = round(max(1, int((self.stats['attack'] * base_power) / ((enemy.stats['defense']*(1+(enemy.buff_debuff[1]/8)))+ 1)))*variance*2*(1+(self.buff_debuff[0]/8)))
            enemy.hp-=damage
        
            last_action=f'Critical strike! {self.name} dealt damage {damage} using regular swing'


    def skill_phys_attack(self,skill):
        global last_action
        will_it_hit=self.random_chance(skill[5])
        will_it_crit=self.random_chance(skill[6])
        element=None
        extra_text=''
        if will_it_hit:
            self.player_mp-=skill[4]
            
            base_power=skill[3]
            if skill[2]!='physical':
                element=skill[2].split('_')[1]
                
            if element==None:
                resistance=enemy.resistance['physical'] 
            else:
                resistance=enemy.resistance[element]
           
            variance = random.uniform(0.85, 1.0)
            if element!=None and enemy.resistance[element]>1:
                    extra_text+=' Enemy Weakness hit!'
            if will_it_crit:

                damage = round(max(1, int((self.stats['attack']* base_power) / ((enemy.stats['defense']*(1+(enemy.buff_debuff[1]/8))) + 1)))*variance*1.5*resistance*(1+(self.buff_debuff[0]/8)))
                enemy.hp-=damage
            
                last_action=f'Critical hit! {self.name} dealt damage {damage} using {skill[0]}.{extra_text}'
                
            else:
                damage = round(max(1, int((self.stats['attack'] * base_power) / ((enemy.stats['defense']*(1+(enemy.buff_debuff[1]/8))) + 1)))*variance*1*resistance*(1+(self.buff_debuff[0]/8)))
                enemy.hp-=damage
                last_action=f'{self.name} dealt damage {damage} using {skill[0]}.{extra_text}'
                
        else:
            last_action=f'{self.name} missed the target!'
    def use_magic(self,skill):
        global last_action
        enemy_resistance=enemy.resistance[self.skill_trigger]
        if self.player_mp>=skill[4]:
            self.player_mp-=skill[4]
            variance = random.uniform(0.85, 1.0)
            base_power=skill[3]
            
            damage = round(max(1, int((self.stats['magic'] * base_power) / ((enemy.stats['defense']*(1+(enemy.buff_debuff[1]/8))) + 1)))*variance*1.5*enemy_resistance*(1+(self.buff_debuff[2]/8)))
            enemy.hp-=damage
            if enemy_resistance>1:
                last_action=f'Weakness hit! {self.name} dealt damage {damage} using {skill[0]}.'
            else:
                last_action=f'{self.name} dealt damage {damage} using {skill[0]}.'
        else:
            last_action=f'Insufficient MP.'


            



    def draw(self):
        global game_end_condition,regular_condition
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 30)
        glRotatef(self.rotation, 0, game_end_condition, regular_condition)  # Two conditions added to invert axis when player is dead

        # Body (cuboid)
        glPushMatrix()
        glTranslatef(0, 0, 25)
        glScalef(1.0, 0.5, 2.0)
        glColor3f(self.shirt_color[0],self.shirt_color[1],self.shirt_color[2])  
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
        glRotatef(self.right_arm_angle, 1, 0, 0)  # Rotate up and down
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
p1=Player(175,150,400,10,65,50,15)
p2=Player(58.33,150,350,55,20,55,50)
p3=Player(-58.33,150,300,60,40,77,32)
p4=Player(-175,150,275,75,10,57,66)

p1.name='Player 1'
p2.name='Player 2'
p3.name='Player 3'
p4.name='Player 4'

p1.skill1 = ['Figment Slash', '50 p accuracy, but always critical','physical', 250, 4, 0.5,1]
p1.skill2 = ['Akashic Arts','heavy phys attack', 'physical', 210, 5, 0.96,0.21]
p1.skill3 = ['Tarukaja', 'Attack up by one rank','support',0,10,'attack',1,'team']

p2.skill1 = ['Bufudyne','heavy Ice Damage to one foe', 'magic_ice', 100, 10, 1]
p2.skill2 = ['Ziodyne','heavy electric damage' ,'magic_electricity',100, 10, 1]
p2.skill3 = ['Rakukaja', 'Defense up by one rank','support',0,10,'defense',1,'team'] 


p3.skill1 = ['Ice Dracostrike','ice-based physcial attack' ,'physical_ice',60,6,0.98,0.21]
p3.skill2 =['Makakaja','magic up by one rank', 'support',0,10,'magic',1,'team'] 
p3.skill3 = ['Rakunda','Downs enemy defense by one','support',0,10,'defense',-1,'enemy']

p4.skill1 = ['Mediarama', 'medium recovery to all','support', 0, 10,0,0,'heal']
p4.skill2 = ['Mudoon','heavy ddark attack', 'physical', 0, 7, 0,0]
p4.skill3 = ['Tarukaja','Attack up by one rank', 'support',0,10,'attack',1,'team']


players_class_list=[p1,p2,p3,p4]
turn_order=[p1,p2,p3,p4]
current_player=0


def next_player():

    global current_player,turn_order
    current_player = (current_player + 1) % len(turn_order)
    if isinstance(turn_order[current_player],Player):
        if turn_order[current_player].guarding==True:
            print('guard down')
            turn_order[current_player].guarding=False
            turn_order[current_player].stats['defense']-=60
       

    print(f"Current Player: {current_player}")


def update_boolets():
    global boolet_pos, boolet_direction

    if boolet_pos:
        speed = 5
        # Move the single bullet
        boolet_pos[0][0] += boolet_direction[0][0] * speed
        boolet_pos[0][1] += boolet_direction[0][1] * speed

        # Remove if it crosses x <= 0 or y <= 0
        if boolet_pos[0][1] <= 0:
            boolet_pos.clear()
            boolet_direction.clear()

        


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

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12,color=[1,1,1]):
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
    glColor3f(color[0], color[1], color[2])  # White color for text
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore the original matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)  # Re-enable depth testing










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

    
    boolet_pos.append([p1.position[0], p1.position[1], 70])  

  
    radians = math.radians(p1.rotation)
    boolet_direction.append([math.sin(-radians), math.cos(-radians)])  


def draw_boolet():
    global boolet_pos, boolet_direction

    if len(boolet_pos)!=0:
        for i in range(len(boolet_pos)):
      # Only draw the boolet if it exists
           
            glPushMatrix()
            glTranslatef(boolet_pos[i][0], boolet_pos[i][1], boolet_pos[i][2])  # Use the boolet's position
            glColor3f(boolet_pos[i][3][0], boolet_pos[i][3][1], boolet_pos[i][3][2])  # Red 
            if boolet_pos[i][4]=='ice':
                glutSolidCube(20) #boolet as a solid cube
            elif boolet_pos[i][4]=='electricity':
                glPushMatrix()  # Save the current transformation matrix
                glRotatef(-90, 1,0, 0)  # Rotate 90 degrees around the Y-axis to make it lie along the X-axis
                
                # Draw the cylinder
                gluCylinder(gluNewQuadric(), 15, 15, 40, 10, 10)
                
                glPopMatrix()  # Restore the transformation matrix

            glPopMatrix()



# def draw_shapes():
#     global sword_angle
#     glPushMatrix()
#     glTranslatef(100, 0, 30)
#     # === TORSO ===
#     glColor3f(0.6, 0.6, 0.6)  # Steel gray
#     glPushMatrix()
#     glTranslatef(0, 0, 90)
#     glScalef(1, 0.5, 2)  # Wider chest
#     glutSolidCube(60)
#     glPopMatrix()

#     # === HEAD ===
#     glColor3f(1, 1, 1)  # White
#     glPushMatrix()
#     glTranslatef(0, 0, 160)
#     glutSolidCube(30)
#     glPopMatrix()

#     # === EYES ===
#     glColor3f(1, 0, 0)  # Red eyes
#     glPushMatrix()
#     glTranslatef(-8, 15, 160)
#     glutSolidSphere(3, 10, 10)
#     glTranslatef(16, 0, 0)
#     glutSolidSphere(3, 10, 10)
#     glPopMatrix()

#     # === RIGHT ARM === (separate and raised 90 degrees)
#     glColor3f(0.4, 0.4, 0.4)  # Right arm
#     glPushMatrix()
#     glTranslatef(50, 0, 90)  # Start from right shoulder
#     glRotatef(-5,0, 0, 1)  # Raise arm upwards by 90 degrees

#     # The right hand (palm facing upwards)
#     glPushMatrix()
#     glTranslatef(0, 0, 40)
#     glRotatef(190,0, 0, 1)  # Positioning the hand in a palm-up position
#     glScalef(0.7, 0.7, 0.7)  # Slightly scaled for hand size
#     glutSolidCube(20)  # Hand
#     glPopMatrix()

#     # Sword in the palm of the right hand
#     glColor3f(1,0 , 0)  # Yellow blade color
#     glPushMatrix()
#     glTranslatef(0, 0, 50)  # Position the sword further away from the body
#     glRotatef(sword_angle, 1, 0, 0)  # Make sword vertical (pointing up)
#     gluCylinder(gluNewQuadric(), 4, 4, 60, 10, 10)  # Sword hilt and blade
#     glPopMatrix()

#     glPopMatrix()

#     # === LEFT ARM === (regular pose)
#     glColor3f(0.4, 0.4, 0.4)  # Left arm
#     glPushMatrix()
#     glTranslatef(-50, 0, 90)  # Start from left shoulder
#     glScalef(0.5, 0.5, 2.5)  # Arm shape
#     glutSolidCube(30)  # Left arm
#     glPopMatrix()

#     # === LEGS ===
#     glColor3f(0.3, 0.3, 0.3)  # Legs
#     for side in [-1, 1]:
#         glPushMatrix()
#         glTranslatef(side * 20, 0, 15)
#         glScalef(0.6, 0.6, 2.5)
#         glutSolidCube(30)
#         glPopMatrix()

#     glPopMatrix()

def draw_shapes2():
    glPushMatrix()
    glTranslatef(-100, 0, 0)
    # === TORSO ===
    glColor3f(0.6, 0.6, 0.6)  # Steel gray
    glPushMatrix()
    glTranslatef(0, 0, 90)
    glScalef(1, 0.5, 2)  # Wider chest
    glutSolidCube(60)
    glPopMatrix()

    # === HEAD ===
    glColor3f(1, 1, 1)  # White
    glPushMatrix()
    glTranslatef(0, 0, 160)
    glutSolidCube(30)
    glPopMatrix()

    # === EYES ===
    glColor3f(1, 0, 0)  # Red eyes
    glPushMatrix()
    glTranslatef(-8, 15, 160)
    glutSolidSphere(3, 10, 10)
    glTranslatef(16, 0, 0)
    glutSolidSphere(3, 10, 10)
    glPopMatrix()

    # === ARMS ===
    glColor3f(0.4, 0.4, 0.4)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 50, 0, 90)
        glScalef(0.5, 0.5, 2.5)
        glutSolidCube(30)
        glPopMatrix()

    # === LEGS ===
    glColor3f(0.3, 0.3, 0.3)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 0, 15)
        glScalef(0.6, 0.6, 2.5)
        glutSolidCube(30)
        glPopMatrix()

    # === SHOULDER CANNONS ===
    glColor3f(1, 1, 0)  # Yellow
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 40, -20, 140)
        glRotatef(-60, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)
        glPopMatrix()

    glPopMatrix()



def draw_shapes():
    global sword_angle
    glPushMatrix()
    glTranslatef(0, 0, 30)

    # === TORSO ===
    glColor3f(0.6, 0.1, 0.1)  # Reddish color for the robot
    glPushMatrix()
    glTranslatef(0, 0, 90)
    glScalef(1, 0.5, 2)  # Wider chest
    glutSolidCube(60)
    glPopMatrix()

    # === HEAD ===
    glColor3f(0.8, 0.2, 0.2)  # Reddish color for the robot
    glPushMatrix()
    glTranslatef(0, 0, 160)
    glutSolidCube(30)
    glPopMatrix()

    # === EYES (Mean looking eyes) ===
    glColor3f(1, 0, 0)  # Red for the "mean" eyes
    glPushMatrix()
    glTranslatef(-8, 15, 160)
    glutSolidSphere(4, 10, 10)  # Slightly bigger to make them look intense
    glTranslatef(16, 0, 0)
    glutSolidSphere(4, 10, 10)
    glPopMatrix()

    # === RIGHT ARM === (Sword arm)
    glColor3f(0.7, 0.2, 0.2)  # Reddish color for the right arm
    glPushMatrix()
    glTranslatef(50, 0, 90)  # Start from right shoulder
    glRotatef(-5, 0, 0, 1)  # Rotate to raise arm upwards

    # The right hand (palm facing upwards)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glRotatef(190, 0, 0, 1)  # Positioning the hand in a palm-up position
    glScalef(0.7, 0.7, 0.7)  # Slightly scaled for hand size
    glutSolidCube(20)  # Hand
    glPopMatrix()

    # Sword in the palm of the right hand
    glColor3f(0, 1, 0)  # Red blade color
    glPushMatrix()
    glTranslatef(0, 0, 50)  # Position the sword further from the body
    glRotatef(sword_angle, 1, 0, 0)  # Rotate the sword
    gluCylinder(gluNewQuadric(), 4, 4, 60, 10, 10)  # Sword hilt and blade
    glPopMatrix()

    glPopMatrix()

    # === LEFT ARM === (Sword arm)
    glColor3f(0.7, 0.2, 0.2)  # Reddish color for the left arm
    glPushMatrix()
    glTranslatef(-50, 0, 90)  # Start from left shoulder
    glScalef(0.5, 0.5, 2.5)  # Arm shape
    glutSolidCube(30)  # Left arm
    glPopMatrix()

    # === LEGS ===
    glColor3f(0.7, 0.2, 0.2)  # Reddish color for the legs
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 0, 15)
        glScalef(0.6, 0.6, 2.5)
        glutSolidCube(30)
        glPopMatrix()

    # === SHOULDER GUNS === (Gun arm)
    glColor3f(1, 1, 0)  # Yellow color for the guns
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 40, -20, 140)
        glRotatef(-60, 1, 0, 0)  # Rotate guns to aim downwards
        gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)  # Gun barrels
        glPopMatrix()

    glPopMatrix()



class Enemy:
    def __init__(self, x=0, y=0, z=30):
        self.x = x
        self.y = y
        self.z = z
        self.sword_angle = -20  # Placeholder in case you want to animate or rotate the sword later
        self.stats={'attack':90, 'defense':75,'magic':80}
        self.hp=10000
        self.resistance={'physical':1, 'fire':0.5,'ice':1.5,'electricity':0.8}
        self.buff_debuff=[0,0,0]


    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        # === TORSO ===
        glColor3f(0.6, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(0, 0, 90)
        glScalef(1, 0.5, 2)
        glutSolidCube(60)
        glPopMatrix()

        # === HEAD ===
        glColor3f(0.8, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(0, 0, 160)
        glutSolidCube(30)
        glPopMatrix()

        # === EYES ===
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(-8, 15, 160)
        glutSolidSphere(4, 10, 10)
        glTranslatef(16, 0, 0)
        glutSolidSphere(4, 10, 10)
        glPopMatrix()

        # === RIGHT ARM (Sword arm) ===
        glColor3f(0.7, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(50, 0, 90)
        glRotatef(-5, 0, 0, 1)

        # Hand
        glPushMatrix()
        glTranslatef(0, 0, 40)
        glRotatef(190, 0, 0, 1)
        glScalef(0.7, 0.7, 0.7)
        glutSolidCube(25)
        glPopMatrix()

        # Sword
        glColor3f(0, 1, 0)
        glPushMatrix()
        glTranslatef(10, 0, 50)
        glRotatef(self.sword_angle, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 4, 4, 60, 10, 10)
        glPopMatrix()

        glPopMatrix()

        # === LEFT ARM ===
        glColor3f(0.7, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(-50, 0, 90)
        glScalef(0.5, 0.5, 2.5)
        glutSolidCube(30)
        glPopMatrix()

        # === LEGS ===
        glColor3f(0.7, 0.2, 0.2)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 20, 0, 15)
            glScalef(0.6, 0.6, 2.5)
            glutSolidCube(30)
            glPopMatrix()

        # === SHOULDER GUNS ===
        glColor3f(1, 1, 0)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 40, -20, 140)
            glRotatef(-60, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)
            glPopMatrix()

        glPopMatrix()

enemy = Enemy(x=0, y=0, z=30) 

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
    global player_pos,player_rotation,enemy_pos,player_life,game_end_flag,hits,boolets_missed,boolet_pos,boolet_direction,player_life,first_person,camera_pos,cheat_mode,cheat_vision,radian_calc_for_cheat_vision,radian_calc_for_cheat_vision,game_end_condition,regular_condition,last_action
    
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # Move forward (W key)
    if key == b'w' and game_end_flag==False:  # Move forward
        p1.move('forward',10)
        


    if key == b's' and game_end_flag==False:  # Move backward
        p1.move('backward',10)
    
    # Limit player within grid
    
  
   


    if key == b'a' and game_end_flag==False and cheat_mode==False:  # Rotate left
        p1.rotate(10)

    if key == b'd' and game_end_flag==False and cheat_mode==False:  # Rotate right
        p1.rotate(-10)

    # # Toggle cheat mode (C key)
   
    if key==b'1' and not turn_order[current_player].innermenu_active:
        print('attacking')
        # last_action=f'{turn_order[current_player].name} used regular attack'
        turn_order[current_player].perform_action_phys()
       
    elif key==b'2' and not turn_order[current_player].innermenu_active:
        # print(p1.innermenu_active)
        turn_order[current_player].innermenu_active=True
        skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3]
    elif key==b'3' and not turn_order[current_player].innermenu_active:
        turn_order[current_player].guarding=True
        turn_order[current_player].stats['defense']+=60
        last_action=f'guarding increased defense by 60 points'
        next_player()
    elif key==b'1' and turn_order[current_player].innermenu_active:
 
        print('Madness Crush landed, crit strike!')
        skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3]
        
        if skills[0][2].startswith('physical'):
            last_action=f'{turn_order[current_player].name} used {skills[0][0]}'
            turn_order[current_player].perform_action_phys(1)
        elif skills[0][2].startswith('magic'):
            print(skills)
            last_action=f'{turn_order[current_player].name} used {skills[0][0]}'
            turn_order[current_player].perform_action_mag(1)
        elif skills[0][2].startswith('support'):
            print(skills)
            last_action=f'{turn_order[current_player].name} used {skills[0][0]}'
            turn_order[current_player].perform_action_support(1)


        turn_order[current_player].innermenu_active=False
        if turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and turn_order[current_player].support_execution_mode==False:
                next_player()
        
    elif key==b'2' and turn_order[current_player].innermenu_active:
      
        # print('Weakness striked! 30 fire ddamage done')
        skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3]
      
        if skills[1][2].startswith('physical'):
            last_action=f'{turn_order[current_player].name} used {skills[1][0]}'
            turn_order[current_player].perform_action_phys(2)
        elif skills[1][2].startswith('magic'):
            
            last_action=f'{turn_order[current_player].name} used {skills[1][0]}'
            turn_order[current_player].perform_action_mag(2)
        elif skills[1][2].startswith('support'):
            print(skills)
            last_action=f'{turn_order[current_player].name} used {skills[0][0]}'
            turn_order[current_player].perform_action_support(2)


        turn_order[current_player].innermenu_active=False
        if turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and turn_order[current_player].support_execution_mode==False:
                next_player()
        
    elif key==b'3' and turn_order[current_player].innermenu_active:
        print('raised attacks of all allies by one')
        skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3]
        
        if skills[2][2].startswith('physical'):
            last_action=f'{turn_order[current_player].name} used {skills[2][0]}'
            turn_order[current_player].perform_action_phys(3)
        elif skills[2][2].startswith('magic'):
            print(skills)
            last_action=f'{turn_order[current_player].name} used {skills[2][0]}'
            turn_order[current_player].perform_action_mag(3)
        elif skills[2][2].startswith('support'):
            print(skills)
            last_action=f'{turn_order[current_player].name} used {skills[2][0]}'
            turn_order[current_player].perform_action_support(3)


        turn_order[current_player].innermenu_active=False
        if turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and turn_order[current_player].support_execution_mode==False:
                next_player()
    elif key==b'0' and turn_order[current_player].innermenu_active:
        
        turn_order[current_player].innermenu_active=False
    


 



def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos,left_arm_angle,right_arm_angle,sword_angle
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        if enemy.sword_angle<-25:
            enemy.sword_angle += 5
        

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        if enemy.sword_angle>-95-35:
            enemy.sword_angle-=5
          

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global camera_pos,first_person,cheat_mode
    """
    Handles mouse inputs for firing boolets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a boolet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
    #     fire_boolet()

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print('yes',cheat_mode)
        if first_person:
           first_person = False
           
                
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
        eyeX = (turn_order[current_player].camera_x+30)
        eyeY = turn_order[current_player].camera_y+50
        eyeZ = 70+24+13+10+10  # Near head

        # Calculate where to look based on rotation
        distance = 100  # how far to look forward
        rad = math.radians(turn_order[current_player].camera_rotation)
        targetX = eyeX + math.sin(-rad) * distance-10
        targetY = eyeY + math.cos(-rad) * distance
        targetZ = eyeZ  # Same Z (horizontal view)

        gluLookAt(eyeX, eyeY, eyeZ,
                  targetX, targetY, targetZ,
                  0, 0, 1)
    elif first_person and cheat_mode and not cheat_vision:
        eyeX = p1.position[0]-10  # Fixed X position
        eyeY = p1.position[1]-10 # Fixed Y position
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



def dead_skip(player):
    if player.alive_status==False:
        next_player()


def idle():
    """
    Idle function that runs continuously:
    - Updates the player's rotation for cheat mode.
    - Updates boolet positions and checks for collisions.
    - Triggers screen redraw for real-time updates.
    """
    global boolet_pos, boolet_direction, boolets_missed, hits, enemy_pos, player_pos, player_rotation, player_life, game_end_flag, cheat_mode,regular_condition,game_end_condition,first_person
    turn_order[current_player].update_phys(enemy_position)
    turn_order[current_player].update_support()  # Ensure this is here
    turn_order[current_player].update_mag(enemy_position)
    dead_skip(turn_order[current_player])
    
    update_boolets()     # Move bullets each frame
    draw_boolet()        # Draw them each frame
    glutPostRedisplay()  # Ensure screen updates with the latest changes

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
    if p1.player_hp>70:
        draw_text(10, 480, f"{p1.name} HP: {p1.player_hp}", color=[0, 1, 0])  
    else:
        draw_text(10, 480, f"{p1.name} HP: {p1.player_hp}", color=[1.0, 0.647, 0.0]) 
    draw_text(10, 460, f"{p1.name} MP: {p1.player_mp}", color=[0.53, 0.81, 0.92])  
    if p2.player_hp>70:
        draw_text(10+120*1, 480, f"{p2.name} HP: {p2.player_hp}", color=[0, 1, 0])  
    else:
        draw_text(10+120*1, 480, f"{p2.name} HP: {p2.player_hp}", color=[1.0, 0.647, 0.0]) 
    draw_text(10+120*1, 460, f"{p2.name} MP: {p2.player_mp}", color=[0.53, 0.81, 0.92])  
    
    if p3.player_hp > 70:
        draw_text(10 + 120 * 2, 480, f"{p3.name} HP: {p3.player_hp}", color=[0, 1, 0])
    else:
        draw_text(10 + 120 * 2, 480, f"{p3.name} HP: {p3.player_hp}", color=[1.0, 0.647, 0.0])

    draw_text(10+120*2, 460, f"{p3.name} MP: {p3.player_mp}", color=[0.53, 0.81, 0.92])  

    if p4.player_hp>70:
    
        draw_text(10+120*3, 480, f"{p4.name} HP: {p4.player_hp}", color=[0, 1, 0])  
    else:
        draw_text(10 + 120 * 2, 480, f"{p4.name} HP: {p4.player_hp}", color=[1.0, 0.647, 0.0])
    draw_text(10+120*3, 460, f"{p4.name} MP: {p4.player_mp}", color=[0.53, 0.81, 0.92])  
    

    if enemy.hp>200:
        draw_text(10+120*4, 480, f"Metatron HP: {enemy.hp}", color=[0, 1, 0])
    else:
        draw_text(10+120*4, 480, f"Metatron HP: {enemy.hp}", color=[1.0, 0.647, 0.0])
    
    draw_text(10, 460-20, f"Current Player: {turn_order[current_player].name}")
    # Display game info text at a fixed screen position
    if not turn_order[current_player].innermenu_active and game_end_flag==False and turn_order[current_player] in players_class_list and turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False:
        draw_text(10, 445-23, f"1. Attack")
        draw_text(10, 433-23, f"2. Skill")
        draw_text(10, 421-23, f"3. Guard")

    elif turn_order[current_player].innermenu_active and game_end_flag==False and turn_order[current_player] in players_class_list and turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False:
        draw_text(10, 445-23, f"1. {turn_order[current_player].skill1[0]}->{turn_order[current_player].skill1[1]}->{turn_order[current_player].skill1[4]} MP")
        draw_text(10, 433-23, f"2. {turn_order[current_player].skill2[0]}->{turn_order[current_player].skill2[1]}->{turn_order[current_player].skill2[4]} MP")
        draw_text(10, 421-23, f"3. {turn_order[current_player].skill3[0]}->{turn_order[current_player].skill3[1]}->{turn_order[current_player].skill3[4]} MP")
        draw_text(10, 421-23-12, f"0. Go back")
    draw_text(10, 397-23-20, f"Last Action Result: {last_action}")
    



    
        

    # draw_shapes()
    current_time = (time.time() - start_time)*10  # Get elapsed time
    enemy_size = (np.sin(current_time) + 1) / 2 * (30 - 25) + 25  # Oscillate between 25 and 30


    # Draw the enemy with the calculated size
    # for key in enemy_pos:
    #     enemy_posX=key['enemy_posX']
    #     enemy_posY=key['enemy_posY']
    #     draw_enemy(enemy_posX,enemy_posY,enemy_size)
    limit_fps(30)
    p1.draw()
    p2.draw()
    p3.draw()
    p4.draw()
    enemy.draw()
    # draw_shapes()
    # draw_shapes2()
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
    
    # generate_enemy()  # Generate enemies, initially
    print(enemy_pos)
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the boolet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
