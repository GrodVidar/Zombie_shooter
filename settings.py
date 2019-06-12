import pygame
vec = pygame.math.Vector2

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 255)
BROWN = (139, 69, 19)

# Display settings
BACKGROUND_COLOR = DARK_GREEN
TITLE = "Platform Game"
WIDTH = 1920
HEIGHT = 1080
FPS = 60

# Movement settings
PLAYER_SPEED = 400
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)
MOB_SPEEDS = [100, 150, 200, 200, 300]
MOB_HIT_RECT = pygame.Rect(0, 0, 30, 30)
BULLET_SPEED = 750

# Bullet settings
BULLET_LIFETIME = 1000
BULLET_RATE = 100
GUN_SPREAD = 10
BARREL_OFFSET = vec(30, 10)
KICKBACK = 100
BULLET_DMG = 10
FLASH_TIME = 30

# Player settings
PLAYER_HEALTH = 100

# Mob settings
MOB_HEALTH = 100
MOB_DMG = 20
ZOM_KICKBACK = 25
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Game dimensions
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Fonts
FONT_FILE = 'ilits.ttf'

# images
PLAYER_IMG = 'survivor1_gun.png'
WALL_IMG = 'tile_129.png'
MOB_IMG = 'zoimbie1_hold.png'
FLOOR_IMG = 'tile_04.png'
BULLET_IMG = 'tile_187.png'
TILEMAP = 'gameMap.tmx'
MUZZLE_FLASHES = ['flash04.png', 'flash05.png', 'flash06.png', 'flash07.png', 'flash08.png']
SPLAT = 'blood-splatter-png-44461.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# items
ITEM_IMAGES = {'health': 'health_pack.png'}
HEALTH_PACK_HEAL = 40
BOB_RANGE = 5
BOB_SPEED = 0.1

# Sounds
BG_MUSIC = 'MrMalice - Itchy.mp3'
WEAPON_SOUNDS = ['Retro_8-Bit_Game-Gun_Pistol_Weapon_Shoot_Fire_03.wav']
PLAYER_HIT_SOUNDS = ['8.wav', '9.wav', '10.wav', '11.wav', '12.wav', '13.wav', '14.wav']
MOB_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav','zombie-roar-1.wav', 'zombie-roar-2.wav', 'zombie-roar-3.wav',
                   'zombie-roar-4.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav', 'zombie-roar-8.wav']
MOB_HIT_SOUND = ['splat-15.wav']
EFFECTS_SOUNDS = {'level_start': 'Retro_8-Bit_Game-Alarm_Bell_07.wav',
                  'health_up': 'Retro_8-Bit_Game-Jump_Lift_TakeOff_05.wav'}
