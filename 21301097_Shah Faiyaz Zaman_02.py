from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 
from time import time


########################### Game Parameters and Score  ###############################################
delta=0 #initial delta, delta is updated determining run times of everytime update_diamond function is called, i.e. every frame
score=0
speed=0.09+delta
catcher_speed=5+delta  #initial speeed of catcher and diamond plus delta
pause=False
game_end_flag=False
collision=False  #to prevent multiple readings for one score a collision flag is kept
##################  DIAMOND AND BOX ####################################
rectangle_coord=[]
catcher_box=[]
def generate_catcher_box():
    global catcher_box
    line1= MPLA_main(-50,-385,50,-385)
    line2=MPLA_main(-50,-385,-40,-397)
    line3=MPLA_main(-40,-397,40,-397)
    line4=MPLA_main(40,-397,50,-385)
    color=(1,1,1)
    catcher_box=[line1,line2,line3,line4,color]
def generate_diamond():
    global rectangle_coord,collision
    colors = [(255/255, 0/255, 0/255), (255/255, 165/255, 0/255), (255/255, 255/255, 0),(0, 255/255, 0),(0, 255/255, 255/255), (0, 0, 255/255),  (75/255, 0, 130/255),(238/255, 130/255, 238/255),  
    (255/255, 20/255, 147/255),   
    (255/255, 105/255, 180/255),   
    (255/255, 215/255, 0),     
    (255/255, 105/255, 180/255),   
    (124/255, 252/255, 0),     
    (255/255, 69/255, 0),    
    (255/255, 255/255, 255/255)] 
    x_center = random.randint(-190, 190)
    line1=MPLA_main(x_center-10,335,x_center,350)
    line2=MPLA_main(x_center,350,x_center+10,335)
    line3=MPLA_main(x_center+10,335,x_center,320)
    line4=MPLA_main(x_center,320,x_center-10,335)
    rectangle_coord=[line1,line2,line3,line4,random.choice(colors)]
#########################     NECESSARY DRAWING AND COORDINATE ALGORITHM      ######################################
# freeze=False
W_Width, W_Height = 400,800
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b
def MPLA_main(x_start,y_start,x_end,y_end):
    def zone_finder(dx,dy):
        if dx>0 and dy>0:
            if abs(dx)>abs(dy):
                return 0
            else:
                return 1
        elif dx<0 and dy>0:
            if abs(dx)>abs(dy):
                return 3
            else:
                return 2
        elif dx<0 and dy<0:
            if abs(dx)>abs(dy):
                return 4
            else:
                return 5
        elif dx>0 and dy<0:
            if abs(dx)>abs(dy):
                return 7
            else:
                return 6
        if dx==0:
            return 'vertical'
        elif dy==0:
            return 'horizontal'
    def Convert2Zero(x,y,zone):
        if zone==0:
            return x,y
        elif zone==1:
            return y,x
        elif zone==2:
            return y,-x
        elif zone==3:
            return -x,y
        elif zone==4:
            return -x,-y
        elif zone==5:
            return -y,-x
        elif zone==6:
            return -y,x
        elif zone==7:
            return x,-y
    
    def Convert2Original(x,y,zone):
        if zone==0:
            return x,y
        elif zone==1:
            return y,x
        elif zone==2:
            return -y,x
        elif zone==3:
           return -x,y 
        elif zone==4:
            return -x,-y 
        elif zone==5:
            return -y,-x
        elif zone==6:
            return y,-x
        elif zone==7:
            return x,-y
    points=[]
    dx_init=x_end-x_start
    dy_init=y_end-y_start
    zone=zone_finder(dx_init,dy_init)
    if zone!='vertical' and zone!='horizontal':
        x_end_orignal=x_end
        y_end_original=y_end
        x_start,y_start=Convert2Zero(x_start,y_start,zone)
        x_end,y_end=Convert2Zero(x_end,y_end,zone)
        dx_new=x_end-x_start
        dy_new=y_end-y_start
        d_init=2*dy_new-dx_new
        x_new,y_new=Convert2Original(x_start,y_start,zone)
        points.append([x_new,y_new])
        while points[len(points)-1][0]!=x_end_orignal or points[len(points)-1][1]!=y_end_original:
            if d_init<0:
                x_start+=1
                d_init=d_init+2*dy_new
            else:
                x_start+=1
                y_start+=1
                d_init=d_init+2*dy_new-2*dx_new
            x_new,y_new=Convert2Original(x_start,y_start,zone)
            points.append([x_new,y_new])
    elif zone=='vertical':
        points.append([x_start,y_start])
        while points[len(points)-1][1]!=y_end:
                if y_start>y_end:
                    y_start-=1
                elif y_start<y_end:
                    y_start+=1
                points.append([x_start,y_start])
    elif zone=='horizontal':
        points.append([x_start,y_start])
        while points[len(points)-1][0]!=x_end:
                if x_start>x_end:
                    x_start-=1
                elif x_start<x_end:
                    x_start+=1
                points.append([x_start,y_start])


    return points
   

