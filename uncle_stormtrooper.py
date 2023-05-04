import pygame
from pygame.locals import *
import sys
import time

#Initialize constructor
pygame.init()

#Adaptive Window dimensions
screen_info = pygame.display.Info()
screen_X = screen_info.current_w
screen_Y = screen_info.current_h

#Create the scene for our game
scene = pygame.display.set_mode((screen_X, screen_Y))
pygame.display.set_caption("Uncle Stormtrooper!")
print("This is a shooting game, so beware! Many monsters lurk in the shadows...")

#Colors
BLUE  = (0, 0, 255)
RED = (255, 100, 100)
LRED   = (255, 204, 203)
GREEN = (0, 255, 0) 
BLACK = (0, 0, 0)
GREY = (36, 36, 36)
WHITE = (255, 255, 255)
SKY_BLUE = (135,206,235)  

#Other constants
FPS = 120
Clock = pygame.time.Clock()

#Our bullet object created upon mouse click 
# Note to self: Look at how the player move function was implemented. This can be helpful in getting the intended bullet functionality.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, aim):
        super().__init__()
        self.color = BLACK
        #self.position = pos
        self.velocity = 18
        self.size = 7,5
        self.rect = pygame.Rect([start_pos[0]+10,start_pos[1] -40],self.size)
        self.x = start_pos[0]+10
        # self.slope = (aim[1] - start_pos[1]) / (aim[0] - start_pos[0])
        # self.y_intercept = start_pos[1]
    
    def update(self):
        # Work on the below code to implement shooting in any direction
        # y_temp = self.y #old y value
        # self.x += self.velocity #update current x 
        # self.y = (self.slope * self.x) + self.y_intercept #update current y
        
        # y = self.y -y_temp  #y offset
        self.x += self.velocity
        self.rect.move_ip(self.velocity, 1)
    def check_collision_box(self, boxes):
        return pygame.sprite.spritecollideany(self,boxes)
    def out_of_screen(self):
        if(self.x>1900): # out of screen
            return True
        return False
    def draw(self,surface):
        pygame.draw.rect(surface, BLACK, self.rect)

