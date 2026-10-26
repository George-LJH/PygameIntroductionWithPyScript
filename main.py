import asyncio
import random
import pygame
import time
import js
# Function to generate random obstacle, optional parameter to ensure it doesn't collide with something
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
maxObstacleLimit = 5
teleportDistance = 300
teleportCooldown = 500
lastTeleportTime = -teleportCooldown
githubUrl = "https://github.com/George-LJH/PygameIntroductionWithPyScript"
pygame.init()
paused = False
teleportGraceTime = 250
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "Blnk - Game"
screen = window.get_surface()
playerImage = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
playerImage.fill((24, 25, 26))
teleportPreview = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
teleportPreview.fill((255, 0, 0, 100))
gameOverOnce = False
highscore = 0
cachedUiScale = None
font = None
instructionFont = None
titleFont = pygame.font.SysFont("Arial", 64, bold=True)
titleSurface = titleFont.render("Blnk", True, (255, 255, 255))
titleRect = titleSurface.get_rect()
titleRect.centerx = screenWidth // 2
titleRect.top = 40
fps = 120
# Function to draw multiple lines of text centered for the instructions
def drawCenteredLines(textSurfaces, centerX, centerY, spacing):
    totalHeight = sum(text.get_height() for text in textSurfaces)
    totalHeight += spacing * (len(textSurfaces) - 1)
    currentY = centerY - totalHeight / 2
    for text in textSurfaces:
        textPosition = text.get_rect(center=(centerX, currentY + text.get_height() / 2))
        screen.blit(text, textPosition)
        currentY += text.get_height() + spacing

# Function to reset the game state
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
    lastTeleportTime = pygame.time.get_ticks() - max(teleportCooldown, teleportGraceTime)
# Function to start the game
def startGame():
    global gameStarted
    resetGame()
    gameStarted = True

running = True
resetGame()

