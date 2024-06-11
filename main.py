# pygame template

import pygame, sys, math, random
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_RIGHT, K_LEFT, MOUSEBUTTONDOWN
#__________________________________
pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

def print_text(text, font, text_colour, text_x, text_y):
    image = font.render(text, True, text_colour)
    screen.blit(image, (text_x, text_y))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Initialize global variables
#______________________________________________
#catherines code for the player
player_x = WIDTH/2
player_y = HEIGHT/2
player_speed = 5
player_width = 60
player_height = 115
white_player = pygame.image.load("white-chess-piece.png").convert_alpha()
player_hp = 100

damage_cooldown = 0

player_bullets = []
bullet_speed = 10
bullet_life = 200

laser_on = False
click = False

dash = 1

enemies = []
enemies_rect = []
enemy_health = 100
enemy_speed = 1
b_x = 0
b_y = 0
e_colour = (0,255,0)
e_rect = (0, 0)

# points system
points = 0
bullet_hit = 10
enemy_kill = 200

# waves
wave = 0

# background
background = pygame.image.load("Untitled drawing.png")

#font 
text_font = pygame.font.SysFont(None, 40, bold = True)
text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

#queen powerup location
queenPUP_x = random.randrange(0, 800)
queenPUP_y = random.randrange(0,700)
queenPUP_list = [
    pygame.Rect(queenPUP_x, queenPUP_y, 2, 5)
]
queenPUP_counter = 0

#health powerup location
healthPUP_x = 70
healthPUP_y = 60
healthPUP_list = [
    pygame.Rect(healthPUP_x, healthPUP_y, 2, 5)
]
healthPUP_counter = 0

#laser powerup location
laserPUP_x = 150
laserPUP_y = 150
laserPUP_list = [
    pygame.Rect(laserPUP_x, laserPUP_y, 2, 5)
]
laserPUP_counter = 0

#rook powerup location
rookPUP_x = 100
rookPUP_y = 100
rookPUP_list = [
    pygame.Rect(rookPUP_x, rookPUP_y, 2, 5)
]
rookPUP_counter = 0

coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (45, 50))
coins = [
    pygame.Rect(100, 255, 23, 23),
    pygame.Rect(600, 333, 23, 23)
]
c_collected = 0
#coin bar
coin_bar_height = 60
coin_bar_width = 200
coin_bar_color = (255, 215, 0)

#inventory bar
inventory_bar_height = 80
inventory_bar_width = 580
inventory_bar_colour = (139, 69, 19) 
slot_measurements = 65
slot_colour = (196, 164, 132)
slot_x = 120

#locations of the slots, testing it for now 
slots = [
    (190, 620),  #1
    (285, 640),  #2
    (370, 640),  #3
    (435, 625),  #4
    (slot_x + 320, 630),  #5
    (slot_x + 400, 630),  #6
    (slot_x + 480, 630),  #7

]

#store 
store_width = 800
store_height = 700
store_colour = (92, 64, 51)
coin_colour = (196, 164, 132)
purchase_slots_width = 150
purchase_slots_height = 250 
og_purchase_x = 25
og_purchase_y = 200
laser_price = 10
queenPUP_price = 30
rookPUP_price = 20 
healthPUP_price = 20

store_open = False
e_key_pressed = False

#locations for the powerups within the store for later purchases used
queen_in_store = pygame.Rect(og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height)
laser_in_store = pygame.Rect(225, og_purchase_y, purchase_slots_width, purchase_slots_height)
rookPUP_in_store = pygame.Rect(425, og_purchase_y, purchase_slots_width, purchase_slots_height)
health_in_store = pygame.Rect(625, og_purchase_y, purchase_slots_width, purchase_slots_height)

#chatgpt
full_slots = [False] * len(slots)

#Maggie variables in main menu
pygame.font.get_default_font()
scene_title_font = pygame.font.SysFont('Courier New', 37)
current_screen = 0

startx = 180
starty = 190
exitx = 540
exity = 190
settingx = 750
settingy = 6
titlex = 300
titley = 6

click_x = 0
click_y = 0
clicked = False

#______________________________________________
# Function to get the next available slot
def get_next_available_slot():
    for i, occupied in enumerate(full_slots):
        if not occupied:
            full_slots[i] = True
            return slots[i]
    return None 

# distance calculator
def calc_dist(x1, y1, x2, y2):
    a = y2 - y1
    b = x2 - x1
    return (a**2 + b**2)**0.5

# vectors calculator
def calc_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1) # chat gpt

