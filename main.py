import asyncio
import pygame


# Game settings
screenWidth = 1280
screenHeight = 720
playerSize = 100
playerSpeed = 5
gravity = 1
jumpSpeed = -18


pygame.init()
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "My First PyGame Program"
screen = window.get_surface()

# The player's position
playerX = 0
playerY = screenHeight - playerSize
playerVelocityY = 0
playerIsJumping = False

# The blue obstacle
blueBox = pygame.Rect(500, 300, 100, 100)

running = True
while running:
    # Check for events, such as closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move left and right
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerX -= playerSpeed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerX += playerSpeed

    # Start a jump only when the player is on the ground
    playerIsOnGround = playerY == screenHeight - playerSize
    if keys[pygame.K_SPACE] and playerIsOnGround:
        playerVelocityY = jumpSpeed
        playerIsJumping = True

    # Apply gravity while the player is in the air
    if playerIsJumping:
        playerY += playerVelocityY
        playerVelocityY += gravity

    # Keep the player inside the screen
    playerX = max(0, min(playerX, screenWidth - playerSize))
    playerY = max(0, min(playerY, screenHeight - playerSize))

    # Stop falling when the player reaches the ground
    if playerY == screenHeight - playerSize:
        playerIsJumping = False
        playerVelocityY = 0

    player = pygame.Rect(playerX, playerY, playerSize, playerSize)

    # Reset the player if they touch the blue box
    if player.colliderect(blueBox):
        playerX = 0
        playerY = 0
        player = pygame.Rect(playerX, playerY, playerSize, playerSize)

    # Draw the game
    screen.fill((0, 255, 0))
    pygame.draw.rect(screen, (0, 0, 255), blueBox)
    pygame.draw.rect(screen, (255, 0, 0), player)
    window.flip()

    # Give the browser time to update the screen
    await asyncio.sleep(1 / 60)

pygame.quit()
