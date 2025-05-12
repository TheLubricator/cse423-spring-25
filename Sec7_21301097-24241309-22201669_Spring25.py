
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

t=0
GRID_RADIUS = 399  # Radius of the grid
STEP = 15  # Step between grid points
# Camera-related variables
camera_pos = [0,180,255]
turn_in_progress = True


#depreciated vars##########
cheat_vision=False
cheat_mode=False
###############################
first_person = True  # Flag for first-person view
fovY = 120  # Field of view
GRID_LENGTH = 299  # Length of grid lines (total size 299*2=598)
####XXXXXXXXXXXXXXXXXXX#############
rand_var = 423
start_time = time.time()  # Record the start time for enemy fattening

#######XXXXXXXXX#################
enemy_pos=[]
##################################
player_rotation = 0
player_pos = [0, 0]
hits=0
player_life=5
########################################



# REQ###########
boolet_pos = []  # Stores the current position of the boolet
boolet_direction = [] 
enemy_boolet_pos = []  # Stores the current position of the boolet
enemy_boolet_direction = [] 
megido_ark_pos=[0,100,300]
megido_mode=False
turn_cycles=0

##########
boolets_missed=0
############
game_end_flag=False
win=None
loss=False

regular_condition=1
game_end_condition=0

regular_condition_player=1
game_end_condition_player=0
########################
left_arm_angle=-90
right_arm_angle=-90
sword_angle=-20
########################
enemy_position = (0, 0)
last_action=''
def limit_fps(target_fps):
    start_time = time.perf_counter()
    # Frame processing happens here
    end_time = time.perf_counter()
    frame_time = end_time - start_time
    target_frame_time = 1 / target_fps
    if frame_time < target_frame_time:
        time.sleep(target_frame_time - frame_time)

class Player:
    def __init__(self,x,y,hp,mp,attack_power,defensne_power,magic_power):
        self.guarding=False
        self.regular_condition_player=1
        self.game_end_condition_player=0
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
        self.camera_x=self.position[0]+30
        self.camera_y=self.position[1]+50
        self.camera_z=70+24+13+10+10
        self.camera_pitch = 0
        self.camera_rotation=self.rotation
        self.skill1=None
        self.skill2=None
        self.skill3=None
        self.skill4=None
        self.original_position = [x, y]
        self.original_rotation = self.rotation
        self.resistance=None

        self.alive_status=True
    # def move(self, direction, distance):
    #     radians = math.radians(self.rotation)
    #     if direction == "forward":
    #         self.position[0] += distance * math.sin(-radians)
    #         self.position[1] += distance * math.cos(-radians)
    #     elif direction == "backward":
    #         self.position[0] -= distance * math.sin(-radians)
    #         self.position[1] -= distance * math.cos(-radians)

    #     # Constrain within circular boundary
    #     distance_from_center = math.hypot(self.position[0], self.position[1])
    #     if distance_from_center > GRID_RADIUS - 10:  # Add a small margin to prevent going outside
    #         # Push the player back to the boundary
    #         angle = math.atan2(self.position[1], self.position[0])
    #         self.position[0] = (GRID_RADIUS - 10) * math.cos(angle)
    #         self.position[1] = (GRID_RADIUS - 10) * math.sin(angle)

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



    def move_towards_enemy(self, enemy_position, step_size, min_distance=0):
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
        print(self.action_execution_mode)
        if self.action_execution_mode and not self.magic_execution_mode:
            return  # If already performing an action, ignore other inputs

        self.action_execution_mode = True
        print(self.action_execution_mode)
        self.action_state = 0  # Start action sequence
        self.skill_trigger=skill
    def perform_action_mag(self, skill=''):
        if self.magic_execution_mode and not self.action_execution_mode :
            return  # If already performing an action, ignore other inputs
       

        self.magic_execution_mode = True
        self.magic_state = 0  # Start action sequence
        skills=[self.skill1,self.skill2,self.skill3,self.skill4]
        self.total_skill=skills[skill-1]
        if skill=='':
            self.skill_trigger=skill
        else:
            self.total_skill=skills[skill-1]
            self.type=self.total_skill[2]
            
            self.skill_trigger=self.type.split('_')[1]
    def update_mag(self, enemy_position):
        global last_action,boolet_pos,turn_in_progress
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
                
          
                self.magic_state = 2  # End of magic action
                print(self.magic_state)
            elif self.magic_state==2:
                if len(boolet_pos)==0:
                    self.magic_state=3
            elif self.magic_state == 3:  # Step 3: End action
                self.reset_position()
                self.magic_execution_mode = False
                self.magic_state = 5  # Reset for next time
                self.action_state = 5  # Optional marker
                print(self.total_skill)
                self.use_magic(self.total_skill)
                self.alive_check()

                # if self.skill_trigger=='regular attack':
                #     self.regular_attack()
                turn_in_progress=False
                next_player()
    def update_support(self):
        global turn_in_progress
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
               
                skills = [self.skill1, self.skill2, self.skill3,self.skill4]
                self.use_support_skill(skills[self.skill - 1])
                self.support_execution_mode = False  # End the action
                self.support_state = 5  # Set state to 5 to indicate that the action is complete
                turn_in_progress=False
                next_player()

                          
    
    def use_support_skill(self,skill):
        global last_action
        fail=False
        enemy_buff=False
        dif=''
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
                    elif skill[5]=='debuff':
                        fail=True
                        dif='debuff'
                        print('enter')
                        for buff in range(len(team.buff_debuff)):
                            if team.buff_debuff[buff]<0:
                                team.buff_debuff[buff]=0

                      
                        
                           
                            

                    print(team.buff_debuff)
                if not fail:
                    last_action=f'{skill[5].upper()} of all allies raised by one'
                elif fail and dif=='debuff':
                    last_action=f'Dekunda used by {self.name}. All negative effects removed!'
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
                elif skill[5]=='buff':
                        
                        for buff in range(len(enemy.buff_debuff)):
                            if enemy.buff_debuff[buff]>0:
                                enemy.buff_debuff[buff]=0

                        fail=True
                        enemy_buff=True
                        dif='buff'
                                
                       
                print(enemy.buff_debuff)
            
            if not fail and not enemy_buff:
                last_action=f'{skill[5].upper()} of enemy decreased by one'
            elif fail and dif=='buff' and enemy_buff:
                last_action=f'{self.name} used Dekaja. All positive effects removed!'
            elif fail and dif=='' and not enemy_buff:
                print(fail,dif)
                last_action=f'Enemy {skill[5].upper()} already at minimum rank'
        elif skill[7]=='heal':
             if  self.player_mp>= skill[4]:
                self.player_mp-=skill[4]
                teammates=[p1,p2,p3,p4]
                for team in teammates:
                    team.player_hp+=int(team.og_hp*0.40)
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
        global last_action,turn_in_progress
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
                    if self.skill_trigger=='regular attack':
                        self.regular_attack()
                        self.alive_check()
                    else:
                        skills=[self.skill1,self.skill2,self.skill3,self.skill4]
                        self.skill_phys_attack(skills[self.skill_trigger-1])
                        self.alive_check()

            elif self.action_state == 4:  # Step 4: Return to starting position and rotation
                self.reset_position()
                self.action_execution_mode = False  # End the action
                self.action_state = 5  # Mark that action is completely done
                print(self.skill_trigger)
                turn_in_progress=False
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


    def alive_check(self):
        global regular_condition,game_end_condition
        if enemy.hp<0:
            enemy.hp=0    
            regular_condition=0
            game_end_condition=1
            enemy.alive_status=False
            enemy.rotation=90    



    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 30)
        glRotatef(self.rotation, 0, self.game_end_condition_player,self.regular_condition_player)  # Two conditions added to invert axis when player is dead

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