def calc_velocity(speed, angle):
    dx, dy = [speed * math.cos(angle), speed * math.sin(angle)]
    return dx, dy

def handle_powerup_collision(powerup_x, powerup_y, counter):
        if pygame.Rect(powerup_x, powerup_y, 80, 80).colliderect(player_rect):
            new_slot = slots[0]
            slots.pop(0)
            if new_slot:
                counter += 1
                powerup_x, powerup_y = new_slot

        return powerup_x, powerup_y, counter

#beta code still in development for the activation of powerups 
def check_powerup_click(mouse_x, mouse_y):
    global queenPUP_counter, rookPUP_counter, healthPUP_counter, laserPUP_counter
    for slot in slots:
        slot_rect = pygame.Rect(slot[0], slot[1], 65, 65)
        if slot_rect.collidepoint(mouse_x, mouse_y):
            if queenPUP_counter > 0 and slot_rect.collidepoint(queenPUP_x, queenPUP_y):
                queenPUP_counter -= 1
            elif rookPUP_counter > 0 and slot_rect.collidepoint(rookPUP_x, rookPUP_y):
                rookPUP_counter -= 1
            elif healthPUP_counter > 0 and slot_rect.collidepoint(healthPUP_x, healthPUP_y):
                healthPUP_counter -= 1
            elif laserPUP_counter > 0 and slot_rect.collidepoint(laserPUP_x, laserPUP_y):
                laserPUP_counter -= 1 
# ---------------------------
# classes

# class player:
#     def__init__(self, x, y, speed, hp):
#         self.x = x1
#         self.y = y
#         self.speed = speed
#         self.hp = hp
    
running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()


    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #vectors for bullet
            if event.button == 1:  # Left mouse button
                click_x, click_y = event.pos
                angle = calc_angle(player_x, player_y, mouse_x, mouse_y)
                dx, dy = calc_velocity(bullet_speed, angle)
                click = True
                if laser_on == False:
                    player_bullets.append([player_x, player_y, dx, dy, bullet_life])

            check_powerup_click(mouse_x, mouse_y)
            if store_open: #code for purchasing the powerups in the store
                if queen_in_store.collidepoint(event.pos): 
                    if c_collected > queenPUP_price:
                        c_collected -=queenPUP_price
                        queenPUP_counter += 1
                        if slots:  #moving the new item to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                queenPUP_x, queenPUP_y = new_slot
                if laser_in_store.collidepoint(event.pos): 
                    if c_collected > laser_price:
                        c_collected -= laser_price
                        laserPUP_counter += 1
                        if slots:  #moving the new laser to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                laserPUP_x, laserPUP_y = new_slot
                if rookPUP_in_store.collidepoint(event.pos): 
                    if c_collected > rookPUP_price:
                        c_collected -= rookPUP_price
                        rookPUP_counter += 1
                        if slots:  #moving the new laser to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                rookPUP_x, rookPUP_y = new_slot
                if health_in_store.collidepoint(event.pos): 
                    if c_collected > healthPUP_price:
                        c_collected -= healthPUP_price
                        healthPUP_counter += 1
                        if slots:  #moving the new laser to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                healthPUP_x, healthPUP_y = new_slot
        elif event.type == pygame.MOUSEBUTTONUP:
            click = False
            laser_on = False


        elif event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    # mouse_x, mouse_y = pygame.mouse.get_pos()

    print(click)    
    
    # WASD movement
    #!! taken from mrgallo site
    keys = pygame.key.get_pressed()
    if player_y > 0:
        if keys[119] == True:  # w
            player_y -= 10 * dash

    if player_x > 0:
        if keys[97] == True:  # a
            player_x -= 10 * dash

    if player_y < HEIGHT-player_height:
        if keys[115] == True:  # s
            player_y += 10 * dash

    if player_x < WIDTH-player_width:
        if keys[100] == True:  # d
            player_x += 10 * dash

      #adding a key press on E to open the store
    if keys[101]:  
        if not e_key_pressed:
            store_open = not store_open
            e_key_pressed = True

        else:
          e_key_pressed = False


    # Catherine's bullet system
    for b in player_bullets:
        b[0] += b[2]
        b[1] += b[3]
        b[4] -= 1
        
    player_bullets_alive = []
    for b in player_bullets:
        if b[4] >= 0:
            player_bullets_alive.append(b)

    player_bullets = player_bullets_alive

    if enemy_health <= 0:
        points += enemy_kill

    # LAZERS!!!!
    if keys[108] == True: # l
        laser_on = True
    
    player_vect = pygame.Vector2(player_x, player_y)
    mouse_vect = pygame.Vector2(mouse_x, mouse_y)
    diff = player_vect - mouse_vect
    diff += player_vect
    diff.scale_to_length(2000)

    # dash
    if keys[109] == True: # l
        dash = 5
    else:
        dash = 1

    # Catherine Enemy beta system

    if keys[112] == True:  # p
        for _ in range(1):
            e_x = random.randrange(0, WIDTH)
            e_y = random.randrange(0, HEIGHT)
            
            enemy = [e_x, e_y, 0, 0, enemy_health] 
            enemies.append(enemy)

            e_rect = pygame.Rect(e_x-10, e_y-10, 20, 20)
            enemies_rect.append(e_rect)

    
    enemies_alive = []
    e_rects = []

    for e in enemies:
        enemy_to_player_dist = calc_dist(player_x, player_y, e[0], e[1])
        enemy_angle = calc_angle(e[0], e[1], player_x, player_y)
        e[2], e[3] = calc_velocity(enemy_speed, enemy_angle)
        e_rect = pygame.Rect(e[0]-10, e[1]-10, 20, 20)
        e_rects.append(e_rect)

        if enemy_to_player_dist != 0:
            if enemy_to_player_dist < 50:
                e[0] += e[2]*3
                e[1] += e[3]*3
            else:
                e[0] += e[2]
                e[1] += e[3]
            #add attack animation
        
        for b in player_bullets:
            b_rect = pygame.Rect(b[0]-2, b[1]-2, 4, 4)
            if b_rect.colliderect(e_rect):
                e[4] -= 10
                b[4] = -1
                points += bullet_hit
        
        if e[4] >= 0:
            enemies_alive.append(e)

    enemies = enemies_alive

    # player 
    player_hitbox = white_player.get_rect()
    player_hitbox.topleft = (player_x, player_y)

    if damage_cooldown <= 0:
        if player_hitbox.collidelist(e_rects) >= 0:
            player_hp -= 10
            damage_cooldown = 20
    elif damage_cooldown > 0:
        damage_cooldown -= 1

    if player_hp <= 0:
        print("dead")

    # waves

    wave


    


    #coins being collected 

