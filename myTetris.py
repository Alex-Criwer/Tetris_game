import pygame
import random

pygame.font.init()

windowSize = [900, 800]
playingArea = [450, 600]
windowWidth, windowHight = windowSize[0], windowSize[1]
playingAreaWidth, playingAreaHight = playingArea[0], playingArea[1]
cellWidth = cellHight = playingAreaWidth // 30

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
dark_red = (139, 0, 0)
grey = (128, 128, 128)
gold = (255, 215, 0)

colorsOfFigures = [white, green, red, dark_red, grey, gold]

O_single = ['00000',
            '00000',
            '00110',
            '00110',
            '00000']

S_up = ['00000',
        '00100',
        '00110',
        '00010',
        '00000']

S_down = ['00000',
          '00000',
          '00110',
          '01100',
          '00000']

I_up = ['00100',
        '00100',
        '00100',
        '00100',
        '00000']

I_down = ['00000',
          '00000',
          '11110',
          '00000',
          '00000']

T_down = ['00000',
          '00000',
          '01110',
          '00100',
          '00000']

T_up = ['00000',
        '00100',
        '01110',
        '00000',
        '00000']

T_left = ['00000',
          '00100',
          '01100',
          '00100',
          '00000']

T_right = ['00000',
           '00100',
           '00110',
           '00100',
           '00000']

L_down = ['00000',
          '00000',
          '01110',
          '01000',
          '00000']

L_up = ['00000',
        '00010',
        '01110',
        '00000',
        '00000']

L_left = ['00000',
          '00110',
          '00010',
          '00010',
          '00000']

L_right = ['00000',
           '00100',
           '00100',
           '00110',
           '00000']

Z_down = ['00000',
          '00000',
          '01100',
          '00110',
          '00000']

Z_up = ['00000',
        '00010',
        '00110',
        '00100',
        '00000']

O = [O_single]
S = [S_up, S_down]
Z = [Z_up, Z_down]
I = [I_up, I_down]
S = [S_up, S_down]
T = [T_up, T_down, T_left, T_right]

figures = [O, S, Z, I, S, T]


class Figure:
    def __init__(self, x, y, figure):
        self.xField = x
        self.yField = y
        self.figure = figure
        self.color = random.choice(colorsOfFigures)
        self.numberOsSwaps = 0


def randomFigure():
    # tmp = random.choice(figures)  # todo проверь
    return Figure(6, 0, random.choice(figures))


def drawField(window, row, columns):
    topX = (windowWidth - playingAreaWidth) // 2
    topY = windowHight - playingAreaHight - 80
    for i in range(row):
        pygame.draw.line(window, (176, 224, 230), (topX, topY + 30 * i),
                         (topX + playingAreaWidth, topY + 30 * i))
        for j in range(columns):
            pygame.draw.line(window, (176, 224, 230), (topX + j * 30, topY),
                             (topX + j * 30, topY + playingAreaHight))


def createFieldOfColors(cellToColor={}):
    fieldOfColors = [[black for j in range(15)] for i in
                     range(20)]
    for y in range(len(fieldOfColors)):
        for x in range(len(fieldOfColors[y])):
            if (x, y) in cellToColor:
                cellWithColor = cellToColor[(x, y)]
                fieldOfColors[y][x] = cellWithColor
    return fieldOfColors


def drawWindow(window, fieldOfColors):
    window.fill(black)
    pygame.draw.rect(window, white, (
        (windowWidth - playingAreaWidth) // 2, (windowHight - playingAreaHight - 80), playingAreaWidth,
        playingAreaHight), 5)
    # pygame.font.init()
    for i in range(len(fieldOfColors)):
        for j in range(len(fieldOfColors[i])):
            pygame.draw.rect(window, fieldOfColors[i][j], (
                (windowWidth - playingAreaWidth) // 2 + j * 30, (windowHight - playingAreaHight - 80) + i * 30,
                30, 30), 0)
    drawField(window, 20, 15)
    pygame.display.update()


def mySwap(figure):
    whatIsTheFigure = figure.figure[figure.numberOsSwaps % len(figure.figure)]
    positions = []
    for i, line in enumerate(whatIsTheFigure):
        str = list(line)
        for j, column in enumerate(str):
            if column == '1':
                positions.append((figure.xField + j, figure.yField + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid(figure, fieldOfColors):
    allPositions = [[(x, y) for x in range(15) if fieldOfColors[y][x] == black] for y in range(20)]
    allPositions = [j for sub in allPositions for j in sub]
    swapped = mySwap(figure)

    for pos in swapped:
        if pos not in allPositions and pos[1] >= 0:
            return False
    return True


def aboveTheScreen(positions):
    for (x, y) in positions:
        if y <= 0:
            return True
    return False


def game(window):
    # global field;
    cellToColor = {}
    field = createFieldOfColors(cellToColor)
    run = True
    changeFigure = False
    clock = pygame.time.Clock()
    fall_time, timeBeforeTheNext = 0, 0.25  # сколько времени займет перед тем, как что-то начнет падать
    currentFigure = randomFigure()
    nextFigure = randomFigure()

    while run:
        field = createFieldOfColors(cellToColor)
        fall_time += clock.get_rawtime()  # in millisecond that is why divide into 1000
        clock.tick()

        if (fall_time / 1000 > timeBeforeTheNext):
            fall_time = 0
            currentFigure.yField += 1
            if not valid(currentFigure, field) and currentFigure.yField > 0:
                currentFigure.yField -= 1
                changeFigure = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                        currentFigure.xField -= 1
                        if not valid(currentFigure ,field):
                            currentFigure.xField += 1
                elif event.key == pygame.K_RIGHT:
                        currentFigure.xField += 1
                        if not valid(currentFigure ,field):
                            currentFigure.xField -= 1
                if event.key == pygame.K_DOWN:
                    currentFigure.yField += 1
                    if not valid(currentFigure, field):
                        currentFigure.yField -= 1

                elif event.key == pygame.K_UP:
                    currentFigure.numberOsSwaps = (currentFigure.numberOsSwaps + 1) % len(
                        currentFigure.figure)
                    if not valid(currentFigure, field):
                        currentFigure.numberOsSwaps = (currentFigure.numberOsSwaps - 1) % len(currentFigure.figure)

        figure_position = mySwap(currentFigure)

        for i in range(len(figure_position)):
            x, y = figure_position[i]
            if y >= 0:
                field[y][x] = currentFigure.color

        if changeFigure:
            for pos in figure_position:
                point = (pos[0], pos[1])
                cellToColor[point] = currentFigure.color
            currentFigure = nextFigure
            nextFigure = randomFigure()
            changeFigure = False

        drawWindow(window, field)

        if aboveTheScreen(cellToColor):
            run = False

    tmp = pygame.font.SysFont('arial', 50, bold=True)
    label = tmp.render("You lost", 1, (255, 20, 147))
    window.blit(label, (275, 450))
    pygame.display.update()
    pygame.time.delay(1500)


    pygame.display.quit()


def playing(window):
    game(window)


window = pygame.display.set_mode((windowWidth, windowHight))
pygame.display.set_caption("TETRIS")
playing(window)