class Enemy:
    def __init__(self, x=0, y=-50, z=30):
        self.name='Metatron'
        self.x = x
        self.y = 0
        self.z = z
        self.original_x = x
        self.original_y=y
        self.original_z=z
        self.eye_color=0.5
        self.sword_size=60
        
        self.rotation=0
        self.original_rotation = self.rotation
        self.sword_angle = -90  # Placeholder in case you want to animate or rotate the sword later
        self.stats={'attack':90, 'defense':75,'magic':80}
        self.hp=4000
        self.resistance={'physical':1, 'fire':0.5,'ice':1.5,'electricity':0.4}
        self.buff_debuff=[0,0,0]
        self.camera_x=x+100
        self.camera_y=270
        self.camera_z=z+100+100
        self.camera_rotation=0
        self.camera_pitch = -90
        self.alive_status=True
        self.move=False
        self.regular_attack_execution_mode=False
        self.sinai_execution_mode=False
        self.deathbound_execution_mode=False
        self.support_execution_mode=False
        self.charging_executiion_mode=False
        self.charged=False
        self.sword_color=[0,1,0]
        self.special_support_execution_mode=False
        self.shield_of_god=False
        self.megido_ark_execution_mode=False
        self.critical_state=False
        
    def skill_chance_above_700(self):
        
        skill_weights = {
            "regular_attack": 10,  # more likely to use
            "fire_of_sinai": 20,
            "deathbound": 25,
            "omnipotence": 22,
            "luster_candy":15,
            "debilitate": 15,
            "charge": 5  # very rarely used
        }
        return random.choices(list(skill_weights.keys()), list(skill_weights.values()))[0]
    def skill_chance_below_700(self):
        # Skills available when HP < 700
        skill_weights = {
            "omnipotence": 35,  # prioritized skills after critical state
            "regular_attack": 2,
            "fire_of_sinai": 25,
            "holy_wrath": 10,  # 100% first time after critical state
            "shield_of_god": 8,
            "waves_of_order": 5,
            "charge": 20  # more likely to use charge below 700
        }
        if self.critical_state==False:
            self.critical_state = True
            return "holy_wrath"
        return random.choices(list(skill_weights.keys()), list(skill_weights.values()))[0]
    def choose_an_enemy(self):
    # Filter alive players (player_hp > 0 and alive_status == True)
        alive_players = [player for player in players_class_list if player.player_hp > 0 and player.alive_status]
        
        if not alive_players:
            # No alive players; this should trigger game over, but just in case, return None or handle gracefully
            print("No alive players to target!")
            return None
        
        # Select a random alive player
        chosen_player = random.choice(alive_players)
        print(chosen_player.name)
        return chosen_player
    def choose_action(self):
    # Pick a random player to move towards
        global turn_cycles,turn_in_progress,current_player
        print(current_player)
        if turn_cycles >= 12:
            self.perform_megido_ark()
        else:
            
            if self.hp>700 and not self.critical_state:
                skill=self.skill_chance_above_700()
                if skill=='charge' and self.charged:
                    while True:
                       skill=self.skill_chance_above_700() 
                       if skill!='charge':
                          break
                elif skill=='charge' and not self.charged:
                    self.perform_charge_skill()
                elif skill=='regular_attack':
                    
                    self.perform_regular_attack(self.choose_an_enemy(),'regular')
                elif skill=='fire_of_sinai':
                    self.perform_fire_of_sinai()
                elif skill=='deathbound':
                    self.perform_deathbound()
                elif skill=='omnipotence':
            
                    self.perform_regular_attack(self.choose_an_enemy(),'omnipotence')
                elif skill=='luster_candy':
                    self.perform_support_skill('Luster Candy')
                elif skill=='debilitate':
                    self.perform_support_skill('Debilitate')
            elif self.hp<=700 or self.critical_state:
                skill=self.skill_chance_below_700()
                if skill=='charge' and self.charged:
                    while True:
                       skill=self.skill_chance_below_700()
                       if skill!='charge':
                          break
                elif skill=='charge' and not self.charged:
                    self.perform_charge_skill()
                elif skill=='omnipotence':
                    self.perform_regular_attack(self.choose_an_enemy(),'omnipotence')
                elif skill=='regular_attack':
                    self.perform_regular_attack(self.choose_an_enemy(),'regular')
                elif skill=='fire_of_sinai':
                    self.perform_fire_of_sinai() 
                elif skill=='holy_wrath':
                    self.perform_special_support('holy wrath')
                elif skill=='shield_of_god':
                    self.perform_special_support('shield of god')
                elif skill=='waves_of_order':
                    self.perform_special_support('waves of order')

        

                


                

        # self.pick_a_nigga = random.choice(players_class_list)
        # self.perform_regular_attack(self.pick_a_nigga) 
        # self.perform_support_skill('Debilitate')
        # if self.charged:
        #     self.perform_regular_attack(self.pick_a_nigga,'omnipotence')
        # else:
        #     self.perform_charge_skill()
        # self.perform_special_support('shield of god')
        # self.perform_special_support('waves of order')
        # self.perform_special_support('holy wrath')
        


    
    def donothing(self):
        pass

    def rotate_to_player(self,player):
        target_x, target_y = player.position  # Get target position
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        
        target_angle =- math.degrees(math.atan2(delta_x, delta_y))   # Get the angle in degrees

        # Normalize the target_angle to the range of [-180, 180]
        if target_angle > 180:
            target_angle -= 360  # Adjust to [-180, 180] range if necessary

       
        self.angle_diff = (target_angle - self.rotation + 180) % 360 - 180  # Normalize to [-180, 180]
        
       
        if abs(self.angle_diff) > 12:
            rotation_step = self.angle_diff / 20  # Smoothness factor
            self.rotation = (self.rotation + rotation_step) % 360  # Update rotation with the smooth step
        else:
            # Once close enough, snap to the target angle and stop moving
            self.rotation = target_angle
            print(self.rotation)
            # Stop movement once the rotation is complete





    def move_to_player(self,player):
        min_distance = 60  # Minimum distance to stop moving
        target_x, target_y = player.position  # Get the target player's position
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        self.distance_to_target = math.hypot(delta_x, delta_y)  # Calculate the distance to the target
        

        if self.distance_to_target > min_distance:  # Only move if we are not too close
            # Calculate the angle towards the target (player)
            angle_to_target = math.atan2(delta_y, delta_x)
         

            # Move towards the target by `step_size` units in the direction of the angle
            step_x = 7 * math.cos(angle_to_target)
            step_y = 7 * math.sin(angle_to_target)

            # Update the enemy's position
            self.x += step_x
            self.y += step_y
        else:
            # If we are close enough to the target, stop and adjust position to be exactly at the target
            
            
            print("Enemy reached the target!")
    def random_chance(self,chance: float):
        return random.random() < chance 
    def raise_sword(self):
        if self.sword_angle<=-10:
            self.sword_angle+=2
    def lower_sword(self):
        if self.sword_angle>-135:
            self.sword_angle-=2
    def level_sword(self):
        self.sword_angle=-90
    
    def jetpack_up(self):
        if self.z<130:
            self.z+=2
    def jetpack_down(self):
        if self.z>30:
            self.z-=2
    def move_fifty_steps_forward(self):
        if self.y<50:
            self.y+=5
    def extend_sword(self):
        if self.sword_size<150:
            self.sword_size+=30
    def rotate_to_plus_60d(self):
        if self.rotation<60:
            self.rotation+=5
    def rotate_back_to_zero(self):
        if self.rotation>0:
            self.rotation-=3
    def move_fifty_steps_back(self):
        if self.y>0:
            self.y-=5
    def face_zoom(self):
        if self.camera_y>100:
            self.camera_y-=5
    def charge_multiplier(self):
        if self.charged==False:
            return 1
        else:
            self.charged=False
            self.sword_color=[0,1,0]
            return 2.5
    def zoomed_mode(self):
        self.camera_y=120
    def cam_normal(self):
        self.camera_y=270
    def do_a_360_almost(self):
        if self.rotation<350:
            self.rotation+=10



    def reset_position(self):
        self.x=self.original_x
        self.y=self.original_y
        self.rotation=self.original_rotation
    
    def fire_boolet(self,color='ice'):
        global enemy_boolet_pos, enemy_boolet_direction

    # Spawn the bullet at the player's current position and height
        for _ in range(5):
            enemy_boolet_pos.append([random.randrange(self.x-50,self.x+50), self.y+50, self.z+70])

        # Calculate the forward direction based on current rotation
            radians = math.radians(int(random.randrange(self.rotation-60,self.rotation+60)))
            dx = math.sin(-radians)
            dy = math.cos(-radians)

        # Store the bullet's direction
            enemy_boolet_direction.append([dx, dy])
        print(enemy_boolet_pos,enemy_boolet_direction)
    def perform_regular_attack(self,player,types):
        if self.regular_attack_execution_mode:
            return
        self.regular_attack_execution_mode=True
        self.action_state=0
        self.player_chosen=player
        self.single_attack_type=types
        
    
    def enemy_update_regular(self):
        global last_action,turn_in_progress
        # print(self.regular_attack_execution_mode,self.action_state)
        if self.regular_attack_execution_mode:
            if self.action_state==0:
                self.rotate_to_player(self.player_chosen)

                if abs(self.angle_diff) < 10:
                    
                    self.action_state=1
            elif self.action_state==1:
                self.move_to_player(self.player_chosen)
                if self.distance_to_target<60:
                    self.action_state=2
            elif self.action_state==2:
                self.raise_sword()
                if self.sword_angle>=-10:
                    self.action_state=3
                    
            elif self.action_state==3:
                # print('entered',self.sword_angle)
                self.lower_sword()
                if self.sword_angle<=-135:
                   
                    self.action_state=4
            elif self.action_state==4:
                if self.single_attack_type=='regular':
                    self.register_regular_attack(self.player_chosen)
                elif self.single_attack_type=='omnipotence':
                    self.register_omnipotence(self.player_chosen)
                self.level_sword()
                self.action_state=5
            elif self.action_state==5:
                self.reset_position()
                self.regular_attack_execution_mode=False
                self.action_state=6
                self.alive_check()
                next_player()
                turn_in_progress = False
    def register_omnipotence(self,player):
        global last_action
        will_it_hit=self.random_chance(0.99)
        will_it_crit=self.random_chance(0.7)
        base_power = 200
        damage_scaling=0.4
        print(self.charged)
        charge_multiplier=self.charge_multiplier()
        print(self.charged,charge_multiplier)
        extra=''
        variance = random.uniform(0.85, 1.1)
        if will_it_hit:
            pick_debuff=random.randint(0,2)
            pick=['Attack','Defense','Magic']
            if player.buff_debuff[pick_debuff]>-3:
                player.buff_debuff[pick_debuff]-=1
                extra=f' {pick[pick_debuff]} reduced by one rank'
            else:
                extra=f' {pick[pick_debuff]} already at lowest rank.'
            if not will_it_crit or player.guarding:

                damage = round(max(1, int((self.stats['attack'] * base_power) / ((player.stats['defense']*(1+(player.buff_debuff[1]/8))) + 1)*variance*(1+(self.buff_debuff[0]/8))*damage_scaling*player.resistance['physical']*charge_multiplier)))
                player.player_hp-=damage
                

            
                last_action=f'{self.name} used Omnipotence on {player.name}.{extra}'
            elif will_it_crit and not player.guarding:
                damage = round(max(1, (int((self.stats['attack'] * base_power) / ((player.stats['defense']*(1+(enemy.buff_debuff[1]/8)))+ 1)))*variance*2*(1+(self.buff_debuff[0]/8))*damage_scaling*player.resistance['physical']*charge_multiplier))
                player.player_hp-=damage
            
                last_action=f'Critical strike! {self.name} used Omnipotence on {player.name}.{extra}'
            
          
            print(player.buff_debuff)
        else:
            last_action=f'Attack missed!'
            

    def register_regular_attack(self,player):
        global last_action
        will_it_hit=self.random_chance(0.99)
        will_it_crit=self.random_chance(0.3)
        base_power = 150
        damage_scaling=0.4
        print(self.charged)
        charge_multiplier=self.charge_multiplier()
        print(self.charged,charge_multiplier)
        variance = random.uniform(0.85, 1.1)
        if will_it_hit:
            if not will_it_crit:

                damage = round(max(1, int((self.stats['attack'] * base_power) / ((player.stats['defense']*(1+(player.buff_debuff[1]/8))) + 1)))*variance*(1+(self.buff_debuff[0]/8))*damage_scaling*player.resistance['physical']*charge_multiplier)
                player.player_hp-=damage
            
                last_action=f'{self.name} dealt damage {damage} to {player.name} using regular swing'
            else:
                damage = round(max(1, (int((self.stats['attack'] * base_power) / ((player.stats['defense']*(1+(enemy.buff_debuff[1]/8)))+ 1)))*variance*1.4*(1+(self.buff_debuff[0]/8))*damage_scaling*charge_multiplier*player.resistance['physical']))
                player.player_hp-=damage
            
                last_action=f'Critical strike! {self.name} dealt damage {damage} to {player.name} using regular swing'
        else:
            last_action=f'Attack missed!'
    def perform_fire_of_sinai(self):
        if self.sinai_execution_mode and not self.register_regular_attack:
            return
        self.sinai_execution_mode=True
        self.sinai_state=0
    def enemy_update_sinai(self):
        global enemy_boolet_pos,turn_in_progress
        if self.sinai_execution_mode:
            if self.sinai_state==0:
                self.jetpack_up()
                if self.z>=130:
                    self.sinai_state=1
            elif self.sinai_state==1:
                self.fire_boolet()
                if len(enemy_boolet_pos)>0:
                    self.sinai_state=2
            elif self.sinai_state==2:
                if len(enemy_boolet_pos)==0:
                    self.register_fire_of_sinai()
                    self.alive_check()
                    self.sinai_state=3
            elif self.sinai_state==3:
                self.jetpack_down()
                if self.z<=30:
                    self.sinai_state=4
            elif self.sinai_state==4:
                self.sinai_execution_mode=False
                self.sinai_state=5
                
                next_player()
                turn_in_progress = False
    def register_fire_of_sinai(self):
        global last_action
        base_power=250
        extra_text=''
        for player in players_class_list:
        
            variance = random.uniform(0.85, 1.1)
        

            damage = round(max(1, int((self.stats['magic'] * base_power) / ((player.stats['defense']*(1+(player.buff_debuff[1]/8))) + 1))*variance*(1+(self.buff_debuff[2]/8))*player.resistance['fire']*0.4))
            print(damage)
            if extra_text=='' and player.resistance['fire']>=1.5:
                extra_text=' At least one player\'s weakness hit'
            if  player.alive_status:
             
                player.player_hp-=damage
        last_action=f'Fire of Sinai inflicted severe fire damage to all.{extra_text}'

    def perform_deathbound(self):
        if self.deathbound_execution_mode and not self.regular_attack_execution_mode and not self.sinai_execution_mode:
            return
        self.deathbound_execution_mode=True
        self.deathbound_state=0
    def enemy_update_deathbound(self):
        global turn_in_progress,players_class_list
        if self.deathbound_execution_mode:
            if self.deathbound_state==0:
                self.move_fifty_steps_forward()
                if self.y>=50:
                    self.deathbound_state=1
            elif self.deathbound_state==1:
                self.rotate_to_player(players_class_list[0])
                if abs(self.angle_diff) < 10:
                    self.deathbound_state=2
            elif self.deathbound_state==2:
                self.extend_sword()
                if self.sword_size>=150:
                    self.deathbound_state=3
            elif self.deathbound_state==3:
                self.lower_sword()
                if self.sword_angle<=-135:
                    self.deathbound_state=4
                
            elif self.deathbound_state==4:
                self.rotate_to_plus_60d()
                if self.rotation>=60:
                    self.rotation=60
                    self.register_deathbound()
                    self.alive_check()
                    self.deathbound_state=5
            elif self.deathbound_state==5:
                self.sword_size=60
                self.rotate_back_to_zero()
                if self.rotation<=0:
                    self.rotation=0
                    self.deathbound_state=6
            elif self.deathbound_state==6:
                self.move_fifty_steps_back()
                if self.y<=0:
                    self.deathbound_state=7
            elif self.deathbound_state==7:
                self.deathbound_state=9
                self.deathbound_execution_mode=False
                next_player()
                turn_in_progress=False
    def register_deathbound(self):
        global last_action,players_class_list
        misses=0
        crits=0
        extra=''
        base_power = 200
        print(self.charged)
        charged_multiplier=self.charge_multiplier()
        print(self.charged,charged_multiplier)
        damage_scaling=0.4
        variance = random.uniform(0.85, 1.1)
        for player in players_class_list:
            will_it_hit=self.random_chance(1)
            will_it_crit=self.random_chance(0.3)
            print('hit?',will_it_hit)
            if will_it_hit:
                if not will_it_crit:

                    damage = round(max(1, int((self.stats['attack'] * base_power) / ((player.stats['defense']*(1+(player.buff_debuff[1]/8))) + 1)*variance*(1+(self.buff_debuff[0]/8))*damage_scaling*player.resistance['physical']*charged_multiplier)))
                    if player.alive_status==True:
                        
                        print('uncrit',damage,player.name)
                        player.player_hp-=damage
                
                    
                else:
                    damage = round(max(1, (int((self.stats['attack'] * base_power*(1+self.buff_debuff[0])) / ((player.stats['defense']*(1+(player.buff_debuff[0]/8)))+ 1)*variance*2*(1+(self.buff_debuff[0]/8))*damage_scaling*player.resistance['physical']*charged_multiplier))))
                    if player.alive_status:
                        player.player_hp-=damage
                        crits+=1
                        print('crit',damage,player.name)
                
            else:
                misses+=1

        if misses>0:
            extra+=f'Min one player missed. '
        if crits>0:
            extra+=f'One crit hit!'
        last_action=f'Deathbound hit the entire party! {extra}'
    def perform_support_skill(self,types):
        if self.support_execution_mode and not self.sinai_execution_mode and not self.regular_attack_execution_mode and not self.deathbound_execution_mode:
            return
        self.support_execution_mode=True
        self.support_state=0
        self.support_type=types
    def enemy_update_support(self):
        global turn_in_progress
        if self.support_execution_mode:
         
            if self.support_state==0:
                self.zoomed_mode()
                self.raise_sword()
               
                if self.sword_angle>=-10:
                    self.support_state=1
                    
            elif self.support_state==1:
         
                self.lower_sword()
                if self.sword_angle<=-135:
                   
                    self.support_state=2
            elif self.support_state==2:
                self.register_support_skill()
                self.camera_y=270
                self.level_sword()
                self.support_state=3
            elif self.support_state==3:
                self.support_execution_mode=False
                self.support_state=4
                next_player()
                

    def register_support_skill(self):
        global last_action, players_class_list
        if self.support_type=='Luster Candy':
            if self.buff_debuff[0]<3:
                self.buff_debuff[0]+=1
            if self.buff_debuff[1]<3:
                self.buff_debuff[1]+=1
            if self.buff_debuff[2]<3:
             self.buff_debuff[2]+=1
            print(self.buff_debuff)
            last_action=f'Luster Candy all stats of {self.name} raised by one rank'
        elif self.support_type=='Debilitate':
            for player in players_class_list:
                if player.buff_debuff[0]>-3:
                    player.buff_debuff[0]-=1
                if player.buff_debuff[1]>-3:
                    player.buff_debuff[1]-=1
                if player.buff_debuff[2]>-3:
                    player.buff_debuff[2]-=1
                print(player.buff_debuff)
            last_action=f'Debilitate all stats of the party decreased by one rank'
    def perform_charge_skill(self):
        if self.charging_executiion_mode and not self.sinai_execution_mode and not self.regular_attack_execution_mode and not self.support_execution_mode:
            return
        self.charging_executiion_mode=True
        self.charge_state=0
    def enemy_update_charging(self):
        global turn_in_progress,last_action
        if self.charging_executiion_mode:
            if self.charge_state==0:
                self.zoomed_mode()
                self.charge_state=1
            elif self.charge_state==1:
                self.raise_sword()
                if self.sword_angle>=-10:
                    self.charge_state=2
            elif self.charge_state==2:
                self.sword_color=[3/256, 127/256, 252/256]
                self.charged=True
                self.charge_state=3
                    
            elif self.charge_state==3:
                # print('entered',self.sword_angle)
                self.lower_sword()
                if self.sword_angle<=-135:
                   
                    self.charge_state=4
            elif self.charge_state==4:
                self.charging_executiion_mode=False
                self.charge_state=5
                self.camera_y=270
                last_action=f'{self.name}\'s gathering strength for a powerful attack!'
                
                next_player()
                turn_in_progress=False
    def perform_special_support(self,types):
        if self.special_support_execution_mode and not self.sinai_execution_mode and not self.regular_attack_execution_mode and not self.deathbound_execution_mode and not self.support_execution_mode:
            return
        self.special_support_execution_mode=True
        self.special_support_state=0
        self.special_support_type=types
    def enemy_update_special_support(self):
        global turn_in_progress
        if self.special_support_execution_mode:
         
            if self.special_support_state==0:
                self.zoomed_mode()
                self.do_a_360_almost()
               
                   
                if self.rotation>=350:
                    self.register_special_support()
                    self.special_support_state=1
            elif self.special_support_state==1:
                self.rotation=0
                self.special_support_execution_mode=False
                self.camera_y=270
                self.special_support_state=2
                turn_in_progress=False
                next_player()
                
        
    
    def register_special_support(self):
        global last_action,players_class_list
        if self.special_support_type=='waves of order':
            self.hp+=150
            for stat in range(len(self.buff_debuff)):
                if self.buff_debuff[stat]<0:
                    print(stat)
                    self.buff_debuff[stat]=0
            print(self.buff_debuff)
            last_action=f'{self.name} used Waves of Order! 150 p healed and removed all negative effects'
        elif self.special_support_type=='holy wrath':
            for player in players_class_list:
                player.buff_debuff=[-3,-3,-3]
                print(player.buff_debuff)
            last_action=f'{self.name} unleashed Holy Wrath! All party stats hit rock bottom.'
        elif self.special_support_type=='shield of god':
            self.shield_of_god=True
            self.stats['defense']+=10000
            print(self.stats['defense'])
            last_action=f'{self.name} raised Shield of God. All incoming attacks will deal 1 damage.'
    def perform_megido_ark(self):
        if  self.megido_ark_execution_mode and not self.sinai_execution_mode and not self.regular_attack_execution_mode and not self.special_support_execution_mode and not self.support_execution_mode:
            return
        self.megido_ark_execution_mode=True
        self.megido_state=0
    def enemy_update_megido(self):
        global megido_mode,megido_ark_pos,game_end_flag,last_action,win
        if self.megido_ark_execution_mode:
            if self.megido_state==0:
                self.zoomed_mode()
                self.raise_sword()
                if self.sword_angle>=-10:
                    self.megido_state=1
                    megido_mode=True
                    
                    
            elif self.megido_state==1:
                print('enter')
                
                self.camera_y=370
                megido_ark_pos[2]-=2
                if megido_ark_pos[2]<=-20:
                    self.megido_state=2
                    for player in players_class_list:
                        player.player_hp=0
                        player.game_end_condition_player=1
                        player.regular_condition_player=0
                        player.rotation=90
                    

            elif self.megido_state==2:
                self.megido_ark_execution_mode=False
                megido_mode=False
                self.megido_state=3
                game_end_flag=True
                win=False
                last_action=f'{self.name} used Megido Ark since 12 turn cycles has passed'
                
                    


        
    def alive_check(self):
        for player in [p1, p2, p3, p4]:
            if player.player_hp < 0 and player.alive_status:
                player.player_hp = 0
                player.regular_condition_player = 0
                player.game_end_condition_player = 1
                player.alive_status = False
                player.rotation = 90
                print(f"{player.name} is now dead")




                
                    
               



    def draw(self):
        global regular_condition,game_end_condition
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)  # Translate to the character's position

        # Inverse rotation to make the character face forward at -180
        # When self.rotation = -180, it should be treated as 0
        
        glRotatef(self.rotation, 0, game_end_condition, regular_condition)  # Inverted rotation to correct the orientation

        # === TORSO ===
        glColor3f(0.6, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(0, 0, 90)  # Move the torso up along the z-axis
        glScalef(1, 0.5, 2)  # Scale the torso
        glutSolidCube(60)
        glPopMatrix()

        # === HEAD ===
        glColor3f(92/256, 64/256, 64/256)
        glPushMatrix()
        glTranslatef(0, 0, 160)  # Move the head above the torso
        glutSolidCube(30)
        glPopMatrix()

        # === EYES ===
        glColor3f(self.eye_color, 0, 0)
        glPushMatrix()
        glTranslatef(-8, 15, 160)  # Position for the left eye
        glutSolidSphere(4, 10, 10)
        glTranslatef(16, 0, 0)  # Position for the right eye
        glutSolidSphere(4, 10, 10)
        glPopMatrix()

        # === RIGHT ARM (Sword arm) ===
        glColor3f(0.7, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(50, 0, 90)  # Position for the right arm
        glRotatef(-5, 0, 0, 1)  # Rotate the right arm by -5 degrees along the z-axis

        # Hand
        glPushMatrix()
        glTranslatef(0, 0, 40)  # Position for the hand
        glRotatef(190, 0, 0, 1)  # Rotate hand
        glScalef(0.7, 0.7, 0.7)
        glutSolidCube(25)
        glPopMatrix()

        # Sword
        glColor3f(self.sword_color[0], self.sword_color[1], self.sword_color[2])
        glPushMatrix()
        glTranslatef(10, 0, 50)  # Position for the sword
        glRotatef(self.sword_angle, 1, 0, 0)  # Rotate sword along the x-axis
        gluCylinder(gluNewQuadric(), 4, 4, self.sword_size, 10, 10)
        glPopMatrix()

        glPopMatrix()

        # === LEFT ARM ===
        glColor3f(0.7, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(-40, 0, 100)  # Position for the left arm
        glScalef(0.5, 0.5, 2.5)  # Scale the left arm
        glutSolidCube(30)
        glPopMatrix()

        # === LEGS ===
        glColor3f(0.7, 0.2, 0.2)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 20, 0, 15)  # Position for the legs
            glScalef(0.6, 0.6, 2.5)  # Scale the legs
            glutSolidCube(30)
            glPopMatrix()

        # === SHOULDER GUNS ===
        glColor3f(1, 1, 0)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 40, -20, 150)  # Position for shoulder guns
            glRotatef(-140, 1, 0, 0)  # Rotate the guns along the x-axis
            gluCylinder(gluNewQuadric(), 5, 5, 55, 10, 10)
            glPopMatrix()

        glPopMatrix()
    def draw_megido(self):
        global megido_ark_pos
        glPushMatrix()
        glTranslatef(megido_ark_pos[0], megido_ark_pos[1], megido_ark_pos[2])
        glColor3f(1, 0, 0)                   # Red bullet
        glutSolidSphere(130, 50, 50)
        glPopMatrix()






    
def initiate_people():

    p1=Player(175,150,500,100,65,50,15)
    p2=Player(58.33,150,425,125,20,55,50)
    p3=Player(-58.33,150,500,150,40,90,32)
    p4=Player(-175,150,350,200,10,57,66)

    p1.name='Demifiend'
    p2.name='Black Rider'
    p3.name='Black Frost'
    p4.name='Norn'

    p1.skill1 = ['Figment Slash', '50 p accuracy, but always critical','physical', 300, 10, 0.5,1]
    p1.skill2 = ['Akashic Arts','heavy phys attack', 'physical', 250, 15, 0.96,0.21]
    p1.skill3 = ['Tarukaja', 'Attack up by one rank','support',0,10,'attack',1,'team']
    p1.skill4 = ['Dekunda', 'Remove all debuffs','support',0,10,'debuff',1,'team']

    p2.skill1 = ['Bufudyne','heavy Ice Damage to one foe', 'magic_ice', 200, 20, 1]
    p2.skill2 = ['Ziodyne','heavy electric damage' ,'magic_electricity',200, 20, 1]
    p2.skill3 = ['Rakukaja', 'Defense up by one rank','support',0,10,'defense',1,'team'] 
    p2.skill4 = ['Makakaja', 'Magic up by one rank','support',0,10,'magic',1,'team'] 


    p3.skill1 = ['Ice Dracostrike','ice-based physcial attack' ,'physical_ice',200,25,0.98,0.21]
    p3.skill2 =['Tarukaja','Attack up by one rank', 'support',0,10,'attack',1,'team'] 
    p3.skill3 = ['Rakunda','Downs enemy defense by one','support',0,10,'defense',-1,'enemy']
    p3.skill4 = ['Tarunda','Downs enemy attack by one','support',0,10,'attack',-1,'enemy']


    p4.skill1 = ['Mediarama', 'medium recovery to all','support', 0, 20,0,0,'heal']
    p4.skill2 = ['Tarunda','Downs enemy attack by one','support',0,10,'attack',-1,'enemy']
    p4.skill3 = ['Makanda','Downs enemy magic by one','support',0,10,'magic',-1,'enemy']
    p4.skill4 = ['Dekaja','Nullifies enemy buffs','support',0,10,'buff',-1,'enemy']


    p1.resistance={'physical':1, 'fire':0.9,'ice':0,'electricity':2}
    p2.resistance={'physical':1, 'fire':1.5,'ice':0,'electricity':1}
    p3.resistance={'physical':1.2, 'fire':0.7,'ice':0.7,'electricity':1}
    p4.resistance={'physical':0.7, 'fire':1,'ice':1,'electricity':1}


    enemy = Enemy(x=0, y=0, z=30) 
    return p1,p2,p3,p4,enemy
p1,p2,p3,p4,enemy=initiate_people()
players_class_list=[p1,p2,p3,p4]
turn_order=[p1,p2,p3,p4,enemy]
current_player=0

# # enemy.hp=10
# p1.player_hp=200
# p2.player_hp=10
# p3.player_hp=10
# p4.player_hp=10

def next_player():
    global current_player, turn_order, turn_in_progress, game_end_flag, win, regular_condition, game_end_condition, turn_cycles

    # Check game-over condition first
    alive_players = [p for p in players_class_list if p.alive_status and p.player_hp > 0]
    if not alive_players:
        game_end_flag = True
        win = False
        print("All players are dead. Game Over!")
        return
    if enemy.hp <= 0:
        game_end_flag = True
        win = True
        regular_condition = 0
        game_end_condition = 1
        enemy.rotation = 90
        print("Enemy defeated. Victory!")
        return

    # Move to the next player in turn_order
    current_player = (current_player + 1) % len(turn_order)

    # Skip dead players (only check Player objects)
    while isinstance(turn_order[current_player], Player) and (not turn_order[current_player].alive_status or turn_order[current_player].player_hp <= 0):
        print(f"{turn_order[current_player].name} is dead")
        current_player = (current_player + 1) % len(turn_order)
        # Safety check to avoid infinite loop
        if all(not p.alive_status or p.player_hp <= 0 for p in players_class_list) and not isinstance(turn_order[current_player], Enemy):
            game_end_flag = True
            win = False
            print("All players are dead. Game Over!")
            return

    # Handle new turn
    if turn_order[current_player]==enemy:
        turn_cycles += 1
        print(f"Turn cycle: {turn_cycles}")

    if isinstance(turn_order[current_player], Player):
        if turn_order[current_player].guarding:
            print("Guard down")
            turn_order[current_player].guarding = False
            turn_order[current_player].stats['defense'] -= 60
        turn_in_progress = True
    elif isinstance(turn_order[current_player], Enemy):
        turn_in_progress = True
        if not game_end_flag:
            enemy.choose_action()
        if turn_order[current_player].shield_of_god:
            print("Shield of God deactivated")
            turn_order[current_player].shield_of_god = False
            turn_order[current_player].stats['defense'] -= 10000

    print(f"Current Player: {turn_order[current_player].name}")


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
def update_boolets_enemy():
    global enemy_boolet_pos, enemy_boolet_direction

    speed = 2
    print
    for i in reversed(range(len(enemy_boolet_pos))):
        # Move the bullet
        enemy_boolet_pos[i][0] += enemy_boolet_direction[i][0] * speed
        enemy_boolet_pos[i][1] += enemy_boolet_direction[i][1] * speed
        enemy_boolet_pos[i][2] -= enemy_boolet_direction[i][1] * 4

        # Remove the bullet if it goes below a threshold (e.g., z <= 10)
        if enemy_boolet_pos[i][2] <= 10:
            del enemy_boolet_pos[i]
            del enemy_boolet_direction[i]

        
def draw_fiery_background():
    """
    Draws a fiery effect around the mountain using animated gradients.
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    num_segments = 100  # Smoothness of the circular gradient
    outer_radius = GRID_RADIUS * 3  # Extend the fiery effect far beyond the grid

    # Time-based animation for flickering effect
    current_time = time.time()
    flicker_intensity = (math.sin(current_time * 5) + 1) / 2  # Oscillates between 0 and 1

    glBegin(GL_TRIANGLE_FAN)
    # Center of the fiery background (dark red)
    glColor4f(0.8, 0.2, 0.0, 0.8 * flicker_intensity)
    glVertex3f(0, 0, -1)  # Center point

    # Outer fiery gradient (bright orange)
    for i in range(num_segments + 1):
        theta = 2.0 * math.pi * i / num_segments
        x = outer_radius * math.cos(theta)
        y = outer_radius * math.sin(theta)

        # Flickering gradient colors
        glColor4f(1.0, 0.5, 0.0, 0.5 * flicker_intensity)
        glVertex3f(x, y, -1)
    glEnd()

    glDisable(GL_BLEND)

def draw_grid():
    """
    Draws a circular grid with 3 soil-colored rings, 4 red-colored rings, and 3 soil-colored rings.
    """
    num_circles = 10  # Total number of concentric circles
    step_radius = GRID_RADIUS / num_circles  # Radius step for each circle

    # Define colors for the rings
    soil_brown = (0.55, 0.35, 0.25)  # Soil-like brown
    red = (1.0, 0.0, 0.0)           # Bright red

    # Draw concentric rings
    for i in range(1, num_circles + 1):
        radius_inner = (i - 1) * step_radius
        radius_outer = i * step_radius

        # Assign colors based on the ring index
        if i <= 3:  # First 3 rings are soil-colored
            glColor3f(*soil_brown)
        elif 4 <= i <= 7:  # Next 4 rings are red-colored
            glColor3f(*red)
        else:  # Last 3 rings are soil-colored
            glColor3f(*soil_brown)

        # Draw the ring as a quad strip
        glBegin(GL_QUAD_STRIP)
        num_segments = 100  # Smoothness of the circle
        for j in range(num_segments + 1):
            theta = 2.0 * math.pi * j / num_segments
            x_inner = radius_inner * math.cos(theta)
            y_inner = radius_inner * math.sin(theta)
            x_outer = radius_outer * math.cos(theta)
            y_outer = radius_outer * math.sin(theta)
            glVertex3f(x_inner, y_inner, 0)  # Inner vertex
            glVertex3f(x_outer, y_outer, 0)  # Outer vertex
        glEnd()


def draw_circular_wall():
    """
    Draws a sloped circular wall around the grid, creating the illusion of a mountain.
    """
    wall_height = 150  # Height of the wall
    base_radius = GRID_RADIUS * 2  # Radius of the base of the sloped wall
    wall_color = [0.4, 0.3, 0.2]  # Dark rocky color for the wall

    # Set the wall color
    glColor3f(wall_color[0], wall_color[1], wall_color[2])

    # Draw the sloped wall as a cone-like structure
    glBegin(GL_QUAD_STRIP)
    num_segments = 100  # Smoothness of the wall
    for i in range(num_segments + 1):
        theta = 2.0 * math.pi * i / num_segments
        x_outer = GRID_RADIUS * math.cos(theta)
        y_outer = GRID_RADIUS * math.sin(theta)
        x_base = base_radius * math.cos(theta)
        y_base = base_radius * math.sin(theta)

        # Top edge of the wall (near the grid)
        glVertex3f(x_outer, y_outer, 0)

        # Bottom edge of the wall (falling downwards)
        glVertex3f(x_base, y_base, -wall_height)
    glEnd()

    # Add shading to the wall
    glColor3f(0.3, 0.2, 0.1)  # Darker shade for depth
    glBegin(GL_LINE_LOOP)
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        x = GRID_RADIUS * math.cos(theta)
        y = GRID_RADIUS * math.sin(theta)
        glVertex3f(x, y, 0)  # Top edge of the wall
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
def draw_boolet_enemy():
    global enemy_boolet_pos
    # print("Bullet positions:", enemy_boolet_pos)

    # Draw each enemy bullet
    for pos in enemy_boolet_pos:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])  # Move to this bullet's position
        glColor3f(237/256, 98/256, 28/256)                   # Red bullet
        glutSolidSphere(10, 5, 5)            # Radius 10, low-res sphere
        glPopMatrix()





#     glPopMatrix()

# def draw_shapes2():
#     glPushMatrix()
#     glTranslatef(-100, 0, 0)
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

#     # === ARMS ===
#     glColor3f(0.4, 0.4, 0.4)
#     for side in [-1, 1]:
#         glPushMatrix()
#         glTranslatef(side * 50, 0, 90)
#         glScalef(0.5, 0.5, 2.5)
#         glutSolidCube(30)
#         glPopMatrix()

#     # === LEGS ===
#     glColor3f(0.3, 0.3, 0.3)
#     for side in [-1, 1]:
#         glPushMatrix()
#         glTranslatef(side * 20, 0, 15)
#         glScalef(0.6, 0.6, 2.5)
#         glutSolidCube(30)
#         glPopMatrix()

#     # === SHOULDER CANNONS ===
#     glColor3f(1, 1, 0)  # Yellow
#     for side in [-1, 1]:
#         glPushMatrix()
#         glTranslatef(side * 40, -20, 140)
#         glRotatef(-60, 1, 0, 0)
#         gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)
#         glPopMatrix()

#     glPopMatrix()



# def draw_shapes():
#     global sword_angle
#     glPushMatrix()
#     glTranslatef(0, 0, 30)

#     # === TORSO ===
#     glColor3f(0.6, 0.1, 0.1)  # Reddish color for the robot
#     glPushMatrix()
#     glTranslatef(0, 0, 90)
#     glScalef(1, 0.5, 2)  # Wider chest
#     glutSolidCube(60)
#     glPopMatrix()

#     # === HEAD ===
#     glColor3f(0.8, 0.2, 0.2)  # Reddish color for the robot
#     glPushMatrix()
#     glTranslatef(0, 0, 160)
#     glutSolidCube(30)
#     glPopMatrix()

#     # === EYES (Mean looking eyes) ===
#     glColor3f(1, 0, 0)  # Red for the "mean" eyes
#     glPushMatrix()
#     glTranslatef(-8, 15, 160)
#     glutSolidSphere(4, 10, 10)  # Slightly bigger to make them look intense
#     glTranslatef(16, 0, 0)
#     glutSolidSphere(4, 10, 10)
#     glPopMatrix()

#     # === RIGHT ARM === (Sword arm)
#     glColor3f(0.7, 0.2, 0.2)  # Reddish color for the right arm
#     glPushMatrix()
#     glTranslatef(50, 0, 90)  # Start from right shoulder
#     glRotatef(-5, 0, 0, 1)  # Rotate to raise arm upwards

#     # The right hand (palm facing upwards)
#     glPushMatrix()
#     glTranslatef(0, 0, 40)
#     glRotatef(190, 0, 0, 1)  # Positioning the hand in a palm-up position
#     glScalef(0.7, 0.7, 0.7)  # Slightly scaled for hand size
#     glutSolidCube(20)  # Hand
#     glPopMatrix()

#     # Sword in the palm of the right hand
#     glColor3f(0, 1, 0)  # Red blade color
#     glPushMatrix()
#     glTranslatef(0, 0, 50)  # Position the sword further from the body
#     glRotatef(sword_angle, 1, 0, 0)  # Rotate the sword
#     gluCylinder(gluNewQuadric(), 4, 4, 60, 10, 10)  # Sword hilt and blade
#     glPopMatrix()

#     glPopMatrix()

#     # === LEFT ARM === (Sword arm)
#     glColor3f(0.7, 0.2, 0.2)  # Reddish color for the left arm
#     glPushMatrix()
#     glTranslatef(-50, 0, 90)  # Start from left shoulder
#     glScalef(0.5, 0.5, 2.5)  # Arm shape
#     glutSolidCube(30)  # Left arm
#     glPopMatrix()

#     # === LEGS ===
#     glColor3f(0.7, 0.2, 0.2)  # Reddish color for the legs
#     for side in [-1, 1]:
#         glPushMatrix()
#         glTranslatef(side * 20, 0, 15)
#         glScalef(0.6, 0.6, 2.5)
#         glutSolidCube(30)
#         glPopMatrix()

#     # === SHOULDER GUNS === (Gun arm)
#     glColor3f(1, 1, 0)  # Yellow color for the guns
#     for side in [-1, 1]:
#         glPushMatrix()
#         glTranslatef(side * 40, -20, 140)
#         glRotatef(-60, 1, 0, 0)  # Rotate guns to aim downwards
#         gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)  # Gun barrels
#         glPopMatrix()

#     glPopMatrix()







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
    global player_pos,player_rotation,enemy_pos,player_life,game_end_flag,hits,boolets_missed,boolet_pos,boolet_direction,player_life,first_person,camera_pos,cheat_mode,cheat_vision,radian_calc_for_cheat_vision,radian_calc_for_cheat_vision,game_end_condition,regular_condition,last_action,turn_in_progress
    
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # Move forward (W key)
    
    
  
   


    # if key == b'a' and game_end_flag==False and cheat_mode==False:  # Rotate left
    #     p1.rotate(10)

    # if key == b'd' and game_end_flag==False and cheat_mode==False:  # Rotate right
    #     p1.rotate(-10)

    # # Toggle cheat mode (C key)
    if isinstance(turn_order[current_player],Player) and not game_end_flag:
        print(key)
        if key==b'1' and not turn_order[current_player].innermenu_active and not isinstance(turn_order[current_player],Enemy):
            print('attacking')
            # last_action=f'{turn_order[current_player].name} used regular attack'
            turn_order[current_player].perform_action_phys()

        
        elif key==b'2' and not turn_order[current_player].innermenu_active and not isinstance(turn_order[current_player],Enemy):
            # print(p1.innermenu_active)
            turn_order[current_player].innermenu_active=True
            skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3]
        elif key==b'3' and not turn_order[current_player].innermenu_active  :
            turn_order[current_player].guarding=True
            turn_order[current_player].stats['defense']+=60
            last_action=f'{turn_order[current_player].name} guarded, thus increasing defense by 60 points!'
            turn_in_progress=False
            next_player()
        elif key==b'1' and turn_order[current_player].innermenu_active and not isinstance(turn_order[current_player],Enemy):
    
        
            skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3,turn_order[current_player].skill4]
            
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
            # if turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and turn_order[current_player].support_execution_mode==False:
            #         next_player()
            
        elif key==b'2' and turn_order[current_player].innermenu_active:
            
        
            # print('Weakness striked! 30 fire ddamage done')
            skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3,turn_order[current_player].skill4]
        
            if skills[1][2].startswith('physical'):
                last_action=f'{turn_order[current_player].name} used {skills[1][0]}'
                turn_order[current_player].perform_action_phys(2)
            elif skills[1][2].startswith('magic'):
                
                last_action=f'{turn_order[current_player].name} used {skills[1][0]}'
                turn_order[current_player].perform_action_mag(2)
            elif skills[1][2].startswith('support'):
                print(skills)
                last_action=f'{turn_order[current_player].name} used {skills[1][0]}'
                turn_order[current_player].perform_action_support(2)


            turn_order[current_player].innermenu_active=False
            # if turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and turn_order[current_player].support_execution_mode==False:
            #         next_player()
            
        elif key==b'3' and turn_order[current_player].innermenu_active:
            print('raised attacks of all allies by one')
            skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3,turn_order[current_player].skill4]
            
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
            # if turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and turn_order[current_player].support_execution_mode==False:
            #         next_player()
        elif key==b'4' and turn_order[current_player].innermenu_active:
            print('raised attacks of all allies by one')
            skills=[turn_order[current_player].skill1,turn_order[current_player].skill2,turn_order[current_player].skill3,turn_order[current_player].skill4]
            
            if skills[3][2].startswith('physical'):
                last_action=f'{turn_order[current_player].name} used {skills[3][0]}'
                turn_order[current_player].perform_action_phys(4)
            elif skills[3][2].startswith('magic'):
                print(skills)
                last_action=f'{turn_order[current_player].name} used {skills[3][0]}'
                turn_order[current_player].perform_action_mag(4)
            elif skills[3][2].startswith('support'):
                print(skills)
                last_action=f'{turn_order[current_player].name} used {skills[3][0]}'
                turn_order[current_player].perform_action_support(4)


            turn_order[current_player].innermenu_active=False
        elif key==b'0' and turn_order[current_player].innermenu_active:
            
            turn_order[current_player].innermenu_active=False
    
    if key==b'q':
        glutLeaveMainLoop()

 



def specialKeyListener(key, x, y):
    """g
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos,left_arm_angle,right_arm_angle,sword_angle,t
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
        target_x, target_y = p2.position  # Get the target player's position
        delta_x = target_x - enemy.x
        delta_y = target_y - enemy.y
        rad = math.radians(enemy.rotation)
        test=False
        
    
         # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        target_x, target_y = p1.position  # Get the target player's position
        delta_x = target_x - enemy.x
        delta_y = target_y - enemy.y
        rad = math.radians(enemy.rotation)
       
        angle_to_target = math.atan2(delta_y, delta_x)
        enemy.x += 7 * math.cos(angle_to_target)
        enemy.y += 7 * math.sin(angle_to_target)
        enemy.z-=7
       
        
    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global camera_pos,first_person,cheat_mode
    """
    Handles mouse inputs for firing boolets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a boolet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
    #     fire_boolet()

        # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print('yes',cheat_mode)
        if first_person:
           first_person = False
           
                
        else:
            first_person = True
        print(first_person)

    
            
            


def setupCamera():
    global first_person,player_rotation,cheat_vision,cheat_mode,radian_calc_for_cheat_vision,game_end_flag,win,current_player

    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(fovY, 1.25, 0.1, 1500)  
    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()  

    if first_person and not game_end_flag:
        
        # Eye (camera) position on head
        eyeX = (turn_order[current_player].camera_x)
        eyeY = turn_order[current_player].camera_y
        eyeZ = turn_order[current_player].camera_z  # Near head

        # Calculate where to look based on rotation
        distance = 100  # how far to look forward
        rad = math.radians(turn_order[current_player].camera_rotation)
        if isinstance(turn_order[current_player],Enemy):
            rad=rad+ math.pi
        targetX = eyeX + math.sin(-rad) * distance-10
        targetY = eyeY + math.cos(-rad) * distance
        targetZ = eyeZ  # Same Z (horizontal view)

        gluLookAt(eyeX, eyeY, eyeZ,
                  targetX, targetY, targetZ,
                  0, 0, 1)
    # elif first_person and not game_end_flag:
        
    #     # Eye (camera) position on head
    #     eyeX = (turn_order[current_player].camera_x)
    #     eyeY = turn_order[current_player].camera_y
    #     eyeZ = turn_order[current_player].camera_z  # Near head

    #     # Calculate where to look based on rotation
    #     distance = 100  # how far to look forward
    #     rad = math.radians(turn_order[current_player].camera_rotation)
    #     if isinstance(turn_order[current_player],Enemy):
    #         rad=rad+ math.pi
    #     targetX = eyeX + math.sin(-rad) * distance-10
    #     targetY = eyeY + math.cos(-rad) * distance
    #     targetZ = eyeZ  # Same Z (horizontal view)

    #     gluLookAt(eyeX, eyeY, eyeZ,
    #               targetX, targetY, targetZ,
    #               0, 0, 1)
    elif first_person and game_end_flag and win==False:
        
        # Eye (camera) position on head
        eyeX = (enemy.camera_x)
        eyeY = 370
        eyeZ = enemy.camera_z  # Near head

        # Calculate where to look based on rotation
        distance = 100  # how far to look forward
        rad = math.radians(enemy.camera_rotation)
        if isinstance(turn_order[current_player],Enemy):
            rad=rad+ math.pi
        targetX = eyeX + math.sin(-rad) * distance-10
        targetY = eyeY + math.cos(-rad) * distance
        targetZ = eyeZ  # Same Z (horizontal view)

        gluLookAt(eyeX, eyeY, eyeZ,
                  targetX, targetY, targetZ,
                  0, 0, 1)
    elif first_person and game_end_flag and win==True:
        
        # Eye (camera) position on head
        eyeX = (enemy.camera_x)
        eyeY = 300
        eyeZ = enemy.camera_z  # Near head

        # Calculate where to look based on rotation
        distance = 100  # how far to look forward
        rad = math.radians(enemy.camera_rotation)
        
        rad=rad+ math.pi
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
        pitch = math.radians(turn_order[current_player].camera_pitch)  # Vertical rotation (up/down)
        targetZ = eyeZ + math.sin(pitch) * distance  # Adjust target Z to look up/down
    
    # Adjust targetX and targetY for vertical (pitch) tilt
        targetX += math.sin(pitch) * math.sin(-rad) * distance
        targetY += math.sin(pitch) * math.cos(-rad) * distance

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
    at_least_one_alive=False
    for player in players_class_list:

        if player.alive_status==True:
            at_least_one_alive=True
            break
    # print('one alive',at_least_one_alive)
    print(f'playeralive{player.name}',player.alive_status)
    if player.alive_status==False and at_least_one_alive and not game_end_flag:
        next_player()


def idle():
    """
    Idle function that runs continuously:
    - Updates the player's rotation for cheat mode.
    - Updates boolet positions and checks for collisions.
    - Triggers screen redraw for real-time updates.
    """
    global boolet_pos, boolet_direction, boolets_missed, hits, enemy_pos, player_pos, player_rotation, player_life, game_end_flag, cheat_mode,regular_condition,game_end_condition,first_person
    global turn_in_progress

    # if not turn_in_progress:
    #     return  # Skip this frame — waiting for new turn start

    if isinstance(turn_order[current_player],Enemy)==False:
        
        turn_order[current_player].update_phys(enemy_position)
        if isinstance(turn_order[current_player],Enemy)==False:
            turn_order[current_player].update_support()  # Ensure this is here
        if isinstance(turn_order[current_player],Enemy)==False:
            turn_order[current_player].update_mag(enemy_position)
   
    elif isinstance(turn_order[current_player],Enemy):
        turn_order[current_player].enemy_update_regular()
        if isinstance(turn_order[current_player],Enemy):
            turn_order[current_player].enemy_update_sinai()
        if isinstance(turn_order[current_player],Enemy):
            turn_order[current_player].enemy_update_deathbound()
        if isinstance(turn_order[current_player],Enemy):
            turn_order[current_player].enemy_update_support()
        if isinstance(turn_order[current_player],Enemy):
            turn_order[current_player].enemy_update_charging()
        if isinstance(turn_order[current_player],Enemy):
            turn_order[current_player].enemy_update_special_support()
        if isinstance(turn_order[current_player],Enemy):
            turn_order[current_player].enemy_update_megido()
    
    
    # if not isinstance(turn_order[current_player],Enemy):
    #     # print(turn_order[current_player].name,turn_order[current_player].alive_status)
    #     dead_skip(turn_order[current_player])
    update_boolets()     # Move bullets each frame
    draw_boolet() 
    draw_boolet_enemy() 
    update_boolets_enemy()      # Draw them each frame
    glutPostRedisplay()  # Ensure screen updates with the latest changes

def showScreen():
    global pulse,enemy_pos,first_person,camera_pos,player_pos,player_life,megido_mode,turn_cycles,game_end_flag,win
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

    draw_fiery_background()

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    draw_grid()
    draw_circular_wall()
    if p1.player_hp>100:
        draw_text(10, 480, f"{p1.name} HP: {p1.player_hp}", color=[0, 1, 0])  
    else:
        draw_text(10, 480, f"{p1.name} HP: {p1.player_hp}", color=[1.0, 0.647, 0.0]) 
    draw_text(10, 460, f"{p1.name} MP: {p1.player_mp}", color=[0.53, 0.81, 0.92])  
    if p2.player_hp>100:
        draw_text(10+120*1+3, 480, f"{p2.name} HP: {p2.player_hp}", color=[0, 1, 0])  
    else:
        draw_text(10+120*1+3, 480, f"{p2.name} HP: {p2.player_hp}", color=[1.0, 0.647, 0.0]) 
    draw_text(10+120*1+3, 460, f"{p2.name} MP: {p2.player_mp}", color=[0.53, 0.81, 0.92])  
    
    if p3.player_hp > 100:
        draw_text(10 + 120 * 2+3*2, 480, f"{p3.name} HP: {p3.player_hp}", color=[0, 1, 0])
    else:
        draw_text(10 + 120 * 2+3*2, 480, f"{p3.name} HP: {p3.player_hp}", color=[1.0, 0.647, 0.0])

    draw_text(10+120*2+3*2, 460, f"{p3.name} MP: {p3.player_mp}", color=[0.53, 0.81, 0.92])  

    if p4.player_hp>100:
    
        draw_text(10+120*3+3*3, 480, f"{p4.name} HP: {p4.player_hp}", color=[0, 1, 0])  
    else:
        draw_text(10 + 120 * 3+3*3, 480, f"{p4.name} HP: {p4.player_hp}", color=[1.0, 0.647, 0.0])
    draw_text(10+120*3+3*3, 460, f"{p4.name} MP: {p4.player_mp}", color=[0.53, 0.81, 0.92])  
    

    if enemy.hp>700:
        draw_text(10+120*4, 480, f"Metatron HP: {enemy.hp}", color=[0, 1, 0])
    else:
        draw_text(10+120*4, 480, f"Metatron HP: {enemy.hp}", color=[1.0, 0.647, 0.0])
    draw_text(10+120*4, 460-1, f"Current turn cycle: {turn_cycles}", color=[1, 0, 1])
    
    draw_text(10, 460-20, f"Current Player: {turn_order[current_player].name}")
    
    
    # Display game info text at a fixed screen position
    if not isinstance(turn_order[current_player],Enemy):
        if not turn_order[current_player].innermenu_active and game_end_flag==False and turn_order[current_player] in players_class_list and turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and not isinstance(turn_order[current_player],Enemy):
            draw_text(10, 445-23, f"1. Attack")
            draw_text(10, 433-23, f"2. Skill")
            draw_text(10, 421-23, f"3. Guard")

        elif turn_order[current_player].innermenu_active and game_end_flag==False and turn_order[current_player] in players_class_list and turn_order[current_player].action_execution_mode==False and turn_order[current_player].magic_execution_mode==False and not isinstance(turn_order[current_player],Enemy):
            draw_text(10, 445-23, f"1. {turn_order[current_player].skill1[0]}->{turn_order[current_player].skill1[1]}->{turn_order[current_player].skill1[4]} MP")
            draw_text(10, 433-23-1, f"2. {turn_order[current_player].skill2[0]}->{turn_order[current_player].skill2[1]}->{turn_order[current_player].skill2[4]} MP")
            draw_text(10, 421-23-2, f"3. {turn_order[current_player].skill3[0]}->{turn_order[current_player].skill3[1]}->{turn_order[current_player].skill3[4]} MP")
            draw_text(10, 421-23-12-3, f"4. {turn_order[current_player].skill4[0]}->{turn_order[current_player].skill4[1]}->{turn_order[current_player].skill4[4]} MP")
            
            draw_text(10, 421-23-12-12-4, f"0. Go back")
    draw_text(10, 397-23-20-12, f"Last Action Result: {last_action}")
    if  game_end_flag and win==False:
        draw_text(10, 397-23-20-12-50, f"In the end, {p1.name} and his friends were no match for {enemy.name}.Game Over!")
        draw_text(10, 397-23-20-12-50-20, f"Press Q to quit")
    elif game_end_flag and win==True:
        draw_text(10, 397-23-20-12-50, f"With relentless attacks, {p1.name} and his friend triumphed over the great adversary! You win!")
        draw_text(10, 397-23-20-12-50-20, f"Press Q to quit")
    elif not game_end_flag:
        draw_text(10, 397-23-20-12-20, f"Press Q to quit")



    
        

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
    draw_boolet_enemy()
    draw_boolet()
    if megido_mode:
        enemy.draw_megido()

    
        


    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(625, 500)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Metatron's Wrath")  # Create the window
    
    # generate_enemy()  # Generate enemies, initially
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    # glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the boolet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
