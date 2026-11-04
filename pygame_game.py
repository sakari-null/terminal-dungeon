import pygame

pygame.init()
Font = pygame.font.Font(None, 48)
SmallFont = pygame.font.Font(None, 28)
Clock = pygame.time.Clock()

Screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Terminal Dungeon")

Running = True
GameState = "playing"

PlayerX = 100
PlayerY = 100
PlayerSpeed = 90.0
PlayerDirection = "right"
PlayerMoving = False
PlayerAnimationTimer = 0
PlayerAnimationFrame = 0
PlayerOffsetY = 0
PlayerIdleTimer = 0
PlayerIdleOffsetY = 0

WALL_COLOR = (55, 55, 65)
FLOOR_COLOR = (125, 105, 75)
PLAYER_SIZE = 32
TILE_SIZE = 32

DungeonMap = [
    "####################",
    "#.......#####......#",
    "#..................#",
    "#.................E#",
    "#..................#",
    "#.......#...#......#",
    "#########...########",
    "#########...########",
    "#####...........####",
    "#####...........####",
    "#####...........####",
    "#####...........####",
    "#####...........####",
    "#####...........####",
    "####################"
]

def isWall(Column, Row):

    if Row < 0 or Row >= len(DungeonMap):
        return True

    if Column < 0 or Column >= len(DungeonMap[Row]):
       return True

    if DungeonMap[Row][Column] == "#":
        return True
    else:
        return False


def canMove(X, Y):
    LeftColumn = X // TILE_SIZE
    RightColumn = (X + PLAYER_SIZE - 1) // TILE_SIZE
    TopRow = Y // TILE_SIZE
    BottomRow = (Y + PLAYER_SIZE - 1) // TILE_SIZE

    if isWall(LeftColumn, TopRow):
        return False
    if isWall(RightColumn, TopRow):
        return False
    if isWall(LeftColumn, BottomRow):
        return False
    if isWall(RightColumn, BottomRow):
        return False
    return True


def getMoveDistance(X, Y, Distance, Direction):
    Step = int(Distance)
    while Step > 0:
        if Direction == "left":
            if canMove(X - Step, Y):
                return Step
            Step -= 1

        elif Direction == "right":
            if canMove(X + Step, Y):
                return Step
            Step -= 1
            
        elif Direction == "up":
            if canMove(X, Y - Step):
                return Step
            Step -= 1
            
        elif Direction == "down":
            if canMove(X, Y + Step):
                return Step
            Step -= 1

    return 0

    
