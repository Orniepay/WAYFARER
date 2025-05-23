import pygame # type: ignore
import random
import sys
import time
from NPCs.tutorial_npc_dialogue import handle_npc_dialogue  # Import the first NPC dialogue functionality
from NPCs.tutorial_npc_2_dialogue import handle_npc_2_dialogue  # Import the second NPC dialogue functionality
from NPCs.tutorial_npc_3_dialogue import handle_npc_3_dialogue  # Import the third NPC dialogue functionality
from NPCs.tutorial_npc_4_dialogue import handle_npc_4_dialogue  # Import the fourth NPC dialogue functionality
import world_select
import json
from saves_handler import *
from firework_level_end import show_level_complete_deaths
from saves_handler import update_unlock_state, get_unlock_state
from pause_menu import PauseMenu  # Import the PauseMenu class

# Initialize PyGame
pygame.init()
pygame.mixer.init() # Initialize Pygame Audio Mixer

# Load the level complete sound 
level_complete_sound = pygame.mixer.Sound("Audio/LevelComplete.mp3")
pygame.mixer.music.set_volume(1.0)  # start at 100% volume 

# Gadget pick up sound 
gadget_sound = pygame.mixer.Sound("Audio/GadgetPickUp.mp3")

# Death sound 
death_sound = pygame.mixer.Sound("Audio/Death.mp3")

# Super speed power up sound
super_speed_sound = pygame.mixer.Sound("Audio/SuperSpeed.mp3")

# Dash power up sound
dash_sound = pygame.mixer.Sound("Audio/Dash.mp3")

# Power up sound (global)
power_up_sound = pygame.mixer.Sound("Audio/PowerUpPickUp.mp3") 

# Coin pick up sound 
coin_sound = pygame.mixer.Sound("Audio/Coin.mp3")

# Screen setting
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better

TILE_SIZE = HEIGHT // 30  # Adjusted for better layout

scale_factor = HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial Level")

