import asyncio
import random
import pygame
import time
import js

def randomObstacle(safeRect=None):
    while True:
        obstacleX = random.randint(0, screenWidth - obstacleSize)
        obstacleY = random.randint(0, screenHeight - obstacleSize)

        if random.randint(0, 1) == 0:
            obstacle = pygame.Rect(obstacleX, 0, obstacleSize, screenHeight)
        else:
            obstacle = pygame.Rect(0, obstacleY, screenWidth, obstacleSize)

        if safeRect is None or not obstacle.colliderect(safeRect):
            return obstacle


# Game settings
screenWidth = 1280
screenHeight = 720
playerSize = 100
playerSpeed = 10
obstacleSize = 25
obstacleInterval = 0.75
maxObstacles = 2
teleportDistance = 300
teleportCooldown = 500
lastTeleportTime = -teleportCooldown
githubUrl = "https://github.com/George-LJH/PygameIntroductionWithPyScript"
pygame.init()


window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "My First PyGame Program"
screen = window.get_surface()
playerImage = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
red = random.randint(0, 255)
green = random.randint(0, 255)
blue = random.randint(0, 255)
playerImage.fill((255, 0, 0))
teleportPreview = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
teleportPreview.fill((255, 0, 0, 100))
gameOverOnce = False
highscore = 0
redScale = 1
greenScale = 1
blueScale = 1
cachedUiScale = None
font = None
instructionFont = None

def drawCenteredLines(textSurfaces, centerX, centerY, spacing):
    totalHeight = sum(text.get_height() for text in textSurfaces)
    totalHeight += spacing * (len(textSurfaces) - 1)
    currentY = centerY - totalHeight / 2

    for text in textSurfaces:
        textPosition = text.get_rect(center=(centerX, currentY + text.get_height() / 2))
        screen.blit(text, textPosition)
        currentY += text.get_height() + spacing


def resetGame():
    global score, obstacleInterval, playerX, playerY, obstacles
    global nextObstacles, player, lastObstacleTime, gameStarted
    global obstacleSize, lastTeleportTime, highscore, maxObstacles, trail
    global trailFrameCounter
    obstacleSize = 25
    score = 0
    obstacleInterval = 0.75
    playerX = (screenWidth/2)-(playerSize)/2
    playerY = (screenHeight/2)-(playerSize)/2
    player = pygame.Rect(playerX, playerY, playerSize, playerSize)
    obstacles = [randomObstacle(player), randomObstacle(player)]
    nextObstacles = [randomObstacle(player), randomObstacle(player)]
    lastObstacleTime = time.time()
    lastTeleportTime = pygame.time.get_ticks() - teleportCooldown
    gameStarted = False
    saved_highscore = js.localStorage.getItem("highScore")
    highscore = int(saved_highscore or 0)
    if saved_highscore is None:
        js.localStorage.setItem("highScore", "0")
    maxObstacles = 2
    trail = []
    trailFrameCounter = 0


def startGame():
    global gameStarted
    resetGame()
    gameStarted = True


running = True
resetGame()

