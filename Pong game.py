# Import the pygame module

import pygame 

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
 

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

#speeds for objects
pspeed = 1
p1speed = 0
p2speed = 0
xspeed = 1
yspeed = 0

#scores for the players
score1 = 0
score2= 0


#instructions for creating player 1
class Player1(pygame.sprite.Sprite):
    
    #iniitialises the player when the class is called
    def __init__(self):
        
        self.surf = pygame.Surface((25,150))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(30, (SCREEN_HEIGHT/2)))
       
    #fuction within the class that is called every frame
    def update(self, pressed_keys):
        global p1speed
        global pspeed
        
        #allows the player to be moved
        if pressed_keys[K_w]:
            p1speed = pspeed
            self.rect.y = self.rect.y - p1speed

        if pressed_keys[K_s]:
            p1speed = (-1)*pspeed
            self.rect.y = self.rect.y - p1speed
            
            
		#keeps player one on screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
				
		
#instructions for creating player 2
class Player2(pygame.sprite.Sprite):
    #iniitialises the player when the class is called
    def __init__(self):
        
        self.surf = pygame.Surface((25,150))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH-30, (SCREEN_HEIGHT/2)))
        
    #fuction within the class that is called every frame
    def update(self, pressed_keys):
        global p2speed
        global pspeed
        
        #allows the player to be moved
        if pressed_keys[K_UP]:
            p2speed = pspeed
            self.rect.y = self.rect.y - p2speed
            
        if pressed_keys[K_DOWN]:
            p2speed = (-1)*pspeed
            self.rect.y = self.rect.y - p2speed
			
		#keeps player two on screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            

				
#class for the game puck
class Puck(pygame.sprite.Sprite):
    #initialises the puck
    def __init__(self):
        
        self.surf = pygame.Surface([10,10])
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        
	#allows the puck to be updated every frame
    def update(self):
        
        #calls global variables for the speed of the puck
        global xspeed
        global yspeed
        #calls global variables for the player score
        global score1
        global score2
        
        #controls the movement of the puck and stops it leaving the screen
        self.rect.x = self.rect.x + xspeed
        self.rect.y = self.rect.y + yspeed
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH/2
            self.rect.y = SCREEN_HEIGHT/2
            yspeed = 0
            score2 = score2 + 1

        if self.rect.left > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH/2
            self.rect.y = SCREEN_HEIGHT/2
            yspeed = 0
            score1 = score1 + 1
            
        if self.rect.top < 0:
            yspeed = yspeed*(-1)
            
        if self.rect.bottom > SCREEN_HEIGHT:
            yspeed = yspeed*(-1)
            
            
# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#set up players and puck
player1 = Player1()
player2 = Player2()
puck = Puck()



# Variable to keep the main loop running
running = True
 
# Main loop
while running:
# Look at every event in the queue
    for event in pygame.event.get():
        #did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        #did the user release one of the movement keys
        elif event.type == pygame.KEYUP:
            #for each resets the speed
            if event.key == K_w:
                p1speed = 0
                
            if event.key == K_s:
                p1speed = 0
                
            if event.key == K_UP:
                p2speed = 0
                
            if event.key == K_DOWN:
                p2speed = 0
                
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
	

    
	#get the currently pressed keys
    pressed_keys = pygame.key.get_pressed()
	
	#use the update funtion on the players to move the players base on keys pressed
    player1.update(pressed_keys)
    player2.update(pressed_keys)
    puck.update()


	#set screen colour
    screen.fill((0,0,0))
    
    
    #sets up the different parts required for the text
    font = pygame.font.SysFont("Grobold", 36)
    scoreprint = ("Player 1: "+str(score1) + "   Player 2: "+str(score2))
    text = font.render(scoreprint, 1, (255,255,255))
    textRect = text.get_rect(center=(SCREEN_WIDTH/2, 50))
    
    
    #detects if the puck is hititng either of the players so the puck can be reflected
    if puck.rect.left < player1.rect.right and player1.rect.top < puck.rect.bottom and player1.rect.bottom > puck.rect.top:
        xspeed = xspeed*(-1)
        yspeed = p1speed*(-1)
    if puck.rect.right > player2.rect.left and player2.rect.top < puck.rect.bottom and player2.rect.bottom > puck.rect.top:
        xspeed = xspeed*(-1)
        yspeed = p2speed*(-1)
        
	#draw the players, puck and text
    screen.blit(player1.surf, player1.rect)
    screen.blit(player2.surf, player2.rect)
    screen.blit(puck.surf, puck.rect)
    screen.blit(text, textRect)
        
    
	#updates the display
    pygame.display.flip()
	