while Running:

    DeltaTime = Clock.tick(30) / 1000

    Screen.fill((80, 100, 140))
    
    if GameState == "won":
        Text = Font.render("You escaped the dungeon!", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(400, 300))
        Screen.blit(Text, TextRect)
        ExitText = SmallFont.render("Press ESC to quit", True, (200, 200, 200))
        ExitRect = ExitText.get_rect(center=(400, 350))
        Screen.blit(ExitText, ExitRect)
        RestartText = SmallFont.render("Press R to play again", True, (200, 200, 200))
        RestartRect = RestartText.get_rect(center=(400, 385))
        Screen.blit(RestartText, RestartRect)        
       
    else:

        for RowIndex, Row in enumerate(DungeonMap):
            for ColumnIndex, Tile in enumerate(Row):
                X = ColumnIndex * TILE_SIZE
                Y = RowIndex * TILE_SIZE
                if Tile == "#":
                    pygame.draw.rect(Screen, WALL_COLOR, (X, Y, TILE_SIZE, TILE_SIZE))
                elif Tile == "E":
                    pygame.draw.rect(Screen, (100, 55, 30), (X, Y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(Screen, (65, 40, 25), (X + 4, Y + 2, 24, 28), 2)
                    pygame.draw.circle(Screen, (220, 180, 70), (X + 23, Y + 16), 2)
                else:
                    pygame.draw.rect(Screen, FLOOR_COLOR, (X, Y, TILE_SIZE, TILE_SIZE))

       # pygame.draw.rect(Screen, (220, 190, 120), (PlayerX, PlayerY, PLAYER_SIZE, PLAYER_SIZE))

        DrawY = PlayerY + PlayerOffsetY + PlayerIdleOffsetY

        pygame.draw.rect(Screen, (220, 190, 120), (PlayerX + 8, DrawY, 16, 12))
        pygame.draw.rect(Screen, (100, 65, 35), (PlayerX + 3, DrawY + 0, 26, 5))
        pygame.draw.rect(Screen, (130, 85, 45), (PlayerX + 8, DrawY - 5, 16, 7))

        if PlayerDirection == "right":
            pygame.draw.rect(Screen, (30, 30, 30), (PlayerX + 19, DrawY + 4, 3, 3))

        elif PlayerDirection == "left":
            pygame.draw.rect(Screen, (30, 30, 30), (PlayerX + 11, DrawY + 4, 3, 3))

        elif PlayerDirection == "down":
            pygame.draw.rect(Screen, (30, 30, 30), (PlayerX + 11, DrawY + 4, 3, 3))
            pygame.draw.rect(Screen, (30, 30, 30), (PlayerX + 19, DrawY + 4, 3, 3))

        pygame.draw.rect(Screen, (60, 90, 130), (PlayerX + 6, DrawY + 12, 20, 12))

        if PlayerAnimationFrame == 0:
            pygame.draw.rect(Screen, (60, 90, 130), (PlayerX, DrawY + 15, 6, 10))
            pygame.draw.rect(Screen, (60, 90, 130), (PlayerX + 26, DrawY + 11, 6, 10))
        else:
            pygame.draw.rect(Screen, (60, 90, 130), (PlayerX, DrawY + 11, 6, 10))
            pygame.draw.rect(Screen, (60, 90, 130), (PlayerX + 26, DrawY + 15, 6, 10))
        
        if PlayerAnimationFrame == 0:
            pygame.draw.rect(Screen, (70, 55, 45), (PlayerX + 8, DrawY + 22, 6, 10))
            pygame.draw.rect(Screen, (70, 55, 45), (PlayerX + 18, DrawY + 26, 6, 6))
        else:
            pygame.draw.rect(Screen, (70, 55, 45), (PlayerX + 8, DrawY + 26, 6, 6))
            pygame.draw.rect(Screen, (70, 55, 45), (PlayerX + 18, DrawY + 22, 6, 10))

    pygame.display.flip()

    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
        elif Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_ESCAPE and GameState == "won":
                Running = False
            elif Event.key == pygame.K_r and GameState == "won":
                PlayerX = 100
                PlayerY = 100
                PlayerAnimationTimer = 0
                PlayerAnimationFrame = 0
                PlayerOffsetY = 0
                PlayerIdleTimer = 0
                PlayerIdleOffsetY = 0
                PlayerDirection = "right"
                GameState = "playing"

    Keys = pygame.key.get_pressed()
    
    if GameState == "won":
        continue
    
    PlayerMoving = False

    if Keys[pygame.K_RIGHT] or Keys[pygame.K_LEFT] or Keys[pygame.K_UP] or Keys[pygame.K_DOWN]:
        PlayerMoving = True

    if PlayerMoving:
        PlayerAnimationTimer += DeltaTime
        PlayerIdleTimer = 0

        if PlayerAnimationTimer >= 0.2:
            PlayerAnimationFrame = 1 - PlayerAnimationFrame
            PlayerAnimationTimer = 0
    else:
        PlayerAnimationFrame = 0
        PlayerAnimationTimer = 0
        PlayerIdleTimer += DeltaTime
        PlayerIdleOffsetY = -abs((int(PlayerIdleTimer * 1.5) % 4) - 2)
    
    MoveAmount = PlayerSpeed * DeltaTime

    if PlayerMoving:
        PlayerOffsetY = -2 if PlayerAnimationFrame == 0 else 0
    else:
        PlayerOffsetY = 0

    if Keys[pygame.K_RIGHT]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "right")
        PlayerX += MoveDistance
        PlayerDirection = "right"

    if Keys[pygame.K_LEFT]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "left")
        PlayerX -= MoveDistance
        PlayerDirection = "left"

    if Keys[pygame.K_UP]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "up")
        PlayerY -= MoveDistance
        PlayerDirection = "up"

    if Keys[pygame.K_DOWN]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "down")
        PlayerY += MoveDistance
        PlayerDirection = "down"

    if DungeonMap[PlayerY // TILE_SIZE][PlayerX // TILE_SIZE] == "E":
        GameState = "won"


pygame.quit()