while running:
    displayWidth, displayHeight = screen.get_size()
    uiScale = min(displayWidth / screenWidth, displayHeight / screenHeight)
    teleportedThisFrame = False
    startButton = pygame.Rect(
        displayWidth // 2 - 140,
        displayHeight - 90,
        280,
        70,
    )


    red += redScale
    green += greenScale
    blue += blueScale
    if red >= 255:
        redScale = -1
    elif red <= 0:
        redScale = 1
    if green >= 255:
        greenScale = -1
    elif green <= 0:
        greenScale = 1
    if blue >= 255:
        blueScale = -1
    elif blue <= 0:
        blueScale = 1
    playerImage.fill((red, green, blue))
    if uiScale != cachedUiScale:
        font = pygame.font.SysFont(None, max(20, round(40 * uiScale)))
        instructionFont = pygame.font.SysFont(None, max(16, round(28 * uiScale)))
        cachedUiScale = uiScale
    textSpacing = max(8, round(12 * uiScale))

    # Check for events, such as closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not gameStarted:
                startGame()
            if event.key == pygame.K_SPACE and gameStarted:
                currentTeleportTime = pygame.time.get_ticks()
                if currentTeleportTime - lastTeleportTime >= teleportCooldown:
                    keys = pygame.key.get_pressed()
                    teleported = False
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        playerY -= teleportDistance
                        teleported = True
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        playerY += teleportDistance
                        teleported = True
                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        playerX += teleportDistance
                        teleported = True
                    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        playerX -= teleportDistance
                        teleported = True

                    if teleported:
                        lastTeleportTime = currentTeleportTime
                        teleportedThisFrame = True
                        playerX = max(0, min(playerX, screenWidth - playerSize))
                        playerY = max(0, min(playerY, screenHeight - playerSize))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if startButton.collidepoint(event.pos) and not gameStarted:
                js.window.open(githubUrl, "_blank")

    if gameStarted:
        # Draw the game
        screen.fill((0, 255, 0))
        keys = pygame.key.get_pressed()
        if not teleportedThisFrame:
            # Move left and right
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                playerX -= playerSpeed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                playerX += playerSpeed

            # Move up and down
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                playerY -= playerSpeed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                playerY += playerSpeed

        # Keep the player inside the screen
        playerX = max(0, min(playerX, screenWidth - playerSize))
        playerY = max(0, min(playerY, screenHeight - playerSize))

        player = pygame.Rect(playerX, playerY, playerSize, playerSize)
        trailFrameCounter += 1
        if trailFrameCounter >= 3:
            trail.append((player.copy(), 150))
            trailFrameCounter = 0
            trail = trail[-12:]

        # Reduce the opacity of old trail positions
        updatedTrail = []
        for trailRect, opacity in trail:
            opacity -= 8
            if opacity > 0:
                updatedTrail.append((trailRect, opacity))

        trail = updatedTrail
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                # playerX = 0
                # playerY = screenHeight - playerSize
                # player = pygame.Rect(playerX, playerY, playerSize, playerSize)
                gameOverOnce = True
                gameStarted = False
                obstacleInterval = 0.75
                break

        currentTimeObstacleGeneration = time.time()
        if currentTimeObstacleGeneration - lastObstacleTime >= obstacleInterval:
            
            obstacleSize = min(obstacleSize + 1, 50)
            if score % 5 == 0 and score != 0:
                maxObstacles += min(7, int(score / 5))
            obstacles = nextObstacles
            nextObstacles = []
            for _ in range(maxObstacles):
                nextObstacles.append(randomObstacle())
            score += 1
            if score > highscore:
                highscore = score
                js.localStorage.setItem("highScore", str(highscore))
            lastObstacleTime = currentTimeObstacleGeneration
            obstacleInterval = max(0.01, obstacleInterval - 0.01)


        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 0, 255), obstacle)
        screen.blit(teleportPreview, (max(0, playerX - teleportDistance), playerY))
        screen.blit(teleportPreview, (min(screenWidth - teleportPreview.get_width(), playerX + teleportDistance), playerY))
        screen.blit(teleportPreview, (playerX, max(0, playerY - teleportDistance)))
        screen.blit(teleportPreview, (playerX, min(screenHeight - teleportPreview.get_height(), playerY + teleportDistance)))
        for trailRect, opacity in trail:
            trailColor = (
                red * opacity // 150,
                green * opacity // 150,
                blue * opacity // 150,
            )
            pygame.draw.rect(screen, trailColor, trailRect)
        screen.blit(playerImage, player)
        for nextObstacle in nextObstacles:
            pygame.draw.rect(screen, (255, 255, 0), nextObstacle, 5)
        scoreText = font.render(f"Wave: {score}", True, (255, 255, 255))
        teleportCooldownRemaining = max(
            0, (teleportCooldown - (pygame.time.get_ticks() - lastTeleportTime)) / 1000
        )
        if teleportCooldownRemaining > 0:
            teleportCooldownText = font.render(
                f"Teleport cooldown: {teleportCooldownRemaining:.3f}s",
                True,
                (255, 255, 255),
        )

        else:
            teleportCooldownText = font.render(
                f"Teleport ready!",
                True,
                (255, 255, 255),
        )
        obstacleIntervalText = font.render(
            f"Game Speed: {obstacleInterval:.2f}s",
            True,
            (255, 255, 255),
        )
        hudTexts = [scoreText, teleportCooldownText, obstacleIntervalText]
        tallestHudText = 0
        for text in hudTexts:
            if text.get_height() > tallestHudText:
                tallestHudText = text.get_height()
        hudY = tallestHudText / 2 + textSpacing
        for text in hudTexts:
            textPosition = text.get_rect(topleft=(textSpacing, hudY))
            screen.blit(text, textPosition)
            hudY += text.get_height() + textSpacing
    else:
        # Game Over or Start Screen
        screen.fill((0, 0, 0))
        startButtonColor = (0, 180, 255) if startButton.collidepoint(
            pygame.mouse.get_pos()
        ) else (0, 120, 255)
        pygame.draw.rect(screen, startButtonColor, startButton)
        buttonLabel = "View GitHub Repo"
        startButtonText = font.render(buttonLabel, True, (255, 255, 255))
        startButtonTextPosition = startButtonText.get_rect(center=startButton.center)
        screen.blit(startButtonText, startButtonTextPosition)
        if not gameOverOnce:
            menuTexts = [
                font.render("Press ENTER to start", True, (255, 255, 255)),
            ]
        else:
            menuTexts = [
                font.render("Game Over!", True, (255, 255, 255)),
                font.render("Press ENTER to restart", True, (255, 255, 255)),
                font.render(f"Wave: {score}", True, (255, 255, 255)),
            ]

        menuTexts.append(font.render(f"Highscore: {highscore}", True, (255, 255, 255)))
        instructions = [
            "Move: Arrow Keys or W A S D",
            "Teleport: Hold SPACE and press a Direction Key",
            "Teleport cooldown: Check the timer in the top-left",
            "Blue lasers are active. Yellow outlines show the next wave.",
            "Each wave replaces all lasers at the same time.",
            "The number of lasers can increase during the game.",
        ]
        menuTexts.extend(
            instructionFont.render(instruction, True, (255, 255, 255))
            for instruction in instructions
        )
        drawCenteredLines(menuTexts, displayWidth / 2, displayHeight / 2, textSpacing)
    window.flip()
    # Give the browser time to update the screen
    await asyncio.sleep(1 / 120)

pygame.quit()
