import pygame
import random
from collections import deque

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
EnemyAnimationTimer = 0
EnemyAnimationFrame = 0
EnemyOffset = 0
EnemySpeed = 35.0
EnemyVerticalSpeed = 35.0
EnemyPauseTimer = 0
EnemyDirection = 1
EnemyVerticalDirection = 1
EnemyPatrolAxis = "horizontal"
EnemyChasing = False
EnemyAlertTimer = 0
ENEMY_ALERT_DURATION = 2.0
EnemyDecisionTimer = 0
EnemyChaseVerticalDirection = 1
EnemyLastSeenX = 0
EnemyLastSeenY = 0
EnemyPath = []
EnemyPathGoal = None
EnemyWasChasing = False
EnemySearching = False
EnemySearchTimer = 0.0
EnemySearchCenterX = 0
EnemySearchCenterY = 0
EnemySearchDirection = 1
EnemySearchSpeed = 25.0
ENEMY_SEARCH_RANGE = 48
PlayerOffsetY = 0
PlayerIdleTimer = 0
PlayerIdleOffsetY = 0
PlayerLives = 3
PlayerScore = 0
PlayerInvulnerabilityTimer = 0
PlayerInvulnerabilityDuration = 1.5

WALL_COLOR = (55, 55, 65)
FLOOR_COLOR = (125, 105, 75)
PLAYER_SIZE = 32
TILE_SIZE = 32
ENEMY_SIZE = 24
ENEMY_DETECTION_RANGE = 120
EnemyX = 484
EnemyY = 68
ENEMY_MIN_Y = 64
ENEMY_MAX_Y = 128

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


def findPath(StartColumn, StartRow, GoalColumn, GoalRow):
    Start = (StartColumn, StartRow)
    Goal = (GoalColumn, GoalRow)

    Queue = deque([Start])
    Previous = {Start: None}

    while Queue:
        Current = Queue.popleft()

        if Current == Goal:
            break

        Column, Row = Current

        Neighbors = [
            (Column + 1, Row),
            (Column - 1, Row),
            (Column, Row + 1),
            (Column, Row - 1)
        ]

        for Neighbor in Neighbors:
            NeighborColumn, NeighborRow = Neighbor

            if not isWall(NeighborColumn, NeighborRow) and Neighbor not in Previous:
                Previous[Neighbor] = Current
                Queue.append(Neighbor)

    if Goal not in Previous:
        return []

    Path = []
    Current = Goal

    while Current is not None:
        Path.append(Current)
        Current = Previous[Current]

    Path.reverse()
    return Path


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


