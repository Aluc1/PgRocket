from random import randint
from math import sin, cos, tan
import pygame

class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        return
    def as_int_tuple(self) -> tuple:
        return (int(self.x), int(self.y))
    def ait_with_offset(self, offset: tuple) -> tuple:
        return (int(self.x + randint(offset[0], offset[1])), int(self.y + randint(offset[0], offset[1])))
class Entity:
    def __init__(self, position: Vector2, size: Vector2, speed: float) -> None:
        self.position = position
        self.size = size
        self.speed = speed
        return

def collides_entity(entity1: Entity, entity2: Entity) -> bool:
    # Detect collision with top left corner #
    if (entity1.position.x >= entity2.position.x) and (entity1.position.x <= entity2.position.x + entity2.size.x) and (entity1.position.y >= entity2.position.y) and (entity1.position.y <= entity2.position.y + entity2.size.y):
        return True
    # Detect collision with top right corner #
    elif (entity1.position.x + entity1.size.x >= entity2.position.x) and (entity1.position.x + entity1.size.x <= entity2.position.x + entity2.size.x) and (entity1.position.y >= entity2.position.y) and (entity1.position.y <= entity2.position.y + entity2.size.y):
        return True
    # Detect collision with bottom left corner #
    elif (entity1.position.x >= entity2.position.x) and (entity1.position.x <= entity2.position.x + entity2.size.x) and (entity1.position.y + entity1.size.y >= entity2.position.y) and (entity1.position.y + entity1.size.y <= entity2.position.y + entity2.size.y):
        return True
    # Detect collision with bottom right corner #
    elif (entity1.position.x + entity1.size.x >= entity2.position.x) and (entity1.position.x + entity1.size.x <= entity2.position.x + entity2.size.x) and (entity1.position.y + entity1.size.y >= entity2.position.y) and (entity1.position.y + entity1.size.y <= entity2.position.y + entity2.size.y):
        return True
    # No collision detected #
    else:
        return False

def main() -> None:
    # Initialize pygame modules #
    pygame.display.init()
    pygame.font.init()
    # Constants #
    WIDTH, HEIGHT = 640, 480
    PLAYER_ACCEL = 100
    OFFSET_MIN, OFFSET_MAX = -2, 3
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    SPRITE_ROCKET = pygame.transform.scale(pygame.image.load("resources/rocket.png"), (32, 64))
    SPRITE_ASTEROID = pygame.transform.scale(pygame.image.load("resources/asteroid.png"), (128, 256))
    SPRITE_PLANET = pygame.transform.scale(pygame.image.load("resources/planet.png"), (32, 32))
    FONT_30 = pygame.font.Font("resources/f.ttf", 30)
    FONT_60 = pygame.font.Font("resources/f.ttf", 60)
    PRE_TITLE = FONT_60.render("PgRocket", False, WHITE)
    PRE_PLAY = FONT_30.render("Play", False, WHITE)
    PRE_PLAY_HOVER = FONT_30.render("Play", False, RED)
    PRE_HIT = FONT_30.render("You were hit by an asteroid!", False, RED)
    # Window #
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PgRocket")
    # Variables #
    player = None
    player_points = None
    asteroid = None
    planet = None
    clock = pygame.time.Clock()
    on_menu = True
    running = True
    started = True
    # Main loop #
    while running:
        # Events #
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    on_menu = True
                    started = True
        # Timing #
        FRAME_DELTA = clock.tick_busy_loop() / 1000
        # Input #
        KEYS = pygame.key.get_pressed()
        MOUSE_POS = pygame.mouse.get_pos()
        MOUSE_PRESS = pygame.mouse.get_pressed()
        # Menu #
        if on_menu:
            window.fill(BLACK)
            window.blit(PRE_TITLE, (10, 10))
            if (MOUSE_POS[1] >= 200) and (MOUSE_POS[1] <= 230):
                if MOUSE_PRESS[0]:
                    # Reset entity variables and start game #
                    player = Entity(Vector2(640 /  2 - 16, 360), Vector2(32, 64), 0)
                    asteroid = Entity(Vector2(randint(0, 640-128), -512), Vector2(128, 200), 500) # 200 y size to give the player a chance to escape before asteroid really hits them
                    planet = Entity(Vector2(randint(0, 640-32), -64), Vector2(32, 32), 125)
                    player_points = 0
                    on_menu = False
                    started = False
                else:
                    window.blit(PRE_PLAY_HOVER, (50, 200))
            else:
                window.blit(PRE_PLAY, (50, 200))
            if not started:
                window.blit(PRE_HIT, (50, 400))
                window.blit(FONT_30.render("Final score: " + str(player_points), False, WHITE), (50, 430))
            pygame.display.flip()
        # Game #
        else:
            # Handle input and player movement #
            if KEYS[pygame.K_LEFT]:
                player.speed -= PLAYER_ACCEL * FRAME_DELTA
            if KEYS[pygame.K_RIGHT]:
                player.speed += PLAYER_ACCEL * FRAME_DELTA
            player.position.x += player.speed * FRAME_DELTA * 15
            # Wrap around effect #
            if player.position.x < -64:
                player.position.x = 640
            elif player.position.x > 640:
                player.position.x = -64
            # Player rotation ( Graphics only ) #
            rotation = -player.speed
            if rotation < -90:
                rotation = -90
            elif rotation > 90:
                rotation = 90
            # Change Y coordinate based on rotation #
            player.position.y = 360 + abs(rotation / 2)
            # Change hitbox size based on rotation #
            player.size.x = 32 + abs(rotation / 2)
            player.size.y = 64 - abs(rotation / 4)
            # Manage asteroid #
            asteroid.position.y += asteroid.speed * FRAME_DELTA
            if collides_entity(player, asteroid):
                on_menu = True
            if asteroid.position.y > 480:
                asteroid.position.y = -256
                asteroid.position.x = randint(0, 640-128)
            # Manage planet #
            planet.position.y += planet.speed * FRAME_DELTA
            if collides_entity(player, planet):
                planet.position.y = 481
                player_points += 1
            elif planet.position.y > 480:
                planet.position.y = -32
                planet.position.x = randint(0, 640-32)
            # Draw graphics #
            window.fill(BLACK)
            # pygame.draw.rect(window, RED, (player.position.as_int_tuple(), player.size.as_int_tuple()), 1) # Draw hitbox
            POINTS = FONT_30.render(str(player_points), False, WHITE)
            POINTS_POS = (int(player.position.x), 450)
            window.blit(SPRITE_PLANET, planet.position.as_int_tuple())
            window.blit(pygame.transform.rotate(SPRITE_ROCKET, rotation), player.position.ait_with_offset((OFFSET_MIN, OFFSET_MAX)))
            window.blit(SPRITE_ASTEROID, asteroid.position.ait_with_offset((OFFSET_MIN, OFFSET_MAX)))
            window.blit(POINTS, POINTS_POS)
            pygame.display.flip()
    pygame.quit()
    return

if __name__ == "__main__":
    main()