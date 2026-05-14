import sys
import random
import pygame
pygame.init()

# --- Screen setup ---
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bouncing Ball Game")

# --- Colors ---
black = (0, 0, 0)
white = (255, 255, 255)

# --- Background setup ---
# Make sure "background.jpg" is in the same folder as this Python file
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (width, height))

# --- Music setup ---
# Make sure "background_music.mp3" is in the same folder as this Python file
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(1.5)   # 0.0 = mute, 1.0 = max volume
pygame.mixer.music.play(-1)          # -1 = loop forever

# --- Ball setup ---
ball = pygame.image.load("intro_ball.gif")
ball = pygame.transform.scale(ball, (90, 90))  # Increased ball size
ballrect = ball.get_rect()

# Function to reset the ball position & direction
def reset_ball():
    ballrect.centerx = random.randint(100, width - 100)  # Random X position
    ballrect.top = 50  # Start from near the top
    dx = random.choice([-8.0, 8.0])  # Random horizontal direction
    dy = 8.0  # Always start moving downward
    return [dx, dy]

speed = reset_ball()

# --- Paddle setup ---
paddle_width, paddle_height = 120, 15
paddle = pygame.Rect(width // 2 - paddle_width // 2, height - 40, paddle_width, paddle_height)
paddle_speed = 8

# --- Score setup ---
score = 0
font = pygame.font.Font(None, 36)

# --- Game state ---
game_over = False

clock = pygame.time.Clock()

# --- Main Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Paddle movement
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        if keys[pygame.K_RIGHT] and paddle.right < width:
            paddle.move_ip(paddle_speed, 0)

        # Ball movement
        ballrect = ballrect.move(speed)

        # Bounce from left and right walls
        if ballrect.left <= 0 or ballrect.right >= width:
            speed[0] = -speed[0]

        # Bounce from top wall
        if ballrect.top <= 0:
            speed[1] = -speed[1]

        # Paddle collision
        if ballrect.colliderect(paddle):
            speed[1] = -abs(speed[1])  # Always bounce upward
            score += 1

            # Increase ball speed every 10 points
            if score % 10 == 0:
                speed[0] *= 1.1
                speed[1] *= 1.1

        # Check if ball missed paddle (goes below screen)
        if ballrect.bottom >= height:
            game_over = True
            pygame.mixer.music.stop()  # Stop music when game is over

    # --- Drawing section ---
    screen.blit(background, (0, 0))  # Draw background image

    if not game_over:
        # Draw ball & paddle
        screen.blit(ball, ballrect)
        pygame.draw.rect(screen, white, paddle)

        # Draw score
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))
    else:
        # Game Over screen
        over_text = font.render("GAME OVER - Press R to Restart", True, white)
        screen.blit(over_text, (width // 2 - 200, height // 2))
        score_text = font.render(f"Final Score: {score}", True, white)
        screen.blit(score_text, (width // 2 - 100, height // 2 + 40))

        # Restart option
        if keys[pygame.K_r]:
            # Reset game state
            speed = reset_ball()
            paddle.centerx = width // 2
            score = 0
            game_over = False
            pygame.mixer.music.play(-1)  # Restart background music

    pygame.display.flip()
    clock.tick(60)