def canEnemyMove(X, Y):
    EnemyRect = pygame.Rect(X, Y, ENEMY_SIZE, ENEMY_SIZE)

    for Row, Line in enumerate(DungeonMap):
        for Column, Tile in enumerate(Line):
            if Tile == "#":
                WallRect = pygame.Rect(
                    Column * TILE_SIZE,
                    Row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                if EnemyRect.colliderect(WallRect):
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

    if PlayerInvulnerabilityTimer > 0:
        PlayerInvulnerabilityTimer -= DeltaTime

    if GameState == "playing":
        PlayerCenterX = PlayerX + PLAYER_SIZE // 2
        PlayerCenterY = PlayerY + PLAYER_SIZE // 2
        EnemyCenterX = int(EnemyX) + ENEMY_SIZE // 2
        EnemyCenterY = EnemyY + ENEMY_SIZE // 2
        EnemyColumn = int(EnemyX + ENEMY_SIZE // 2) // TILE_SIZE
        EnemyRow = int(EnemyY + ENEMY_SIZE // 2) // TILE_SIZE

        VerticalDistance = PlayerCenterY - EnemyCenterY

        if VerticalDistance > 0:
            EnemyChaseVerticalDirection = 1
        elif VerticalDistance < 0:
            EnemyChaseVerticalDirection = -1

        PlayerDetected = False

        if abs(PlayerCenterY - EnemyCenterY) <= TILE_SIZE:
            if EnemyDirection == 1 and EnemyCenterX < PlayerCenterX <= EnemyCenterX + ENEMY_DETECTION_RANGE:
                PlayerDetected = True
            elif EnemyDirection == -1 and EnemyCenterX - ENEMY_DETECTION_RANGE <= PlayerCenterX < EnemyCenterX:
                PlayerDetected = True

        if PlayerDetected:
            EnemyChasing = True
            EnemyAlertTimer = ENEMY_ALERT_DURATION
            EnemyLastSeenX = PlayerCenterX
            EnemyLastSeenY = PlayerCenterY
        elif EnemyAlertTimer > 0:
            EnemyAlertTimer -= DeltaTime
        else:
            EnemyChasing = False

        EnemyAnimationTimer += DeltaTime

        if EnemyChasing:
            EnemyPauseTimer = 0

            PlayerColumn = EnemyLastSeenX // TILE_SIZE
            PlayerRow = EnemyLastSeenY // TILE_SIZE

            if not EnemyWasChasing or EnemyPathGoal != (PlayerColumn, PlayerRow):
                print("Calculating path:", EnemyColumn, EnemyRow, "->", PlayerColumn, PlayerRow)

                EnemyPath = findPath(
                    EnemyColumn,
                    EnemyRow,
                    PlayerColumn,
                    PlayerRow
                )

                EnemyPathGoal = (PlayerColumn, PlayerRow)

                if len(EnemyPath) > 1:
                    EnemyPath.pop(0)

            EnemyWasChasing = True

            if EnemyPath:
                TargetColumn, TargetRow = EnemyPath[0]

                TargetX = TargetColumn * TILE_SIZE + TILE_SIZE // 2
                TargetY = TargetRow * TILE_SIZE + TILE_SIZE // 2

                EnemyCenterX = int(EnemyX) + ENEMY_SIZE // 2
                EnemyCenterY = int(EnemyY) + ENEMY_SIZE // 2

                DistanceX = TargetX - EnemyCenterX
                DistanceY = TargetY - EnemyCenterY

                if abs(DistanceX) < 2 and abs(DistanceY) < 2:
                    EnemyPath.pop(0)

                else:
                    PreviousEnemyY = EnemyY

                    if DistanceY > 0:
                        MoveDistance = min(EnemyVerticalSpeed * DeltaTime, DistanceY)
                        EnemyY += MoveDistance
                    elif DistanceY < 0:
                        MoveDistance = min(EnemyVerticalSpeed * DeltaTime, abs(DistanceY))
                        EnemyY -= MoveDistance

                    if not canEnemyMove(EnemyX, EnemyY):
                        EnemyY = PreviousEnemyY

                    PreviousEnemyX = EnemyX

                    if DistanceX > 0:
                        MoveDistance = min(EnemySpeed * DeltaTime, DistanceX)
                        EnemyX += MoveDistance
                    elif DistanceX < 0:
                        MoveDistance = min(EnemySpeed * DeltaTime, abs(DistanceX))
                        EnemyX -= MoveDistance

                    if not canEnemyMove(EnemyX, EnemyY):
                        EnemyX = PreviousEnemyX

        else:
            if EnemyWasChasing:
                EnemyPauseTimer = 0
                EnemySearchTimer = 3.0
                EnemySearchCenterX = EnemyX
                EnemySearchCenterY = EnemyY
                EnemyPath = []
                EnemyPathGoal = None
                EnemySearching = True

            EnemyWasChasing = False

            if EnemySearching:
                EnemySearchTimer -= DeltaTime

                if EnemySearchTimer <= 0:
                    EnemySearching = False
                    EnemySearchTimer = 0

            if EnemySearching:
                SearchMinX = EnemySearchCenterX - ENEMY_SEARCH_RANGE
                SearchMaxX = EnemySearchCenterX + ENEMY_SEARCH_RANGE

                PreviousEnemyX = EnemyX
                EnemyX += EnemySearchSpeed * EnemySearchDirection * DeltaTime

                if (EnemyX < SearchMinX or EnemyX > SearchMaxX
                        or not canEnemyMove(EnemyX, EnemyY)):
                    EnemyX = PreviousEnemyX
                    EnemySearchDirection *= -1

            elif EnemyPauseTimer > 0:
                EnemyPauseTimer -= DeltaTime

            else:
                EnemyDecisionTimer += DeltaTime

                if EnemyDecisionTimer >= 1.0:
                    if random.random() < 0.25:
                        EnemyDirection *= -1

                    EnemyDecisionTimer = 0

                if EnemyPatrolAxis == "horizontal":
                    EnemyX += EnemySpeed * EnemyDirection * DeltaTime

                    if EnemyX <= 400:
                        EnemyX = 400
                        EnemyDirection = 1
                        EnemyVerticalDirection = -1
                        EnemyPauseTimer = random.uniform(0.4, 1.5)
                        EnemySpeed = random.uniform(25.0, 55.0)
                        EnemyPatrolAxis = "vertical"

                    elif EnemyX >= 560:
                        EnemyX = 560
                        EnemyDirection = -1
                        EnemyVerticalDirection = 1
                        EnemyPauseTimer = random.uniform(0.4, 1.5)
                        EnemySpeed = random.uniform(25.0, 55.0)
                        EnemyPatrolAxis = "vertical"

                elif EnemyPatrolAxis == "vertical":
                    EnemyY += EnemyVerticalSpeed * EnemyVerticalDirection * DeltaTime

                    if EnemyY <= ENEMY_MIN_Y:
                        EnemyY = ENEMY_MIN_Y
                        EnemyDirection = 1
                        EnemyPauseTimer = random.uniform(0.4, 1.5)
                        EnemyPatrolAxis = "horizontal"

                    elif EnemyY >= ENEMY_MAX_Y:
                        EnemyY = ENEMY_MAX_Y
                        EnemyDirection = -1
                        EnemyPauseTimer = random.uniform(0.4, 1.5)
                        EnemyPatrolAxis = "horizontal"
        if EnemyAnimationTimer >= 0.3:
            EnemyAnimationFrame = 1 - EnemyAnimationFrame
            EnemyAnimationTimer = 0
            EnemyOffset = -2 if EnemyAnimationFrame == 0 else 0

    Screen.fill((80, 100, 140))

    if GameState == "won":
        Text = Font.render("You escaped the dungeon!", True, (255, 255, 255))
        TextRect = Text.get_rect(center=(400, 300))
        Screen.blit(Text, TextRect)
        ExitText = SmallFont.render("Press ESC to quit", True, (200, 200, 200))
        ExitRect = ExitText.get_rect(center=(400, 350))
        Screen.blit(ExitText, ExitRect)
        RestartText = SmallFont.render("Press R to play again", True, (200, 200, 200))
        FinalScoreText = SmallFont.render(f"Final Score: {PlayerScore}", True, (255, 220, 100))
        FinalScoreRect = FinalScoreText.get_rect(center=(400, 425))
        Screen.blit(FinalScoreText, FinalScoreRect)
        RestartRect = RestartText.get_rect(center=(400, 385))
        Screen.blit(RestartText, RestartRect)

    elif GameState == "lost":
        Text = Font.render("You were caught!", True, (220, 70, 70))
        TextRect = Text.get_rect(center=(400, 300))
        Screen.blit(Text, TextRect)

        ExitText = SmallFont.render("Press ESC to quit", True, (200, 200, 200))
        ExitRect = ExitText.get_rect(center=(400, 350))
        Screen.blit(ExitText, ExitRect)

        RestartText = SmallFont.render("Press R to try again", True, (200, 200, 200))
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

        # DEBUG: Draw enemy path
        for Column, Row in EnemyPath:
            pygame.draw.rect(
                Screen,
                (255, 255, 0),
                (Column * TILE_SIZE + 12, Row * TILE_SIZE + 12, 8, 8)
            )

       # pygame.draw.rect(Screen, (220, 190, 120), (PlayerX, PlayerY, PLAYER_SIZE, PLAYER_SIZE))

        # BUG
        EnemyDrawY = EnemyY + EnemyOffset
        EnemyDrawX = int(EnemyX)
        pygame.draw.rect(Screen, (180, 60, 60), (EnemyDrawX, EnemyDrawY, ENEMY_SIZE, ENEMY_SIZE))
        pygame.draw.rect(Screen, (20, 20, 20), (EnemyDrawX + 5, EnemyDrawY + 6, 4, 4)) # body
        pygame.draw.rect(Screen, (120, 35, 35), (EnemyDrawX + 2, EnemyDrawY + 2, 20, 3)) # shell
        pygame.draw.rect(Screen, (20, 20, 20), (EnemyDrawX + 15, EnemyDrawY + 6, 4, 4)) # eye
        pygame.draw.rect(Screen, (60, 20, 20), (EnemyDrawX + 9, EnemyDrawY + 16, 6, 2)) # eye
        if EnemyAnimationFrame == 0:
            pygame.draw.rect(Screen, (40, 40, 40), (EnemyDrawX + 5, EnemyDrawY - 4, 3, 6)) # tentacle
            pygame.draw.rect(Screen, (40, 40, 40), (EnemyDrawX + 16, EnemyDrawY - 4, 3, 6))
        else:
            pygame.draw.rect(Screen, (40, 40, 40), (EnemyDrawX + 5, EnemyDrawY - 6, 3, 8)) # tentacle
            pygame.draw.rect(Screen, (40, 40, 40), (EnemyDrawX + 16, EnemyDrawY - 2, 3, 4))


        if PlayerInvulnerabilityTimer <= 0 or int(PlayerInvulnerabilityTimer * 10) % 2 == 0:
            # HERO
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

        LivesText = SmallFont.render(f"Lives: {PlayerLives}", True, (255, 255, 255))
        Screen.blit(LivesText, (660, 20))
        ScoreText = SmallFont.render(f"Score: {PlayerScore}", True, (255, 255, 255))
        Screen.blit(ScoreText, (660, 55))

    pygame.display.flip()



    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
        elif Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_ESCAPE and GameState in ("won", "lost"):
                Running = False
            elif Event.key == pygame.K_r and GameState in ("won", "lost"):
                PlayerX = 100
                PlayerY = 100
                PlayerLives = 3
                PlayerInvulnerabilityTimer = 0
                PlayerScore = 0
                EnemyX = 484
                EnemyY = 68
                EnemyAnimationTimer = 0
                EnemyAnimationFrame = 0
                EnemyOffset = 0
                EnemyPauseTimer = 0
                EnemyDecisionTimer = 0
                EnemyDirection = 1
                EnemyVerticalDirection = 1
                EnemyPatrolAxis = "horizontal"
                PlayerAnimationTimer = 0
                PlayerAnimationFrame = 0
                PlayerOffsetY = 0
                PlayerIdleTimer = 0
                PlayerIdleOffsetY = 0
                PlayerDirection = "right"
                GameState = "playing"

    Keys = pygame.key.get_pressed()

    if GameState in ("won", "lost"):
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

    PlayerRect = pygame.Rect(PlayerX, PlayerY, PLAYER_SIZE, PLAYER_SIZE)
    EnemyRect = pygame.Rect(EnemyX, EnemyY, ENEMY_SIZE, ENEMY_SIZE)

    if PlayerRect.colliderect(EnemyRect) and PlayerInvulnerabilityTimer <= 0:
        PlayerLives -= 1
        PlayerScore += 50
        PlayerInvulnerabilityTimer = PlayerInvulnerabilityDuration

        if PlayerLives <= 0:
            GameState = "lost"

    if DungeonMap[PlayerY // TILE_SIZE][PlayerX // TILE_SIZE] == "E":
        PlayerScore += 100
        GameState = "won"


pygame.quit()