# note: code will be added to store the coin in inventory
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height) # !!
    for c in coins: 
        #command found online
        if c.colliderect(player_rect):
            coins.remove(c)
            c_collected += 1

    if queenPUP_y <= 600:
        queenPUP_x, queenPUP_y, queenPUP_counter = handle_powerup_collision(queenPUP_x, queenPUP_y, queenPUP_counter)
    if healthPUP_y <= 600:
        healthPUP_x, healthPUP_y, healthPUP_counter = handle_powerup_collision(healthPUP_x, healthPUP_y, healthPUP_counter)
    if rookPUP_y <= 600:
        rookPUP_x, rookPUP_y, rookPUP_counter = handle_powerup_collision(rookPUP_x, rookPUP_y, rookPUP_counter)
    if laserPUP_y <= 600:
        laserPUP_x, laserPUP_y, laserPUP_counter = handle_powerup_collision(laserPUP_x, laserPUP_y, laserPUP_counter)


    queenPUP_x, queenPUP_y, queenPUP_counter = handle_powerup_collision(queenPUP_x, queenPUP_y, queenPUP_counter)
    healthPUP_x, healthPUP_y, healthPUP_counter = handle_powerup_collision(healthPUP_x, healthPUP_y, healthPUP_counter)
    rookPUP_x, rookPUP_y, rookPUP_counter = handle_powerup_collision(rookPUP_x, rookPUP_y, rookPUP_counter)
    laserPUP_x, laserPUP_y, laserPUP_counter = handle_powerup_collision(laserPUP_x, laserPUP_y, laserPUP_counter)
    # DRAWING
    #_________________________________

