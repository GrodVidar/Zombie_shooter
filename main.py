import pygame
import random
from os import path
import sys
from settings import *
from sprites import *
from tilemap import *

def draw_player_hp(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 400
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf,col, fill_rect)
    pygame.draw.rect(surf,BLACK, outline_rect, 2)


class Game(object):
    def __init__(self):
        # initialize game
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(100,100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align='nw'):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        fonts_folder = path.join(game_folder, 'fonts')
        sounds_folder = path.join(game_folder, 'sounds')
        self.title_font = path.join(fonts_folder, FONT_FILE)
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map = TiledMap(path.join(map_folder, TILEMAP))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pygame.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pygame.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pygame.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.bullet_img = pygame.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.splat = pygame.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pygame.transform.scale(self.splat,(int(TILESIZE*1.5),int(TILESIZE*1.5)))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pygame.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Load Sounds
        pygame.mixer.music.load(path.join(sounds_folder, BG_MUSIC))
        self.soundfx = {}
        for type in EFFECTS_SOUNDS:
            self.soundfx[type] = pygame.mixer.Sound(path.join(sounds_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for sound in WEAPON_SOUNDS:
            s = pygame.mixer.Sound(path.join(sounds_folder, sound))
            s.set_volume(.1)
            self.weapon_sounds['gun'].append(s)
        self.mob_moan_sounds = []
        for sound in MOB_MOAN_SOUNDS:
            s = pygame.mixer.Sound(path.join(sounds_folder, sound))
            s.set_volume(.1)
            self.mob_moan_sounds.append(s)
        self.player_hit_sounds = []
        for sound in PLAYER_HIT_SOUNDS:
            s = pygame.mixer.Sound(path.join(sounds_folder, sound))
            s.set_volume(.3)
            self.player_hit_sounds.append(s)
        self.mob_hit_sounds = []
        for sound in MOB_HIT_SOUND:
            s = pygame.mixer.Sound(path.join(sounds_folder, sound))
            s.set_volume(.1)
            self.mob_hit_sounds.append(s)

    def new(self):
        # reset the game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera= Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.soundfx['level_start'].set_volume(.05)
        self.soundfx['level_start'].play()


    def run(self):
        # game-loop
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(.10)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # keep updating game
        self.all_sprites.update()
        self.camera.update(self.player)
        # check collision - Player - Item
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                self.soundfx['health_up'].set_volume(.10)
                self.soundfx['health_up'].play()
                hit.kill()
                self.player.add_health(HEALTH_PACK_HEAL)
        # check collision - Player - Mob
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DMG
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(ZOM_KICKBACK, 0).rotate(-hits[0].rot)
            if random() < 1:
                choice(self.player_hit_sounds).play()
        # check collision - Mob - bullet
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DMG
            hit.vel = vec(0, 0)

    def events(self):
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen,((0,255,0)), (x, 0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen,((0,255,0)), (0, y), (WIDTH,y))

    def draw(self):
        # draw game
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, TEAL, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, TEAL,self.camera.apply_rect(wall.rect), 1)
        # pygame.draw.rect(self.screen, (255,255,255), self.player.hit_rect, 2)
        draw_player_hp(self.screen, WIDTH/2-200, HEIGHT-100, self.player.health / PLAYER_HEALTH)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("PAUSED", self.title_font, 300, RED, WIDTH/2, HEIGHT/2, align="center")
        pygame.display.flip()

    def show_start_screen(self):
        # show the start screen
        pass

    def show_game_over_screen(self):
        # screen shows up when loss or win
        pass


game = Game()

game.show_start_screen()

while True:
    game.new()
    game.run()
    game.show_game_over_screen()

pygame.quit()
