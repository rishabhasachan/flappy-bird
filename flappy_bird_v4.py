import pygame, sys, random

# taking 2 same images side by side with 500 width, for movement effect
def draw_base():
    screen.blit(base_surf, (base_x_pos,500))
    screen.blit(base_surf, (base_x_pos + 500,500))
    
#setting up and bottom pipes with equal gap in between them having random positions
def create_pipe():
    random_pipe_height = random.choice(pipe_height)                                   # choose among pipe_heights
    bottom_pipe = pipe_surf.get_rect(midtop = (700,random_pipe_height))               # midtop point will be right side at starting 
    top_pipe = pipe_surf.get_rect(midbottom = (700,random_pipe_height-200))
    return bottom_pipe, top_pipe


# takes pipe_list of rectangle and move left
def move_pipes(pipeList):
    for pipe in pipeList:
        pipe.centerx -= 5
    return pipeList

	
def draw_pipes(pipeList):
    for pipe in pipeList:
        if pipe.top <= 0: 
            flip_pipe_surf = pygame.transform.flip(pipe_surf,False,True)               # False: as we do not want any flip in x direction
            screen.blit(flip_pipe_surf, pipe)
        else:
            screen.blit(pipe_surf, pipe)
    return pipeList

	
def collision(pipeList):
    global can_score              # when we can score
    # collision with pipes
    for pipe in pipeList:
        if bird_rect.colliderect(pipe):       #colliderect() test if two rectangles overlap
            hit_sound.play()
            can_score = True
            return False

# collision with top and bottom
    if bird_rect.top <= 0 or bird_rect.bottom >=510:
        hit_sound.play()
        can_score = True
        return False                                    # game not active

    return True                                         # game active

def rotate_bird(bird):
    bird_rot = pygame.transform.rotozoom(bird, -bird_mov * 3, 1)     #rotozoom is used for scaling and rotating the surface rotozoom(surface,rotation,scaling)
    return bird_rot

def level_display():
    level_surf = game_font.render(f'Level : {int(level)}', True, (255,255,255)) # True for sharper text 
    level_rect = level_surf.get_rect(center = (70, 50))
    screen.blit(level_surf, level_rect)
    
def score_display(game_state):
    if game_state == 'game_active':
        score_surf = game_font.render(f'Score : {int(score)}', True, (255,255,255))                 # True for sharper text 
        score_rect = score_surf.get_rect(center = (400, 50))
        screen.blit(score_surf, score_rect)
        
    if game_state == 'game_over':
        score_surf = game_font.render(f'Score : {int(score)}', True, (255,255,255))
        score_rect = score_surf.get_rect(center = (240, 50))
        screen.blit(score_surf, score_rect)

        high_score_surf = game_font.render(f'High score : {int(high_score)}', True, (255,255,255)) 
        high_score_rect = high_score_surf.get_rect(center = (240, 450))
        screen.blit(high_score_surf, high_score_rect)

def max_score():
#reading file to get current high score of a game
    with open('score.txt','r') as f:
        lines = f.readlines()
        score = lines[0].strip()   
        score = int(score)
    return score;

def update_high_score(score, high_score):
    high_score = max_score()                       #getting score from function max_score() and compare with current score to update high score in scores.txt        

    with open('score.txt', 'w') as f:
        if score > high_score:
            high_score = score
            f.write(str(int(high_score)))
        else:
            f.write(str(int(high_score)))
    return high_score
	
def pipe_score_check():
    global score, can_score 
	
    if pipe_list:
        for pipe in pipe_list:
            if 150 < pipe.centerx <160  and can_score:       # when pipe crosses this pixel which actually seems that bird crosses pipe then score increases by one
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True
      
#initiate pygame
pygame.init()

# main screen
screen = pygame.display.set_mode((500, 600))

# to get control over frame rates, so that system work properly, we need to create Clock object
clock = pygame.time.Clock()

# font
game_font = pygame.font.Font('04B_19.ttf', 25)

# Game Variables
gravity = 0.20
bird_mov = 0
game_active = False                      # for game over logic, bird and pipe only visible when game_active is True 
score = 0
high_score = max_score()
can_score = True
level=1

# background image
bg_surf = pygame.image.load('img/bg2.png').convert()         #converts the image in the convenient form for pygame efficiency

# base/floor surface image
base_surf = pygame.image.load('img/base2.png').convert()
base_x_pos = 0                                               # for base movement

# bird
bird_surf = pygame.image.load('img/bluebird-downflap.png').convert_alpha()          # to remove background rect during rotating bird
bird_rect = bird_surf.get_rect(center = (200,200))                                  # takes rectangle around bird surface for placing and collision detection

# pipes
pipe_surf = pygame.image.load('img/pipe-red.png')
pipe_list = []                                          # to store pipes
SPAWNPIPE = pygame.USEREVENT                            # this event triggers based on time set
pygame.time.set_timer(SPAWNPIPE, 2200)                  # after 1200 ms it will triger, using this to generate pipes after every 1200 ms
pipe_height = [260,350,450]

# message/ game over screen
message_surf = pygame.image.load('img/intro2.png').convert_alpha()
message_rect = message_surf.get_rect(center = (250,220))


# Sounds and Music
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# main loop
while True:
	#look for all the event going on like key press, closing the window etc.
    for event in pygame.event.get():
       
        # check for screen close
        if event.type == pygame.QUIT:
            pygame.quit()                    # uninitializing the game
            sys.exit()                       # exit system module
			
		# check if any key is pressed
        if event.type == pygame.KEYDOWN:
            
            # game active logic
            if event.key == pygame.K_SPACE and game_active == True:
                bird_mov = 0                                          # to correct the movement
                bird_mov -= 7                                         # to fly bird
                flap_sound.play()
				
            # game over logic
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center=(200,200)
                bird_mov = 0
                score = 0

        if event.type == SPAWNPIPE:
            # create new pipe in pipe_list and extend 
            pipe_list.extend(create_pipe())

            if(score == 0):
                level=1
                pygame.time.set_timer(SPAWNPIPE, 2200)
            if(score == 5):
                level=2
                pygame.time.set_timer(SPAWNPIPE, 1200)
            if(score == 10):
                level=3
                pygame.time.set_timer(SPAWNPIPE, 800)
           
    # show bg_surface in screen
	# blit - Draw the image on the screen at the given position.
    screen.blit(bg_surf, (0,0))
    


# bird and pipe are only visible when game_active is True. other things are visible always
    if game_active:
        # Bird movement
        bird_mov += gravity # incresing
        rotated_bird = rotate_bird(bird_surf)
        bird_rect.centery += bird_mov                   # bird moves down
        screen.blit(rotated_bird, bird_rect)

        # check collision detection, if collision is detected then game_active will be false
        game_active = collision(pipe_list)

        # Pipe movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # score
        pipe_score_check()
        score_display('game_active')

	#level
        level_display()
    else:
        screen.blit(message_surf, message_rect)
        high_score = update_high_score(score, high_score)
        score_display('game_over')
        
    
    
    # for base floor movement effect
    base_x_pos -= 1
    draw_base()
    if base_x_pos <= -500:           # <= is for safer side
        base_x_pos = 0
        
 
    # take everything in the loop and draw in screen
    pygame.display.update()

    # add FPS using clock object
    clock.tick(80)                       # FPS <= value so FPS can be < value baised on how much stuff is on the screen
   