#MAIN MENU(Maggie)
    # chessboardImg = pygame.image.load('chessboard.jpg')
    # screen.blit(chessboardImg, (100,100))

    # Scene 1 (Menu screen) chessboard + title
    if current_screen == 0:

        chessboardImg = pygame.image.load('chessboard.jpg')
        # smallchessboard = pygame.transform.scale(chessboardImg, (30,30))

        screen.blit(chessboardImg, (2,-20))
        scene_title = scene_title_font.render('Main Menu', True, (219, 33, 98))
        screen.blit(scene_title, (29, 13))

        pygame.draw.rect(screen, (242, 177, 202), (102,163,262,359))
        pygame.draw.rect(screen, (217, 87, 147), (461,163,262,359))

        #Start Button
        startImg = pygame.image.load('startbutton.png')
        smallstart = pygame.transform.scale(startImg, (102,60))
        screen.blit(smallstart, (startx, starty))
        #Exit Button
        ExitImg = pygame.image.load('exitbutton.png')
        smallexit = pygame.transform.scale(ExitImg, (97,60))
        screen.blit(smallexit, (exitx, exity))

        SettingImg = pygame.image.load('settingsbutton.png')
        smallsetting = pygame.transform.scale(SettingImg, (30,30))
        screen.blit(smallsetting, (settingx, settingy))

        #Title
        titleImg = pygame.image.load('dethroned_title.png')
        bigtitle = pygame.transform.scale(titleImg, (240,160))
        screen.blit(bigtitle, (titlex, titley))


        #check if button clicked
        if (click_x>=startx and click_x<=startx+100) and (click_y>=starty and click_y<=starty+50) and clicked == False:
            print("Start Button CLicked")
            current_screen = 2

        elif (click_x>=exitx and click_x<=exitx+100) and (click_y>=exity and click_y<=exity+50) and clicked == False:
            print("Exit Button Clicked")


            break
        elif (click_x >= settingx and click_x <= settingx +40) and (click_y>=settingy and click_y<=settingy+40) and clicked == False:
            print("Settings Button Clicked")
            current_screen =1


    # Scene 2 (Instructions/setting screen) MARIA ADD UR STUFF HERE
    elif current_screen == 1:

        screen.fill((224, 202, 211)) 
        scene_title = scene_title_font.render('Instructions Screen', True, (242, 17, 109))
        screen.blit(scene_title, (90, 0))

    # Scene 3 (Game)
    elif current_screen == 2:
        white_player = pygame.transform.scale(white_player, (player_width, player_height))

        #queen power up image
        queenPUP = pygame.image.load("queen_powerup.png")
        queenPUP = pygame.transform.scale(queenPUP, (80, 80))

        #health power up image
        healthPUP = pygame.image.load("health_potion.png")
        healthPUP = pygame.transform.scale(healthPUP, (50, 50))

        #rook power up image
        rookPUP = pygame.image.load("rook_potion.png")
        rookPUP = pygame.transform.scale(rookPUP, (50, 50))

        #laser power up image
        laserPUP = pygame.image.load("laser_powerup.png")
        laserPUP = pygame.transform.scale(laserPUP, (70, 70))

        #font 
        text_font = pygame.font.SysFont(None, 40, bold = True)
        text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

         # background
        screen.fill((255, 255, 255))  # always the first drawing command

        # background image
        screen.blit(background, (0,0))

        # draw the pawn image
        pygame.draw.rect(screen, (0, 255, 0), player_hitbox) 

        screen.blit(white_player, (player_x, player_y))

    
        # dummy enemy
        for e in enemies:
            e_rect = pygame.Rect(e[0]-10, e[1]-10, 20, 20)
            pygame.draw.rect(screen, (255, 0, 0), e_rect)    
    
        # laser!!!
        if laser_on == True:
            if click == True:
                pygame.draw.line(screen, (255, 0, 0), (player_x, player_y), (mouse_x, mouse_y), 10)
            else:
                pygame.draw.line(screen, (0, 0, 255), (player_x, player_y), (diff), 1)


        # bullet
        for b in player_bullets:
            b_rect = pygame.Rect(b[0]-2, b[1]-2, 4, 4)
            pygame.draw.rect(screen, (0, 0, 0), b_rect) 


    # Points bar
        print_text(f"{points}", text_font, (0,0,0), 10, 10)
    
    # waves
        print_text(f"WAVE {wave}", text_font, (0,0,0), WIDTH/2, 10)


        #inventory lower bar 
        pygame.draw.rect(screen, inventory_bar_colour, (100, 620, inventory_bar_width, inventory_bar_height))
        pygame.draw.rect(screen, slot_colour, (slot_x, 630, slot_measurements, slot_measurements))
        pygame.draw.rect(screen, slot_colour, (slot_x+80, 630, slot_measurements, slot_measurements))
        pygame.draw.rect(screen, slot_colour, (slot_x+160, 630, slot_measurements, slot_measurements))
        pygame.draw.rect(screen, slot_colour, (slot_x+240, 630, slot_measurements, slot_measurements))
        pygame.draw.rect(screen, slot_colour, (slot_x+320, 630, slot_measurements, slot_measurements))
        pygame.draw.rect(screen, slot_colour, (slot_x+400, 630, slot_measurements, slot_measurements))
        pygame.draw.rect(screen, slot_colour, (slot_x+480, 630, slot_measurements, slot_measurements))

        #coin bar 
        pygame.draw.rect(screen, coin_bar_color, (WIDTH - coin_bar_width, 0, coin_bar_width, coin_bar_height))
        screen.blit(coin_image, (600,5))
        print_text(f"$ {c_collected}", text_font, (0,0,0), 650, 18)

        # Draw coins
        for c in coins:
            screen.blit(coin_image, (c[0],c[1]))

    #draw health potions
        for health_potions in healthPUP_list:
            screen.blit(healthPUP, (healthPUP_x, healthPUP_y))
    
    #draw queen powerups 
        for queen_pups in queenPUP_list: 
            screen.blit(queenPUP, (queenPUP_x, queenPUP_y))

    #draw laser power ups    
        for laser_pups in laserPUP_list: 
            screen.blit(laserPUP, (laserPUP_x, laserPUP_y))
    #draw rook power ups
        for rook_pups in rookPUP_list: 
            screen.blit(rookPUP, (rookPUP_x, rookPUP_y))

    #coding for numbering how many powerups you pick uo 
        for slot in slots: 
            if (queenPUP_x, queenPUP_y) == slot:
                print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), queenPUP_x + 55, queenPUP_y +8)
            if (rookPUP_x, rookPUP_y) == slot:
                print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), rookPUP_x + 55, rookPUP_y +8)
            if(healthPUP_x, healthPUP_y) == slot:
                print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), healthPUP_x + 55, healthPUP_y +8)
            if (laserPUP_x, laserPUP_y) == slot:
                print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), laserPUP_x +55, laserPUP_y + 8)


        # if queenPUP_x == 190 and queenPUP_y == 620:
        #     print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), 250, 630)
        
        # if rookPUP_x == 285 and rookPUP_y == 640:
        #     print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), 330, 630)
        
        # if healthPUP_x == 370 and healthPUP_y == 640:
        #     print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), 410, 630)

        # if laserPUP_x == 435 and laserPUP_y == 625:
        #     print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), 490, 630)
        
    #drawing the store and what they can purchase by pressing E
    if store_open:
        pygame.draw.rect(screen, store_colour, ((WIDTH - store_width) / 2, (HEIGHT - store_height) / 2, store_width, store_height))
        pygame.draw.rect(screen, coin_colour, (300, 600, 200, 50))
        print_text(f"Coins: {c_collected}", text_font, (0, 0, 0), 335,610)
        print_text(f"STORE", text_font, (0, 0, 0), 350,125)

        #queen buy
        pygame.draw.rect(screen, (coin_colour), (og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height))
        screen.blit(queenPUP, (og_purchase_x + 30, og_purchase_y+ 80))
        print_text(f"Queen Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+25, og_purchase_y)
        screen.blit(coin_image, (og_purchase_x + 15, og_purchase_y+ +200))
        print_text(f"{queenPUP_price}", text_font, (0, 0, 0), og_purchase_x+70, og_purchase_y+210)

        #laser pup buy
        pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 200, og_purchase_y, purchase_slots_width, purchase_slots_height))
        screen.blit(laserPUP, (og_purchase_x + 230, og_purchase_y+ 80))
        print_text(f"Laser Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+230, og_purchase_y)
        screen.blit(coin_image, (og_purchase_x + 210, og_purchase_y+ +200))
        print_text(f"{laser_price}", text_font, (0, 0, 0), og_purchase_x+265, og_purchase_y+210)


        #rook pup buy
        pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 400, og_purchase_y, purchase_slots_width, purchase_slots_height))
        screen.blit(rookPUP, (og_purchase_x + 430, og_purchase_y+ 80))
        print_text(f"Rook Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+425, og_purchase_y)
        screen.blit(coin_image, (og_purchase_x + 415, og_purchase_y+ +200))
        print_text(f"{rookPUP_price}", text_font, (0, 0, 0), og_purchase_x+470, og_purchase_y+210)
        
        #health pup buy
        pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 600, og_purchase_y, purchase_slots_width, purchase_slots_height))
        screen.blit(healthPUP, (og_purchase_x + 630, og_purchase_y+ 80))
        print_text(f"Health Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+625, og_purchase_y)
        screen.blit(coin_image, (og_purchase_x + 615, og_purchase_y+ +200))
        print_text(f"{healthPUP_price}", text_font, (0, 0, 0), og_purchase_x+665, og_purchase_y+210)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
