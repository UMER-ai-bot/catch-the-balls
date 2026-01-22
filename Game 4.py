import pygame
import random
import sys

from pygame.cursors import sizer_y_strings
from pygame.examples.midi import fill_region

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1300,675    #default window size
fullscreen = True            #track fullscreen state

# Create window (start in windowed mode)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Blocks")

# Colors
WHITE = (255,255,255)
BLACK = (255,0,0)
RED   = (0,0,0)
BLUE  = (0,0,255)
SKYBLUE = (0,0,255)

# Player setup
player_width, player_height = 200, 50
player_x = WIDTH // 15 - player_width // 15
player_y = HEIGHT - 50 - player_height // 25
player_speed = 50

# Block setup
block_width, block_height = 25, 25
block_speed = 10
blocks = []
for _ in range(5):  # number of blocks
    x = random.randint(0, WIDTH - block_width)
    y = random.randint(-HEIGHT, 0)
    blocks.append(pygame.Rect(x, y, block_width, block_height))

# Score & Lives
score = 0
lives = 10
font = pygame.font.SysFont("Arial", 25, bold=True)

clock = pygame.time.Clock()

# Game loop
game_over = False
while True:
    bg_image = pygame.image.load("background.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, (1500,1500))
    screen.blit(bg_image, (1, 1))


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Toggle fullscreen with F key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen =  fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((1, 1), pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                else:
                    screen = pygame.display.set_mode((1000, 1000))
                    WIDTH, HEIGHT = 6000, 6000

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Block movement and collision
        for block in blocks:
            block.y += block_speed
            if block.y > HEIGHT:
                lives -= 1   # missed a block
                block.y = -block_height
                block.x = random.randint(0, WIDTH - block_width)
                if lives <= 0:
                    game_over = True

            if player_rect.colliderect(block):
                score += 1
                block.y = -block_height
                block.x = random.randint(0, WIDTH - block_width)

            # Draw block
            pygame.draw.rect(screen, RED, block)

        # Draw player
        pygame.draw.rect(screen,WHITE, player_rect)

        # Draw score & lives
        score_text = font.render(f"Score: {score}", True, SKYBLUE)
        lives_text = font.render(f"Lives: {lives}", True, SKYBLUE)
        screen.blit(score_text, (11, 11))
        screen.blit(lives_text, (WIDTH - 150, 10))

    else:
        # Game Over screen
        over_text = font.render("GAME OVER", True, BLUE)
        final_score = font.render(f"Final Score: {score}", True,RED)
        screen.blit(over_text, (WIDTH//2 - 100, HEIGHT//2 - 100))
        screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2 + 1))

    # Update display
    pygame.display.flip()
    clock.tick(60)

    # Game over overlay
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (450, 450))