ground_tile = pygame.image.load("./images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

platform_tile = pygame.image.load("./images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE, TILE_SIZE))

dirt_tile = pygame.image.load("./images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

background = pygame.image.load("./images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to screen size

tree = pygame.image.load("./images/tree.png")
tree = pygame.transform.scale(tree, (TILE_SIZE * 2, TILE_SIZE * 3))  # Resize tree to fit properly

boots = pygame.image.load("./images/boots.png")
boots = pygame.transform.scale(boots, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

npc_1 = pygame.image.load("./Character Combinations/female ginger hair_white_brown skirt_blue pants.png")
npc_1 = pygame.transform.scale(npc_1, (TILE_SIZE, TILE_SIZE))
flipped_npc_1 = pygame.transform.flip(npc_1, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_2 = pygame.image.load("./Character Combinations/brown hair_white_blue shirt_blue pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))
flipped_npc_2 = pygame.transform.flip(npc_2, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_3 = pygame.image.load("./Character Combinations/ginger hair_white_blue shirt_black pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))
flipped_npc_3 = pygame.transform.flip(npc_3, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_4 = pygame.image.load("./Character Combinations/female ginger hair_white_pink skirt_magenta pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))
flipped_npc_4 = pygame.transform.flip(npc_4, True, False)  # Flip horizontally (True), no vertical flip (False)

house = pygame.image.load("./images/house.png")
house = pygame.transform.scale(house, (TILE_SIZE * 5, TILE_SIZE * 3))

thorn = pygame.image.load("./images/thorn.png")
thorn = pygame.transform.scale(thorn, (TILE_SIZE, TILE_SIZE))

flag = pygame.image.load("./images/flag.png")
flag = pygame.transform.scale(flag, (TILE_SIZE, TILE_SIZE))

super_speed_powerup = pygame.image.load("./images/super_speed_powerup.png")
super_speed_powerup = pygame.transform.scale(super_speed_powerup, (TILE_SIZE, TILE_SIZE))

dash_powerup = pygame.image.load("./images/dash_powerup.png")
dash_powerup = pygame.transform.scale(dash_powerup, (TILE_SIZE, TILE_SIZE))

coin = pygame.image.load("./images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

fence = pygame.image.load("./images/fence.png")
fence = pygame.transform.scale(fence, (TILE_SIZE, TILE_SIZE // 2))

sign = pygame.image.load("./images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

rock = pygame.image.load("./images/rock.png")
rock = pygame.transform.scale(rock, (TILE_SIZE, TILE_SIZE // 2))

background_tree = pygame.image.load("./images/background_tree.png")
background_tree = pygame.transform.scale(background_tree, (TILE_SIZE * 1.5, TILE_SIZE * 2))


level_almost_complete_popup = pygame.image.load("./images/level_near_completion_pop_up.png")
level_almost_complete_popup = pygame.transform.scale(level_almost_complete_popup, (250, 60))


level_almost_complete_font = pygame.font.Font('PixelifySans.ttf', 10)
keep_heading_right_font = pygame.font.Font('PixelifySans.ttf', 10)
level_almost_complete_text = level_almost_complete_font.render("Tutorial Level Almost Complete!", True, (255, 255, 255))
keep_heading_right_text = keep_heading_right_font.render("Keep Heading Right!", True, (255, 255, 255))



pop_up_x = WIDTH - (WIDTH * .20)
pop_up_y = HEIGHT - (HEIGHT * .95)



level_almost_complete_rect = level_almost_complete_text.get_rect(center=(pop_up_x + 140, pop_up_y + 18))
keep_heading_right_rect = keep_heading_right_text.get_rect(center=(pop_up_x + 140, pop_up_y + 38))



#-----Gadget inventory images and dictionary

inventory = pygame.image.load("./images/inventory_slot_opacity.png").convert_alpha()
inventory = pygame.transform.scale(inventory, (250, 70))
inventory_x = (WIDTH - 250) // 2
inventory_y = HEIGHT - 100

inventory_jump_boots = pygame.image.load("./images/boots.png")
inventory_jump_boots = pygame.transform.scale(inventory_jump_boots, (42, 50))

inventory_speed_boots = pygame.image.load("./images/speed_boots.png")
inventory_speed_boots = pygame.transform.scale(inventory_speed_boots, (42, 50))

INV_SLOT_WIDTH = 42
INV_SLOT_HEIGHT = 45

first_slot = (inventory_x + 5, inventory_y + 10)
second_slot = (inventory_x + INV_SLOT_WIDTH + 10, inventory_y + 10)

# The inventory will initially be empty
# inventory_slots = {0: inventory_jump_boots, 1: inventory_speed_boots, 2: None, 3: None, 4: None}
# inventory_conditions = {0: double, 1: False, 2: False, 3: False, 4: False}

# Set up the level with a width of 140 and a height of 40 rows
level_width = 140
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

# This is for the snowflake animations
WHITE = (255, 255, 255)
NUM_SNOWFLAKES = 100
snowflakes = []

#This for loop is also for snowflakes
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 6)  # Random size
    speed = random.uniform(1, 6)  # Falling speed
    x_speed = random.uniform(-0.5, 0.5)  # Small horizontal drift
    snowflakes.append([x, y, size, speed, x_speed])

for row_index in range(GROUND, level_height):  # Only draw ground from row 23 down
    row = [1] * level_width  # Default to full ground row
    if row_index >= 10:  # At row 10 and below, create a pit
        for col_index in range(20, 25):  # Remove ground in columns 20-25
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(70, 85):
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(115, 120):
            row[col_index] = 0  # Set to air (pit)
    level_map[row_index] = row  # Add row to level map

# Add solid ground at the very bottom
level_map.append([1] * level_width)

for row_index in range(SURFACE - 4, GROUND): #Raised Ground
    level_map[row_index][35:40] = [1] * 5

level_map[SURFACE - 4][53:58] = [2] * 5   # Platform containing speed boots
level_map[SURFACE - 1][74:76] = [2] * 2   # Platform

for row_index in range(SURFACE - 1, GROUND): #Raised Ground
    level_map[row_index][123:126] = [1] * 3
for row_index in range(SURFACE - 2, GROUND): #Raised Ground
    level_map[row_index][126:128] = [1] * 2
for row_index in range(SURFACE - 6, GROUND): #Raised Ground
    level_map[row_index][128:140] = [1] * 12

level_map[SURFACE - 5][122:124] = [2] * 2 # Platform

# Make terrain before this line. The next code block calculates the ground levels

# Find the ground level for each column
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

# All code after this line should be for props, npcs, gadgets, and powerups. Terrain should not be made here.

# Dictionary containing which tile corresponds to what
tiles = {1: ground_tile, 2: platform_tile, 3: boots, 4: flipped_npc_1, 5: house, 6: thorn, 7: flag, 8: super_speed_powerup, 9: dash_powerup, 
        10: fence, 11: sign, 12: npc_1, 13: speed_boots, 14: coin, 15: npc_2, 16: npc_3, 17: flipped_npc_2, 18: flipped_npc_3, 19: npc_4, 20: flipped_npc_4}

level_map[SURFACE][60] = 4 # NPC 1
level_map[SURFACE][27] = 17 # NPC 2
level_map[SURFACE][86] = 18 # NPC 3
level_map[SURFACE][8] = 20 # NPC 4
level_map[SURFACE-2][62] = 5 # House

level_map[SURFACE][98:104] , level_map[SURFACE][113:115]= [6] * 6, [6] * 2 # Thorns
level_map[SURFACE-5][37], level_map[SURFACE][87] = 7,7 # Flag

level_map[SURFACE][95] = 8 # Super speed powerup
level_map[SURFACE-2][113] = 9 # Dash powerup

level_map[SURFACE-6][122:124] = [10] * 2 # Fence
level_map[SURFACE-7][135:140] = [10] * 5 # Fence

level_map[SURFACE-7][130] = 11 # Sign

rocks = {14, 33, 45, 68, 108, 124} # Column numbers for all the rocks
trees = {10, 30, 50, 90} # Column numbers for all the trees
background_trees = {16, 42, 55, 93, 133} # Column numbers for all the background trees

# Converts the x coordinates to the column on the map
def calculate_column(x): 
    return int(x // TILE_SIZE)

# Converts the column number to the x-coordinate
def calculate_x_coordinate(column):
    return int(column * TILE_SIZE)

# Converts the y coordinate to the row on the map
def calculate_row(y):
    return int(y // TILE_SIZE)

# Converts the row number to the y-coordinate
def calculate_y_coordinate(row):
    return int(row * TILE_SIZE)

def show_level_completed_screen(slot: int, death_count: int):
    level_map[SURFACE][28] = 3 # Respawn double jump boots
    level_map[SURFACE-5][55] = 13 # Respawn speed boots
    level_map[SURFACE-1][68] = 0  # Despawn coin
    level_map[SURFACE-2][79:81] = [0] * 2 # Despawn platforms after getting coin


    respawn_powerups() # Respawn all powerups on the level

    update_save(slot, {"Tutorial Checkpoint": 0}) # Set checkpoint to 0

    current_state = get_unlock_state(slot, "map1")
    current_state[1] = True  # Unlock level 1
    update_unlock_state(slot, current_state, "map1")
    
    level_name = "Tutorial"

    show_level_complete_deaths(slot, 0, death_count, level_name, background)

def respawn_gadgets():
    level_map[SURFACE][28] = 3 # Jump Boots
    level_map[SURFACE-5][55] = 13 # Speed Boots

def respawn_powerups():
    level_map[SURFACE][95] = 8 # Super speed powerup
    level_map[SURFACE-2][113] = 9 # Dash powerup

# Initialize the PauseMenu
pause_menu = PauseMenu(screen)

# Function to run the tutorial level
def tutorial_level(slot: int):

    respawn_gadgets()
    respawn_powerups() # Respawn all powerups on the level

    # Stop any previously playing music 
    pygame.mixer.music.stop()
    
    # Load the tutorial music
    pygame.mixer.music.load("Audio/TutorialLevel.mp3")
    pygame.mixer.music.play(-1)  # -1 loops forever

    # Grab the sprite that was customized
    sprite = load_save(slot).get("character")

    # Load all the images into their respective variables
    player = pygame.image.load(f"./Assets/Character Sprites/standing/{sprite}")
    player = pygame.transform.scale(player, (TILE_SIZE, TILE_SIZE))
    flipped_player = pygame.transform.flip(player, True, False)

    run = pygame.image.load(f"./Assets/Character Sprites/running/{sprite}")
    run = pygame.transform.scale(run, (TILE_SIZE, TILE_SIZE))
    flipped_run = pygame.transform.flip(run, True, False)

    run_frames = [
        pygame.image.load(f"./Assets/Character Sprites/walking/{sprite}"),
        pygame.image.load(f"./Assets/Character Sprites/running/{sprite}")
    ]

    run_frames = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in run_frames]

    checkpoints = [(calculate_x_coordinate(4), calculate_y_coordinate(SURFACE)), (calculate_x_coordinate(37), calculate_y_coordinate(SURFACE-5)), (calculate_x_coordinate(87), calculate_y_coordinate(SURFACE))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_idx = load_save(slot).get("Tutorial Checkpoint")
    if not checkpoint_idx:
        checkpoint_idx = 0
    for i in range(checkpoint_idx+1):
        checkpoint_bool[i] = True

    coin_locations = [(calculate_x_coordinate(68), calculate_y_coordinate(SURFACE-1))]
    coin_picked_up = load_save(slot).get("Tutorial Coins")
    if not coin_picked_up:
        coin_picked_up = [False] * len(coin_locations)

    for k, coin in enumerate(coin_picked_up):
        if coin:
            x, y = coin_locations[k]
            row = calculate_row(y)
            column = calculate_column(x)
            level_map[row][column] = 0

    # Camera position
    camera_x = 0
    player_x = checkpoints[checkpoint_idx][0]  # Start x position, change this number to spawn in a different place
    player_y = checkpoints[checkpoint_idx][1]  # Start y position, change this number to spawn in a different place
    player_speed = 8.5 * scale_factor # Adjust player speed according to their resolution
    default_speed = player_speed
    
    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.25 * scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -18 * scale_factor # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground
    doubleJumpBoots = False # Track if player has double jump boots
    doubleJumped = False # Track if player double jumped already
    speedBoots = False

    times_passed_wooden_sign = 0
    time_before_pop_up_disappears = 0

    if checkpoint_idx == 0:
        level_map[SURFACE][28] = 3 # Double Jump Boots
    elif checkpoint_idx == 1:
        doubleJumpBoots = True
        level_map[SURFACE][28] = 0 # Don't show the double jump boots
        level_map[SURFACE-5][55] = 13 # Respawn Speed Boots
    elif checkpoint_idx == 2:
        level_map[SURFACE][28] = 0 # Don't show the double jump boots
        level_map[SURFACE-5][55] = 0 # Don't show the speed Boots

    if checkpoint_idx != 2:
        level_map[SURFACE-2][79:81] = [0] * 2   # Despawn platform for the coin

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    #-----Declared variables for speed boost to avoid undefined variable error
    powerup_respawns = {}
    super_speed_effects = []
    #-----Declared variables for Dash power-up to avoid undefined variable error
    dashed = False
    dash_duration = 0

    #-----Variable to check which gadget was picked up first
    double_first = False
    dying = False
    death_count = load_save(slot).get("Tutorial Deaths")
    if not death_count:
        death_count = 0

    running = True
    while running:

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the PauseMenu
            result = pause_menu.handle_event(event, slot)
            if result == "restart":
                update_save(slot, {"Tutorial Checkpoint": 0}) # Set checkpoint to 0
                tutorial_level(slot)
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if on_ground:
                    player_vel_y = jump_power  # Normal jump
                    on_ground = False
                    doubleJumped = False  # Reset double jump when landing
                elif doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jump
                    doubleJumped = True  # Mark double jump as used
        if pause_menu.paused:
            continue

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Tutorial", True, (255, 255, 255))  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)
        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0: # Continue if the tile is an air block
                    continue
                if tile == 10: #Draw the fence at half size
                    screen.blit(tiles.get(tile), (x, y + TILE_SIZE // 2))
                else: # Draw according to the dictionary
                    screen.blit(tiles.get(tile), (x, y))
                if calculate_column(player_x) >= 60:
                    level_map[SURFACE][60] = 12 # Draw the normal npc
                else:
                    level_map[SURFACE][60] = 4 # Draw the flipped npc

        # Draw dirt below ground
        for col_index, ground_y in enumerate(ground_levels):
            for row_index in range(ground_y + 1, len(level_map) + 10):  # Extra depth
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                screen.blit(dirt_tile, (x, y))  # Draw dirt using image

        for i in trees:  # Adding trees
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 3) * TILE_SIZE  # Place tree 3 tiles above the ground
            screen.blit(tree, (x, y))

        for i in background_trees:  # Adding background trees
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 2) * TILE_SIZE  # Place background trees 2 tiles above the ground
            screen.blit(background_tree, (x, y))

        for i in rocks:  # Adding rocks
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 1) * TILE_SIZE  # Place rocks 1 tile above the ground
            screen.blit(rock, (x, y + TILE_SIZE // 2))

        for i, snowflake in enumerate(snowflakes):
            x, y, size, speed, x_speed = snowflake  # Unpack snowflake data
            
            # Move snowflake downward and drift sideways
            y += speed  
            x += x_speed  # Drift slightly left/right
            
            # Reset snowflake when it reaches the bottom or moves too far left/right
            if y > HEIGHT:
                y = 0
                x = random.randint(0, WIDTH)  # Respawn at a new x position
            if x < 0 or x > WIDTH:  # Keep it within screen bounds
                x = random.randint(0, WIDTH)

            # Update snowflake position in the list
            snowflakes[i] = [x, y, size, speed, x_speed]

            # Draw snowflake
            pygame.draw.circle(screen, WHITE, (int(x), int(y)), size)
        
        # Check if player is near the NPC
        npc_x = calculate_x_coordinate(60)  # NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_npc_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the NPC 2
        npc_x = calculate_x_coordinate(27)  # NPC 2's x position
        npc_y = (SURFACE) * TILE_SIZE  # NPC 2's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle NPC 2 dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_npc_2_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the NPC 3
        npc_x = calculate_x_coordinate(86)  # NPC 3's x position
        npc_y = (SURFACE) * TILE_SIZE  # NPC 3's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle NPC 3 dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_npc_3_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the NPC 3
        npc_x = calculate_x_coordinate(8)  # NPC 3's x position
        npc_y = (SURFACE) * TILE_SIZE  # NPC 3's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle NPC 3 dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_npc_4_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Handle events
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_d]: # If player presses D
            player_x += player_speed
            moving = True
            direction = 1
        if keys[pygame.K_a]: # If player presses A
            player_x -= player_speed        
            moving = True
            direction = -1
        # Jumping Logic (Space Pressed)
        if keys[pygame.K_SPACE]:
            if on_ground:
                player_vel_y = jump_power  # Normal jump
                on_ground = False
                doubleJumped = False  # Reset double jump when jumping once
        if moving:
            animation_timer += 1
            if animation_timer >= animation_speed:  
                animation_timer = 0
                animation_index = 1 - animation_index  # Alternate between 0 and 1

        current_frame = run_frames[animation_index]

        if direction == -1:  # Flip when moving left
            current_frame = pygame.transform.flip(current_frame, True, False)

        if moving: # Animate the player running if they are moving
            if not on_ground and direction == 1: # If they are airborne and moving right
                screen.blit(run, (player_x - camera_x, player_y))
            elif not on_ground and direction == -1: # If they are airborne and moving left
                screen.blit(flipped_run, (player_x - camera_x, player_y))
            else: # On ground
                screen.blit(current_frame, (player_x - camera_x, player_y))
        else: # Draw the player in an idle position
            if direction == 1: # Right
                screen.blit(player, (player_x - camera_x, player_y))
            else: # Left
                screen.blit(flipped_player, (player_x - camera_x, player_y))

        screen.blit(inventory, (inventory_x, inventory_y))
            
        # Apply gravity
        player_vel_y += gravity
        player_y += player_vel_y

        on_ground = False
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                if tile in {1, 2}:  # Ground or platform tiles
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE

                    # This code block prevents the player from falling through solid ground
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                    player_y + TILE_SIZE <= tile_y + player_vel_y and  # Only land if falling down
                    player_y + TILE_SIZE > tile_y):  # Ensures overlap
                        player_y = tile_y - TILE_SIZE
                        player_vel_y = 0
                        on_ground = True  # Player lands
                        doubleJumped = False # Reset double jump

                    # This code block prevents collision with solid blocks from the left and right
                    if (player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):  # If the player is at the same height as the block
                        if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and player_x + TILE_SIZE - player_speed <= tile_x):  
                            # Moving right into a block
                            player_x = tile_x - TILE_SIZE  

                        elif (player_x < tile_x + TILE_SIZE and player_x + TILE_SIZE > tile_x and player_x + player_speed >= tile_x + TILE_SIZE):  
                            # Moving left into a block
                            player_x = tile_x + TILE_SIZE

                    # This code block prevents collision with solid blocks above their head
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                        player_y < tile_y + TILE_SIZE and player_y - player_vel_y >= tile_y + TILE_SIZE):

                        player_y = tile_y + TILE_SIZE  # Align player below the ceiling
                        player_vel_y = 0  # Stop upward motion
                
                
                # This code picks up the double jump boots
                if tile == 3:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        gadget_sound.play() # Play gadget pick up sound when picking up
                        doubleJumpBoots = True
                        doubleJumped = False

                # This code picks up the speed boots
                if tile == 13:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        gadget_sound.play() # Play gadget pick up sound when picking up
                        player_speed = player_speed * 1.25 # Up the player speed
                        speedBoots = True

                # Thorns
                if tile == 6:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        death_sound.play() # Play gadget pick up sound when picking up
                        dying = True

                # Super Speed
                if tile == 8:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        super_speed_sound.play()
                        level_map[row_index][col_index] = 0
                        power_up_sound.play()

                        if len(super_speed_effects) == 0:
                            player_speed *= 2  # Double the speed
                        super_speed_effects.append({"end_time": pygame.time.get_ticks() + 2000})  # 2 sec effect
                        powerup_respawns[(row_index, col_index)] = [8, pygame.time.get_ticks() + 5000]  # 5 sec respawn

                # Right Dash
                if tile == 9:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        dash_pickup_time = pygame.time.get_ticks()
                        powerup_respawns[(row_index, col_index)] = [9, pygame.time.get_ticks() + 5000]
                        dash_duration = dash_pickup_time + 750
                        dash_sound.play()
                        dashed = True
                        level_map[row_index][col_index] = 0 
                        dash_sound.play()
                        player_speed = player_speed * 2 
                        direction = 1
                        if player_speed < 0:
                            player_speed *= -1

                # Coin
                if tile == 14:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        
                        coin_position = (tile_x, tile_y)
                        idx = coin_locations.index(coin_position)
                        coin_picked_up[idx] = True
                        update_save(slot, {"Tutorial Coins": coin_picked_up}) # Save picked up coins
                        eclipse_increment(slot, 1)
                        level_map[row_index][col_index] = 0
                        coin_sound.play() # Play coin pick up sound when contact
                        level_map[SURFACE-2][79:81] = [2] * 2   # Platform 

        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            show_level_completed_screen(slot, death_count)
            running = False
        
        if player_x <= 0: # Ensure player is within the bounds of the level and does not go to the left
            player_x = 0

        # When player falls past bottom of level = dies
        if player_y + TILE_SIZE >= level_height * TILE_SIZE:
            death_sound.play() # Play death sound when player touches water or thorn
            dying = True
            
        if dying:
            player_x, player_y = checkpoints[checkpoint_idx][0], checkpoints[checkpoint_idx][1]
            death_count += 1
            update_save(slot, {"Tutorial Deaths": death_count})
            respawn_powerups()
            dash_duration = 0
            dying = False
            player_speed = default_speed # Reset to normal speed
            if checkpoint_idx == 0 and doubleJumpBoots:
                doubleJumpBoots = False
                level_map[SURFACE][28] = 3
            elif checkpoint_idx == 1 and speedBoots:
                level_map[SURFACE-5][55] = 13
                speedBoots = False
            if super_speed_effects:
                super_speed_effects.clear()   # Remove all ongoing effects

        current_time = pygame.time.get_ticks()

        # Apply speed effects from multiple power-ups
        for effect in super_speed_effects[:]:  # Iterate over a copy of the list
            if current_time >= effect["end_time"]:  # Check if effect expired
                super_speed_effects.remove(effect)
            if len(super_speed_effects) == 0:
                player_speed /= 2

        # Modified powerup respawns to singular function
        powerup_remove = []
        for position, gadget in powerup_respawns.items():
            if current_time >= gadget[1]:
                level_map[position[0]][position[1]] = gadget[0]
                powerup_remove.append(position) # mark for removal

        # Apply dash powerup
        if dashed:
            if (current_time >= dash_duration) and (dash_duration != 0):
                player_speed = default_speed
                dashed = False
                dash_duration = 0

        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                update_save(slot, {"Tutorial Checkpoint": checkpoint_idx})
                if checkpoint_idx == 2:
                    doubleJumpBoots = False # Remove their double jump boots
                    if speedBoots:
                        speedBoots = False
                        player_speed = player_speed / 1.25 # Revert their speed back to normal
                    if not coin_picked_up[0]: # If coin was not picked up before
                        level_map[SURFACE-1][68] = 14  #Spawn coin after reaching 2nd checkpoint

        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

        # print(player_x)
        #-----Inventory Fill-up logic

        screen.blit(inventory, (inventory_x, inventory_y))

        if (doubleJumpBoots):
            if (doubleJumpBoots) and (speedBoots == False):
                double_first = True
                screen.blit(inventory_jump_boots, first_slot)
            elif (doubleJumpBoots) and (speedBoots) and double_first:
                screen.blit(inventory_jump_boots, first_slot)
                screen.blit(inventory_speed_boots, second_slot)


        if (speedBoots):
            if  (speedBoots) and (doubleJumpBoots == False):
                double_first == False
                screen.blit(inventory_speed_boots, first_slot)
                print(f"SpeedBoots: {speedBoots}")
            elif (doubleJumpBoots) and (speedBoots) and (double_first == False):
                screen.blit(inventory_speed_boots, first_slot)
                screen.blit(inventory_jump_boots, second_slot)


        # Pop up near level completion 
        # print(calculate_column(player_x))
        if (pygame.time.get_ticks() < time_before_pop_up_disappears):
            screen.blit(level_almost_complete_popup, (pop_up_x, pop_up_y))
            screen.blit(level_almost_complete_text, level_almost_complete_rect)
            screen.blit(keep_heading_right_text, keep_heading_right_rect)


        if (calculate_column(player_x) >= 130 and times_passed_wooden_sign < 1):
            times_passed_wooden_sign += 1
            screen.blit(level_almost_complete_popup, (pop_up_x, pop_up_y))
            screen.blit(level_almost_complete_text, level_almost_complete_rect)
            screen.blit(keep_heading_right_text, keep_heading_right_rect)
            time_before_pop_up_disappears = pygame.time.get_ticks() + 5000



        pygame.display.flip()  # Update display

if __name__ == "__main__":
    tutorial_level(1)
    pygame.quit()