while running:
    # Get the current display size and calculate the UI scale based on the screen dimensions
    displayWidth, displayHeight = screen.get_size()
    uiScale = min(displayWidth / screenWidth, displayHeight / screenHeight)
    teleportedThisFrame = False
    GithubButton = pygame.Rect(
        displayWidth // 2 - 140,
        displayHeight - 90,
        280,
        70,
    )
    resetData = pygame.Rect(
        10,
        displayHeight - 55,
        200,
        50,
    )
    playerImage.fill((182, 182, 182))
    
    if uiScale != cachedUiScale:
        font = pygame.font.SysFont(None, max(20, round(40 * uiScale)))
        instructionFont = pygame.font.SysFont(None, max(16, round(28 * uiScale)))
        cachedUiScale = uiScale
    textSpacing = max(8, round(12 * uiScale))
    # Handle events(NOT FOR MOVEMENT, JUST FOR QUIT AND TELEPORTATION)
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
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        playerY += teleportDistance
                        teleported = True
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        playerX += teleportDistance
                        teleported = True
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        playerX -= teleportDistance
                        teleported = True

                    if teleported:
                        lastTeleportTime = currentTeleportTime
                        teleportedThisFrame = True
                        playerX = max(0, min(playerX, screenWidth - playerSize))
                        playerY = max(0, min(playerY, screenHeight - playerSize))
            if event.key == pygame.K_p and gameStarted:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GithubButton.collidepoint(event.pos) and not gameStarted:
                js.window.open(githubUrl, "_blank")
            if resetData.collidepoint(event.pos) and not gameStarted:
                js.localStorage.removeItem("highScore")
                resetGame()
    if gameStarted and not paused:
        screen.fill((15, 12, 30))
        # Handle Movement
        keys = pygame.key.get_pressed()
        if not teleportedThisFrame:
            move_x = (
                (keys[pygame.K_RIGHT] or keys[pygame.K_d])
                - (keys[pygame.K_LEFT] or keys[pygame.K_a])
            )
            move_y = (
                (keys[pygame.K_DOWN] or keys[pygame.K_s])
                - (keys[pygame.K_UP] or keys[pygame.K_w])
            )
            if move_x != 0 and move_y != 0:
                movementMultiplier = 0.7071
            else:
                movementMultiplier = 1.0
            playerX += move_x * playerSpeed * movementMultiplier
            playerY += move_y * playerSpeed * movementMultiplier
        playerX = max(0, min(playerX, screenWidth - playerSize))
        playerY = max(0, min(playerY, screenHeight - playerSize))

        player = pygame.Rect(playerX, playerY, playerSize, playerSize)
        trailFrameCounter += 1
        # Trail behind player
        if trailFrameCounter >= 3:
            trail.append((player.copy(), 150))
            trailFrameCounter = 0
            trail = trail[-12:]
        updatedTrail = []
        for trailRect, opacity in trail:
            opacity -= 8
            if opacity > 0:
                updatedTrail.append((trailRect, opacity))

        trail = updatedTrail
        # Obstacles
        currentTimeObstacleGeneration = time.time()
        if currentTimeObstacleGeneration - lastObstacleTime >= obstacleInterval:
            
            obstacleSize = min(obstacleSize + 1, 50)
            if score % 5 == 0 and score != 0:
                maxObstacles = min(
                    maxObstacleLimit,
                    maxObstacles + min(7, int(score / 5)),
                )
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
            pygame.draw.rect(screen, (255, 0, 0), obstacle)
        # Show teleport preview
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
            screen.blit(teleportPreview, (max(0, playerX - teleportDistance), max(0, playerY - teleportDistance)))
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            screen.blit(teleportPreview, (max(0, playerX - teleportDistance), max(0, playerY + teleportDistance)))
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
            screen.blit(teleportPreview, (max(0, playerX + teleportDistance), max(0, playerY - teleportDistance)))
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            screen.blit(teleportPreview, (max(0, playerX + teleportDistance), max(0, playerY + teleportDistance)))
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            screen.blit(teleportPreview, (max(0, playerX - teleportDistance), playerY))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            screen.blit(teleportPreview, (min(screenWidth - teleportPreview.get_width(), playerX + teleportDistance), playerY))
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            screen.blit(teleportPreview, (playerX, max(0, playerY - teleportDistance)))
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            screen.blit(teleportPreview, (playerX, min(screenHeight - teleportPreview.get_height(), playerY + teleportDistance)))
        # Handle Trails(AGAIN)
        for trailRect, opacity in trail:
            scaleFactor = opacity / 150.0
            scaledWidth = max(1, int(playerSize * scaleFactor))
            scaledHeight = max(1, int(playerSize * scaleFactor))
            scaledTrailSurface = pygame.transform.scale(playerImage, (scaledWidth, scaledHeight))
            alphaSurface = pygame.Surface((scaledWidth, scaledHeight), pygame.SRCALPHA)
            alphaSurface.fill((255, 255, 255, int(opacity)))
            scaledTrailSurface.blit(alphaSurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            offsetX = (playerSize - scaledWidth) // 2
            offsetY = (playerSize - scaledHeight) // 2
            
            screen.blit(scaledTrailSurface, (trailRect.x + offsetX, trailRect.y + offsetY))
        # Obstacles Collision Detection(to change player color)
        for nextObstacle in nextObstacles:
            if player.colliderect(nextObstacle):
                playerImage.fill((255, 0, 0))
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                playerImage.fill((255, 0, 0))
        screen.blit(playerImage, player)
        # Draw next obstacles with yellow outline
        for nextObstacle in nextObstacles:
            preview_surf = pygame.Surface((nextObstacle.width, nextObstacle.height), pygame.SRCALPHA).convert_alpha()
            pygame.draw.rect(preview_surf, (255, 255, 0, 112), (0, 0, nextObstacle.width, nextObstacle.height), 5)
            screen.blit(preview_surf, (nextObstacle.x, nextObstacle.y))
        # HUD
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
            teleportPreview.fill((255, 0, 0, 100))

        else:
            teleportCooldownText = font.render(
                f"Teleport ready!",
                True,
                (255, 255, 255),
            )
            teleportPreview.fill((0,255, 0, 100))
        obstacleIntervalText = font.render(
            f"Game Speed: {obstacleInterval:.2f}s",
            True,
            (255, 255, 255),
        )

        teleportGraceRemaining = max(
            0, (teleportGraceTime - (pygame.time.get_ticks() - lastTeleportTime)) / 1000
        )
        teleportGraceTimeText = font.render(
            f"Teleport Grace Period: {teleportGraceRemaining:.3f}s",
            True,
            (255, 255, 255),
        )
        hudTexts = [scoreText, teleportCooldownText, obstacleIntervalText, teleportGraceTimeText]
        tallestHudText = 0
        for text in hudTexts:
            if text.get_height() > tallestHudText:
                tallestHudText = text.get_height()
        hudY = tallestHudText / 2 + textSpacing
        for text in hudTexts:
            textPosition = text.get_rect(topleft=(textSpacing, hudY))
            screen.blit(text, textPosition)
            hudY += text.get_height() + textSpacing

        # Game Over Screen
        if (
            pygame.time.get_ticks() - lastTeleportTime >= teleportGraceTime
            and any(player.colliderect(obstacle) for obstacle in obstacles)
        ):
            currentScreen = screen.copy()
            for x in range(0, screenWidth, 10):
                screen.blit(currentScreen, (0, 0))
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (x - screenWidth, 0, screenWidth, screenHeight),
                )
                window.flip()
                await asyncio.sleep(1 / fps)

            gameOverOnce = True
            gameStarted = False
            obstacleInterval = 0.75
    # Paused code
    elif paused:
        pauseText = font.render("PAUSED - Press P to resume", True, (255, 255, 255))
        screen.blit(
            pauseText,
            pauseText.get_rect(center=(displayWidth / 2, displayHeight / 2))
        )
    else:
        # Go to GITHUB REPO
        screen.fill((0, 0, 0))
        GithubButtonColor = (0, 180, 255) if GithubButton.collidepoint(
            pygame.mouse.get_pos()
        ) else (0, 120, 255)
        # RESET DATA BUTTON
        resetDataButtonColor = (0, 180, 255) if resetData.collidepoint(
            pygame.mouse.get_pos()
        ) else (0, 120, 255)
        # Draw the buttons
        pygame.draw.rect(screen, resetDataButtonColor, resetData)
        resetDataButtonLabel = "Reset Data"
        resetDataButtonText = font.render(resetDataButtonLabel, True, (255, 255, 255))
        resetDataButtonTextPosition = resetDataButtonText.get_rect(center=resetData.center)
        screen.blit(resetDataButtonText, resetDataButtonTextPosition)   
        pygame.draw.rect(screen, GithubButtonColor, GithubButton)
        githubButtonLabel = "View GitHub Repo"
        GithubButtonText = font.render(githubButtonLabel, True, (255, 255, 255))
        GithubButtonTextPosition = GithubButtonText.get_rect(center=GithubButton.center)
        screen.blit(GithubButtonText, GithubButtonTextPosition)
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
            "Teleport: Press 1 or 2 directional keys (2 to teleport diagonally), then press the Spacebar.",
            "Teleport cooldown: Check the top-left timer or your teleportation preview ",
            "a red indicator on the teleport preview means you must wait, while a green indicator means you are ready to teleport",
            "If your character turns red, it means you are in the path of an incoming laser",
            "Red lasers are active. Yellow outlines show the next wave.",
            "Each wave replaces all lasers at the same time.",
            "The number of lasers will increase during the game.",
        ]
        menuTexts.extend(
            instructionFont.render(instruction, True, (255, 255, 255))
            for instruction in instructions
        )
        drawCenteredLines(menuTexts, displayWidth / 2, displayHeight / 2, textSpacing)
        screen.blit(titleSurface, titleRect) 
    window.flip()
    # Give the browser time to update the screen
    await asyncio.sleep(1 / fps)

pygame.quit()