##############################################        MENU STUFF         #################################################
line1 = MPLA_main(155, 355, 195, 395) 
line2 = MPLA_main(155, 395, 195, 355)  
cross_coord=[line1,line2]
line1 = MPLA_main(-10, 395, -10, 355) 
line2 = MPLA_main(10, 395, 10, 355)    
pause_coord=[line1,line2]
line1 = MPLA_main(15, 375, -10, 395) 
line2 = MPLA_main(15, 375, -10, 355)  
line3 = MPLA_main(-10, 355, -10, 395) 
play_coord=[line1,line2,line3]

line1 = MPLA_main(-155, 375, -195, 375)  
line2 = MPLA_main(-175, 395, -195, 375) 
line3 = MPLA_main(-175, 355, -195, 375)  

reset_coord=[line1,line2,line3]

################################################################################################################

#######################          DRAW AND UPDATE- MAIN LOGIC              ############################


def draw_axes(): #helper function during coding, not part of actual task
    glBegin(GL_LINES)
    glColor3f(0,1,0) 
    glVertex2f(-200, 0) 
    glVertex2f(200, 0)
    glVertex2f(0, -400) 
    glVertex2f(0, 400)

    glEnd()

def draw_menuUI():
    global cross_coord,pause_coord,pause,play_coord,reset_coord,game_end_flag
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1,0,0)
    for line in cross_coord:
        for i in line:
           glVertex2f(i[0],i[1]) 
    glColor3f(1,1,0)
    if pause==False:
        for line in pause_coord:
            for i in line:
                glVertex2f(i[0],i[1]) 
    else:
        for line in play_coord:
            for i in line:
                glVertex2f(i[0],i[1]) 
    glColor3f(0.53, 0.81, 0.98)
    for line in reset_coord:
        for i in line:
           glVertex2f(i[0],i[1])

    
    glEnd()
           
# def draw_points():
#     line=MPLA_main(-10,-20,-20,70)  
#     glPointSize(2)
#     glBegin(GL_POINTS)
#     glColor3f(random.random(),random.random(),random.random())
#     for i in line:
#         glVertex2f(i[0],i[1])
#     glEnd()


def draw_diamond():
 
    glPointSize(1)
    glBegin(GL_POINTS)
    line1,line2,line3,line4,color=rectangle_coord

    glColor3f(color[0],color[1],color[2])
    for i in line1:
        glVertex2f(i[0],i[1])
    for i in line2:
        glVertex2f(i[0],i[1])
    for i in line3:
        glVertex2f(i[0],i[1])
    for i in line4:
        glVertex2f(i[0],i[1])

    glEnd()

def update_diamond():
    global rectangle_coord,pause,game_end_flag,catcher_box,score,speed,collision,catcher_speed
    
    
    if pause==False and game_end_flag==False:
        for line in rectangle_coord[:len(rectangle_coord)-1]:
            for point in line:
                
                point[1] -= speed
                if point[1] > -200 and point[1] <= 50: #since collision flag was used to prevent multiple readings, it was safe to invert collision status once second diamond is in middle of screen 
                    collision=False

                if rectangle_coord[3][0][1] <= -388 and rectangle_coord[3][0][1]>=-397:
                    border_check_left=round(catcher_box[0][0][0])  
                    border_check_right=round(catcher_box[0][len(catcher_box[0])-1][0]) #top part of box
                    diamond_bottom_right=round(rectangle_coord[2][0][0])
                    diamond_bottom_left=round(rectangle_coord[2][len(rectangle_coord[2])-1][0])  #diamond given a hit box of left most point and right most point, with height being the pointiest one at the bottom
                    if diamond_bottom_left in range (border_check_left,border_check_right+1) or diamond_bottom_right in range (border_check_left,border_check_right+1): #collision confirmed if atleast one point diamond's hit box is in range of catch box's range
                       
                        
                        if collision==False:   # to prevent multiple readings of collision for one single point
                            generate_diamond()  
                            score += 1
                            if speed<=0.199:
                                speed += 0.017  #speed doesnt increase infinitely as difficulty would rise infinitely
                            if catcher_speed<7:
                                catcher_speed+=1  #to cope with addedd difficulty catcher speed also increase, twice only
                                # print(catcher_speed)
                            print(f"Score: {score}")
                            collision = True  
                elif rectangle_coord[3][0][1]<=-402 and rectangle_coord[3][0][1]>=-407: #if the diamond's hitbox not in range of either end of box and goes further down then gameover
                    
                    if collision==False: #prevent for accidental game overs even when a collision occured in previous step
                        print(f"Game Over! Score {score}")
                        # print(border_check_left,border_check_right)
                        # print(diamond_bottom_left,diamond_bottom_right)
                        game_end_flag = True
                        break
                 
             
                     
    else:
        pass #game was paused or game over so no update

        

    glutPostRedisplay()    

