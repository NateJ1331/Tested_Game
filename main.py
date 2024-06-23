import pygame as pg
import sys

pg.init()
pg.display.set_caption("Tested")

BG_COLOR = (0, 0, 0)
WIDTH, HEIGHT = 1000, 800
FPS = 60

PLAYER_VEL = 5

window = pg.display.set_mode((WIDTH, HEIGHT))

#creates blocks when called
def get_block(size):
    try:
        image = pg.image.load("Images/Block.png").convert_alpha()
        surface = pg.Surface((size, size), pg.SRCALPHA, 32)
        rect = pg.Rect(0, 0, size, size)
        surface.blit(image, (0, 0), rect)
        return pg.transform.scale2x(surface)
    except pg.error as e:
        print(f"Error loading block image: {e}")
        return None

#everything for player
class Player(pg.sprite.Sprite):
    COLOR = (255, 153, 255)
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_vel = 0
        self.y_vel = 0
        self.mask = pg.mask.from_surface(self.image)
        self.fall_count = 0
        self.jump_count = 0

    #jumps when called
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
    
    #handles up or down movement
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel

    def move_right(self, vel):
        self.x_vel = vel

    #handles constant gravity
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1

    #what happens when you land
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0  # Reset jump count when landed
    
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1

    #draws player
    def draw(self, win):
        pg.draw.rect(win, self.COLOR, self.rect)

class Object(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        if block is not None:
            self.image.blit(block, (0, 0))
            self.mask = pg.mask.from_surface(self.image)
        else:
            print("Block image is None")
            self.mask = None

#handles the backround tiles (adds possiblility to change backround later)
def get_background(name):
    try:
        image = pg.image.load("Images/Tile.png")
        _, _, width, height = image.get_rect()
        tiles = []
        for i in range(WIDTH // width + 1):
            for j in range(HEIGHT // height + 1):
                pos = [i * width, j * height]
                tiles.append(pos)
        return tiles, image
    except pg.error as e:
        print(f"Error loading background image: {e}")
        return [], None

def draw(window, background, bg_image, player, objects):
    if bg_image is not None:
        for tile in background:
            window.blit(bg_image, tile)
    else:
        window.fill(BG_COLOR)

    for obj in objects:
        obj.draw(window)

    player.draw(window)

    pg.display.update()

#vertical collision 
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj) 

    return collided_objects
#vsll other collision
def collide(player,objects,dx): 
    player.move(dx,0)
    player.update()
    collided_object = None
    for obj in objects:
        if pg.sprite.collide_mask(player,obj):
            collided_object = obj
            break

    player.move(-dx,0)
    player.update()

    return collided_object

# movement
def handle_move(player, objects):
    keys = pg.key.get_pressed()
    
    player.x_vel = 0
    collide_left = collide(player,objects,-PLAYER_VEL)
    collide_right = collide(player,objects,PLAYER_VEL)

    if keys[pg.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pg.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)
    
    handle_vertical_collision(player, objects, player.y_vel)

def main(window):
    clock = pg.time.Clock()
    background, bg_image = get_background("Tile.png")

    block_size = 64  #sets the block size

    player = Player(100, 675, 50, 50)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    
    #sets all platforms
    objects = [*floor,
               Block(0,HEIGHT - block_size * 2 , block_size), 
               Block(block_size * 3,HEIGHT - block_size * 4 , block_size),
               Block(block_size * 4,HEIGHT - block_size * 5 , block_size),
               Block(block_size * 4,HEIGHT - block_size * 4 , block_size),
               Block(block_size * 8,HEIGHT - block_size * 7 , block_size),
               Block(block_size * 4,HEIGHT - block_size * 8 , block_size)
               ]

    #main game loop
    run = True
    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            
            #jumping
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player.jump_count < 1:
                    player.jump()

        player.loop(FPS)
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects)

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main(window)
