import pygame

pygame.init()
Clock = pygame.time.Clock()

Screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Debian Dungeon")

Running = True

PlayerX = 100
PlayerY = 100
PlayerSpeed = 90.0

WALL_COLOR = (55, 55, 65)
FLOOR_COLOR = (125, 105, 75)
PLAYER_SIZE = 32
TILE_SIZE = 32

DungeonMap = [
    "####################",
    "#.......#####......#",
    "#..................#",
    "#..................#",
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

    for RowIndex, Row in enumerate(DungeonMap):
        for ColumnIndex, Tile in enumerate(Row):
            X = ColumnIndex * TILE_SIZE
            Y = RowIndex * TILE_SIZE
            if Tile == "#":
                pygame.draw.rect(Screen, WALL_COLOR, (X, Y, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(Screen, FLOOR_COLOR, (X, Y, TILE_SIZE, TILE_SIZE))

    pygame.draw.rect(Screen, (220, 190, 120), (PlayerX, PlayerY, PLAYER_SIZE, PLAYER_SIZE))
    pygame.display.flip()

    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False

    Keys = pygame.key.get_pressed()
    MoveAmount = PlayerSpeed * DeltaTime

    if Keys[pygame.K_RIGHT]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "right")
        PlayerX += MoveDistance

    if Keys[pygame.K_LEFT]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "left")
        PlayerX -= MoveDistance

    if Keys[pygame.K_UP]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "up")
        PlayerY -= MoveDistance

    if Keys[pygame.K_DOWN]:
        MoveDistance = getMoveDistance(PlayerX, PlayerY, MoveAmount, "down")
        PlayerY += MoveDistance


pygame.quit()