def draw_catchbox():
    global catcher_box,game_end_flag
    glPointSize(0.5)
    glBegin(GL_POINTS)
    line1,line2,line3,line4,color=catcher_box
    if game_end_flag==False:
        glColor3f(color[0],color[1],color[2])
    else:
        glColor3f(1,0,0)
    for i in line1:
        glVertex2f(i[0],i[1])
    for i in line2:
        glVertex2f(i[0],i[1])
    for i in line3:
        glVertex2f(i[0],i[1])
    for i in line4:
        glVertex2f(i[0],i[1])

    glEnd()



#############################################################################################################
    






            
################################              INPUT RESPONSE               ##############################################################
  



def mouseListener(button,state,x,y) :
        global pause,game_end_flag,score,speed,delta,catcher_speed
        if (button==GLUT_LEFT_BUTTON) and (state==GLUT_DOWN):  
            x,y=convert_coordinate(x,y)
            if y<400 and y>350:
                if x>-25 and x<25 and pause==False and game_end_flag==False:
                    print("Pausing game")
                    pause=True
                elif x>-25 and x<25 and pause==True:
                    print("Resuming game")
                    pause=False
                elif x>-195 and x<-145:
                    print("Resetting game")
                    generate_diamond()
                    generate_catcher_box()
                    speed=0.09+delta
                    score=0
                    catcher_speed=5+delta
                    game_end_flag=False
                    pause=False
                elif x>150 and x<200:
                    glutLeaveMainLoop()
               

           
        glutPostRedisplay()


def specialKeyListener(key,x,y) :
    global pause,game_end_flag,catcher_box,delta,catcher_speed
    border_check_left=catcher_box[0][0][0]
    border_check_right=catcher_box[0][len(catcher_box[0])-1][0]
    if (key==GLUT_KEY_LEFT) :
        if pause==False and game_end_flag==False:
            for line in catcher_box[:len(catcher_box)-1]:
                for point in line:
                    if border_check_left >= -194:
                        point[0] -= catcher_speed
                    
                   
    if (key==GLUT_KEY_RIGHT):
        if pause==False and game_end_flag==False:
            for line in catcher_box[:len(catcher_box)-1]:
                for point in line:
                    if border_check_right <= 194:
                        point[0] += catcher_speed

    glutPostRedisplay()   

 ##################################################################################################################   

# def keyBoardListener(key,x,y) :
#     global pause
#     if (key==b' ')  and pause!=True:
#         print("Freeze initiated")
#         pause=True
#     elif (key==b' ')  and pause==True:
#         print("Unfreezing screen")
#         pause=False

        
    # glutPostRedisplay()


# def animation(): 
#     global freeze 
#     if (freeze == False): 
#         pass
#     else:
#         pass 

#     glutPostRedisplay()
  

def iterate():
    glViewport(0, 0, 400, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-200, 200, -400, 400, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global delta
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    # draw_axes()
    draw_menuUI()
    draw_diamond()
    draw_catchbox()

    t0 = time()   
    update_diamond()
    t1 = time() 
    delta=t1-t0 #delta calculation


    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(400 ,800) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
generate_diamond()
generate_catcher_box() #initial generation of diamond and catchbox
glutDisplayFunc(showScreen)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)
# glutKeyboardFunc(keyBoardListener)
# glutIdleFunc(animation)
glutMainLoop()