class TeleportationBomb(pygame.sprite.Sprite):
    def __init__(self, pos, speed_x, speed_y):
        super().__init__()
        self.image = pygame.image.load("teleportation_bomb.png")
        self.image = pygame.transform.scale(self.image, (screen_X//100, screen_X//100))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # self.speed_x = screen_X//15
        # self.speed_y = screen_Y//

    def update(self):
        # Update the projectile's position based on its speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Check for collisions and handle them

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("storm_trooper.png")
        self.image = pygame.transform.scale(self.image, (75,125))
        self.rect = self.image.get_rect()
        self.rect.center = (50,0) #so the feet should be at y = 700 + 62.5

        self.vert = 25 #vertical jumping ability
        self.v_speed = 0 # vertical speed
        self.speed = 5 #horizontal speed
        self.gravity = 1
        self.onground = True
        self.can_jump = True 
        self.doublejump = False 
        self.facing_left = False
    
    def move(self, x, y):
        self.rect.move_ip([x,y])

    def get_pos(self):
        return self.rect.center
    
    def set_pos(self, x, y):
        self.rect.center = x, y
    
    def jump(self):
        if  self.doublejump:
            self.doublejump = False  #Does not allow the player to double jump more than once
            self.v_speed -= 15
        if self.can_jump:
            self.can_jump = False
            self.doublejump = True  #Allows the player to double jump
            self.v_speed = -self.vert #Apply force upwards

    def update(self, boxes):
        x_movement = 0
        onground = pygame.sprite.spritecollideany(self,boxes)
        # #What keys are currently being pressed?
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_movement = -self.speed
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            x_movement = self.speed
            self.facing_left = False
         #gravity
        if self.v_speed<10 and not onground:
            self.v_speed += self.gravity

        if self.v_speed >0 and onground:
            self.v_speed = 0
            self.doublejump = False
            self.can_jump = True
       
        
        self.move(x_movement,self.v_speed)

    def draw(self,surface):
        if self.facing_left:
            temp_image = pygame.transform.flip(self.image, True, False)
            surface.blit(temp_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

#Object representing the boxes that make up the floor of maps
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.side = screen_X//25
        self.image = pygame.image.load("box_image_collection/box_1.png")
        self.image = pygame.transform.scale(self.image, (self.side, self.side))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #if the box is 50 X 50 then the intersection of feet of player and top of the box should happen at y = 700 + 62.5 + 25

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#This method creates the floor sprites based on the current level
def generate_floor(lvl):
    floor_boxes = pygame.sprite.Group()

    step = screen_X//25 #based on the size of our box sprites
    for box in range(0, screen_X, step):
        if(lvl==1):
            if(box<screen_X/2):
                floor_boxes.add(Box(box, round(screen_Y*0.9)))
            elif(box> screen_X/2):
                floor_boxes.add(Box((box+ (step*2)), round(screen_Y*0.75)))
        elif(lvl==2):
            if(box<screen_X/3):
                floor_boxes.add(Box(box, round(screen_Y*0.75)))
            elif(box> screen_X/2):
                floor_boxes.add(Box((box), round(screen_Y*0.5)))
        elif(lvl==3):
            if(box<screen_X/4):
                floor_boxes.add(Box(box, round(screen_Y*0.5)))
            elif(box> screen_X/4):
                floor_boxes.add(Box((box+step*2), round(screen_Y*0.8)))
                floor_boxes.add(Box((box+step*2), round(screen_Y*0.3)))
        elif(lvl==4):
            if(box<screen_X/4):
                floor_boxes.add(Box((box), round(screen_Y*0.8)))
                floor_boxes.add(Box((box), round(screen_Y*0.3)))
            elif(box> screen_X/3 and box<screen_X/2):
                floor_boxes.add(Box((box+step*4), round(screen_Y*0.5)))
        elif(lvl==5):
            print("")
    return floor_boxes

#Method to display current score
def score_board(scene, score):
    font = pygame.font.SysFont('Corbel', screen_Y//20)
    score_font = font.render("Score: " + str(score) , True , BLACK )
    scene.blit(score_font, ((screen_X/2)- score_font.get_width()/2, screen_Y//20))

#This function handles the start menu view
def start_menu(scene):
    scene.fill(GREY)
    # defining a font 
    font = pygame.font.SysFont('Corbel',screen_Y//20)
    title_font = pygame.font.SysFont('Arial', screen_Y//12)
    sub_title_font = pygame.font.SysFont('Arial', screen_Y//17)
    title = title_font.render('Shoot! Forest, Shoot!!' , True , WHITE)
    sub_title1 = sub_title_font.render('This is a shooting game, so beware! ' , True , GREEN)
    sub_title2 = sub_title_font.render('Many monsters lurk in the shadows...' , True , GREEN)
    start_button = font.render("Press the Spacebar to Start Your Adventure" , True, WHITE)
    scene.blit(title, (screen_X//2 - title.get_width()/2, screen_Y//10))
    scene.blit(sub_title1, (screen_X//2-sub_title1.get_width()/2, screen_Y//10 + 200))
    scene.blit(sub_title2, (screen_X//2-sub_title2.get_width()/2, screen_Y//10 + 270))
    scene.blit(start_button, (screen_X//2 - start_button.get_width()/2, screen_Y//2 + start_button.get_height()))
    pygame.display.update()

#This is shown to the player once the game is over
def game_over(scene, score):
    scene.fill(SKY_BLUE)
    # defining a font 
    font = pygame.font.SysFont('Corbel',screen_Y//17)
    title_font = pygame.font.SysFont('Arial', screen_Y//10)
    title = title_font.render('GAME OVER!' , True , RED)
    # sub_title1 = sub_title_font.render('This is a shooting game, so beware! ' , True , GREEN)
    # sub_title2 = sub_title_font.render('Many monsters lurk in the shadows...' , True , GREEN)
    actions = font.render("Press the Spacebar to Retry or the Esc key to exit" , True, BLACK)
    final_score = font.render("Your score: " + str(score), True, BLACK)
    scene.blit(title, (screen_X//2 - title.get_width()/2, screen_Y//10))
    # scene.blit(sub_title1, (X/2-sub_title1.get_width()/2, 300))
    # scene.blit(sub_title2, (X/2-sub_title2.get_width()/2, 370))
    scene.blit(final_score, (screen_X//2 - final_score.get_width()/2, screen_Y//2 + final_score.get_height() - 100))
    scene.blit(actions, (screen_X//2 - actions.get_width()/2, screen_Y//2 + actions.get_height()))
    pygame.display.update()

#Controller
def main():
    #Set the game state to the start menu
    game_state =  "start_menu"
    scene.fill(SKY_BLUE)
    #Initialize player
    player = Player()
    floor_level = 1 #Player starts at level 1
    floor = generate_floor(floor_level) #Generate the floor for the current level
    alive = True
    bullets = []
    
    # monsters = []
    # monsters.append(Monster([1300,613], 1))

    score = 0

    while alive:
        
        #Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == MOUSEBUTTONDOWN:
            #     # if(len(bullets)<10):
            #         bullets.append(Bullet(player.get_pos(), pygame.mouse.get_pos()))
            #     # else:
            #     #     pygame.event.post(pygame.event.Event(GAMEOVER))
            if event.type == KEYDOWN:
                if game_state == "start_menu" and event.key==K_SPACE:
                    game_state = "game"
                if game_state == "game_over" and event.key==K_SPACE:
                    main()
                if game_state == "game_over" and event.key==K.ESCAPE:
                    pygame.quit()
                    sys.exit()
                if(event.key==K_UP):
                    player.jump()

        if game_state == "start_menu":
            #Display start menu 
            start_menu(scene)
        if game_state == "game_over":
            #Display game over screen 
            game_over(scene, score)
        if game_state == "game":
            scene.fill(SKY_BLUE) #Background color
            score_board(scene, score)
            player.update(floor)
            player.draw(scene)

            #Dray appropriate map based on player location
            floor.draw(scene)
            
            # for bullet in bullets: #TODO: House all of the bullets in a group.
            #     bullet.draw(scene)
            #     bullet.update()
                
            #     if(bullet.check_collision_box(floor[map_section]) or bullet.out_of_screen()): #remove bullet from this array when it collides with the floor of is out of the screen.
            #         bullets.remove(bullet)
            #     for monster in monsters:
            #         if bullet.rect.colliderect(monster.rect):
            #             # remove the bullet and the enemy sprites from their respective lists
            #             bullets.remove(bullet)
            #             monsters.remove(monster)
            #             # increment the score by 10
            #             score += 10
            #Monsters view
            # if(len(monsters)>0):
            #     if(monsters[0].get_pos()[0]<=1180 or monsters[0].get_pos()[0]>(X-50)):
            #         monsters[0].turn()  #Set the path for the first monster
            #     for i in range(len(monsters)):
            #         if(map_section==0 and i==0):
            #             monsters[i].update()
            #             if(pygame.sprite.spritecollideany(player, monsters)):
            #                 game_state = "game_over"
            #             monsters[i].draw(scene)    

            #Update game state and scene based on the player position
            if(player.get_pos()[1]>screen_Y):
                game_state = "game_over"
            if(player.get_pos()[0]>screen_X):
                player.set_pos(50,player.get_pos()[1])
                floor_level += 1
                floor = generate_floor(floor_level) #Generate the floor for the current level
            elif(player.get_pos()[0]<0):
                player.set_pos(screen_X-20, player.get_pos()[1])
                floor_level -= 1
                floor = generate_floor(floor_level) #Generate the floor for the current level
            
            pygame.display.update()
            Clock.tick(FPS)

main()